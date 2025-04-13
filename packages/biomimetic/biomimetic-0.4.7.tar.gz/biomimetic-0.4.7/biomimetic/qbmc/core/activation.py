# qbmc/core/activations.py
from collections import Counter, defaultdict
import random
import numpy as np
from typing import Dict, List, Union
from .learning import QBMCLearner
from .preprocessing import QBMCDataContainer

BINSIZE = 9

class QBMCActivator:
    def __init__(self, learner: QBMCLearner = None, classification: bool = False, binsize=BINSIZE):
        self.learner = learner
        self.classification = classification
        self.binsize = binsize
        self.processor = learner.processor
        
    def predict(self, X: np.ndarray, debug: bool = False) -> np.ndarray:
        """Make predictions for input data"""
        container = self.processor.auto_convert(X)
        if debug:
            print("\n=== Prediction Input ===")
            print("Original Input:\n", X)
            print("Quantized:", container.quantized)
            if container.quantized:
                print("Scale:", container.scale, "Offset:", container.offset)
            print("Binary Representation:\n", container.binary.astype(int))
            
        return np.array([self.forward_pass(x, container, debug)['prediction'] 
                        for x in container.binary])

    def forward_pass(self, x_bin: np.ndarray, container: QBMCDataContainer, debug: bool = False) -> Dict:
        """Perform a forward pass through the network"""
        if debug:
            print("\n=== Forward Pass ===")
            print("Input binary vector:\n", x_bin.astype(int))
            
        # 1) Convert binary vectors to integers
        x_vals = [self.processor._from_bin(x_bin[f]) for f in range(x_bin.shape[0])]
        if debug:
            print("Converted to integer values:", x_vals)

        # To track which cells had d_min == 0 for which feature
        zero_distance_hits = []

        # For default label score accumulation
        label_scores = defaultdict(float)

        for f, cells in self.learner.feature_layers.items():
            x_val = x_vals[f]
            if debug:
                print(f"\n-- Processing Feature {f} --")
                print(f"Feature value (int): {x_val}")

            cell_distances = []
            for cell in cells:
                w_ints = [self.processor._from_bin(w_row) for w_row in cell.weightArray]
                d = min(abs(x_val - w) for w in w_ints)
                cell_distances.append((cell, d))
                if debug:
                    print(f"  Cell {cell.index} (label: {self.learner.labels_original[cell.index]}):")
                    print(f"    Weights (int): {w_ints}")
                    print(f"    Min distance: {d}")

            min_d = min(d for _, d in cell_distances)

            for cell, d in cell_distances:
                if d == 0:
                    zero_distance_hits.append(cell.index)

            # Default amortized scoring
            for cell, d in cell_distances:
                score = 1.0 if d == min_d else 0.0
                label_scores[cell.index] += score
                if debug and score > 0:
                    print(f"  >> Cell {cell.index} matched min_d={min_d}, score={score}")

        # Count how many times each cell hit d_min == 0
        hit_counts = Counter(zero_distance_hits)
        max_hits = max(hit_counts.values(), default=0)

        if max_hits > 1:
            # We have one or more cells with d_min == 0 across multiple features
            top_cells = [idx for idx, cnt in hit_counts.items() if cnt == max_hits]
            if debug:
                print(f"\n>>> Dominant cells with d_min==0: {top_cells} (occurrences: {max_hits})")

            probs = np.zeros(len(self.learner.labels_original))
            for idx in top_cells:
                probs[idx] = 1.0 / len(top_cells)
        else:
            # Fallback to normalized label scores
            total_score = sum(label_scores.values())
            probs = np.zeros(len(self.learner.labels_original))
            if total_score > 0:
                for idx, sc in label_scores.items():
                    probs[idx] = sc / total_score

        # Prediction
        if self.classification:
            pred = self.learner.labels_original[np.argmax(probs)]
        else:
            pred = float(np.dot(probs, self.learner.labels_original))
            
            # Apply label dequantization for regression
            if hasattr(self.learner, 'label_scale'):
                pred = (pred - self.learner.label_offset) * self.learner.label_scale
        
        if debug:
            print("\n=== Prediction Summary ===")
            print("Label scores:", dict(label_scores))
            print("Probabilities:", probs)
            print("Associated raw labels:", self.learner.labels_original)
            if hasattr(self.learner, 'label_scale'):
                print("Label scale:", self.learner.label_scale)
                print("Label offset:", self.learner.label_offset)
                print("Dequantized labels:", 
                    [(l - self.learner.label_offset) * self.learner.label_scale
                    for l in self.learner.labels_original])
            print("Final prediction:", pred)
        
        return {
            'probabilities': probs,
            'prediction': pred
        }

if __name__ == "__main__":
    print("=== Testing QBMCActivator ===")
    
    # Test data from qbmc.pdf (classification)
    X_train_class = np.array([
        [0, 1, 3, 5, 7, 8],   # Feature 1
        [0, 0, 1, 0, 1, 1]     # Feature 2
    ]).T
    y_train_class = np.array([0, 0, 1, 0, 1, 1])
    X_test_class = np.array([
        [2, 4, 6],  # New X values
        [1, 0, 1]    # Corresponding Y indicators
    ]).T
    
    # ===== Test 1: Basic Classification =====
    print("\nTest 1: Binary Classification")
    clf_learner = QBMCLearner()
    clf_learner.fit(X_train_class, y_train_class)
    
    activator = QBMCActivator(clf_learner, True)
    predictions = activator.predict(X_test_class, debug=False)
    
    print("Test Samples:\n", X_test_class)
    print("Predictions:", predictions)
    
    # ===== Test 2: Regression =====
    print("\nTest 2: Regression")
    X_reg = np.array([
        [1, 2, 3, 5, 6, 8],   # Feature 1
        [2, 4, 6, 10, 12, 16]  # Feature 2
    ]).T
    y_reg = np.array([5, 7, 9, 13, 15, 19])
    
    reg_learner = QBMCLearner()
    reg_learner.fit(X_reg, y_reg)
    reg_activator = QBMCActivator(reg_learner)
    
    test_reg = np.array([
        [4, 7],  # Between training samples
        [6, 12]  # Exact match to training
    ])
    reg_preds = reg_activator.predict(test_reg, debug=False)
    
    print("Test Values:\n", test_reg)
    print("Predictions:", reg_preds)

    # ===== Test 3: Mixed-Type General Test =====
    print("\nTest 3: Mixed Data Types")
    X_mixed = np.array([
        [0.0, 1, 3.1, 5.2],  # Float and int
        [0, 0.5, 1.1, 0.7]    # Float values
    ]).T
    y_mixed = np.array([0, 0.1, 1.3, 2.6])  # Regression
    
    mixed_learner = QBMCLearner()
    mixed_learner.fit(X_mixed, y_mixed)
    mixed_activator = QBMCActivator(mixed_learner)
    
    test_mixed = np.array([
        [2, 1.1],  # Between samples
        [3.1, 1.1] # Exact match
    ])
    mixed_preds = mixed_activator.predict(test_mixed, debug=False)
    
    print("Test Values:\n", test_mixed)
    print("Predictions:", mixed_preds)


    # ===== Test 4: qbmc.pdf Classification Example =====
    print("\nTest 4: qbmc.pdf Classification Example")
    X_example = np.array([
        [0, 1, 2, 3, 2, 1],     # X1 
        [1, 3, 4, 6, 7, 9],     # X2
    ]).T
    y_example = np.array([0, 0, 0, 1, 1, 1])  # Classification
    
    example_learner = QBMCLearner()
    example_learner.fit(X_example, y_example)
    example_activator = QBMCActivator(example_learner, True)
    
    test_example = np.array([
        [-1, 0, 1, 2, 3, 4],   # X1 test values
        [0, 8, 6, 5, 7, 8]     # X2 test values
    ]).T
    example_preds = example_activator.predict(test_example, debug=False)
    
    print("Test Values:\n", test_example)
    print("Predictions:", example_preds)

    # ===== Test 5: qbmc.pdf Regression Example =====
    print("\nTest 5: qbmc.pdf Regression Example")
    X_example = np.array([
        [0, 1, 2, 3, 2, 1],     # X1 
        [1, 3, 4, 6, 7, 9],     # X2
    ]).T
    y_example = np.array([1, 3, 5, 12, 11, 9])  # Regression
    
    example_learner = QBMCLearner()
    example_learner.fit(X_example, y_example)
    example_activator = QBMCActivator(example_learner, classification=True)
    
    test_example = np.array([
        [-1, 0, 1, 2, 3, 4],   # X1 test values
        [0, 8, 6, 5, 7, 8]     # X2 test values
    ]).T
    example_preds = example_activator.predict(test_example, debug=False)
    
    print("Test Values:\n", test_example)
    print("Predictions:", example_preds)

    # ===== Test 6: Real Regression Example =====
    print("\nTest 6: Real Regression Example")
    X_example = np.array([
        [0, 1, 2, 3, 2, 1],     # X1 
        [1, 3, 4, 6, 7, 9],     # X2
    ]).T
    
    def f(x):
        return 2 * x[0] + 3 * x[1] + 5 + random.uniform(-1, 1)
    
    y_example = np.array([f(x) for x in X_example])  # Regression
    
    example_learner = QBMCLearner()
    example_learner.fit(X_example, y_example)
    example_activator = QBMCActivator(example_learner)
    
    test_example = np.array([
        [0, 1, 2, 3, 4],   # X1 test values
        [8, 6, 5, 7, 8]     # X2 test values
    ]).T
    real_preds = np.array([f(x) for x in test_example])
    example_preds = example_activator.predict(test_example, debug=True)

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import r2_score
    lr = LinearRegression()
    lr.fit(X_example, y_example)
    lr_preds = lr.predict(test_example)

    print("\nActual:", real_preds)
    print("Linear Regression Predictions:", lr_preds)
    print("MSE:", mean_squared_error(real_preds, lr_preds))
    print("R2 Score:", r2_score(real_preds, lr_preds))

    print("As for the QBMCActivator predictions, they are:")
    print("Predictions:", example_preds)
    print("MSE:", mean_squared_error(real_preds, example_preds))
    print("R2 Score:", r2_score(real_preds, example_preds))
    
    print("\n=== All QBMCActivator tests passed ===")
