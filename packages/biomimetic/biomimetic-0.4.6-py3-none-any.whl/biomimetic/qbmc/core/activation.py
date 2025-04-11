# qbmc/core/activations.py
import numpy as np
from typing import Dict, List, Union
from .preprocessing import QBMCDataProcessor
from .learning import QBMCLearner

BINSIZE=9

class QBMCActivator:
    def __init__(self, learner: QBMCLearner = None, classification: bool = False, binsize=BINSIZE):
        self.learner = learner
        self.classification = classification
        self.binsize = binsize
        self.processor = QBMCDataProcessor() if learner is None else learner.processor
        
    def predict(self, X: np.ndarray, debug: bool = False) -> np.ndarray:
        X_bin = self.processor.auto_convert(X)
        return np.array([self.forward_pass(x, self.classification, debug)['prediction'] for x in X_bin])

    # def _calculate_matches(self, x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    #     mismatches = weights != x
    #     first_mismatch = np.argmax(mismatches, axis=1)
    #     perfect_matches = np.all(~mismatches, axis=1)
    #     return np.where(perfect_matches, self.learner.binsize, first_mismatch)

    def forward_pass(self, x_bin: np.ndarray, classification: bool = False, debug: bool = False) -> Dict:
        if debug:
            print("\n=== Starting Forward Pass ===")
            print(f"Input binary data:\n{x_bin.astype(int)}")
            print(f"Classification mode: {classification}")

        class_contributions = {}  # Changed from counts to continuous contributions

        # Process each feature independently
        for feature_idx, feature_cells in self.learner.feature_layers.items():
            if debug:
                print(f"\nProcessing Feature {feature_idx}")
                print(f"Input slice: {x_bin[feature_idx].astype(int)}")

            feature_min_distance = float('inf')
            cell_distances = []

            # First pass: calculate distances for all cells
            for cell_idx, cell in enumerate(feature_cells):
                weights = cell.weightArray
                if debug:
                    print(f"\nCell {cell_idx} (class {cell.index}):")
                    print(f"Weights:\n{weights.astype(int)}")

                # Calculate Hamming distance
                distance = np.sum(weights != x_bin[feature_idx])
                
                if debug:
                    print(f"Total mismatches (distance): {distance}")

                cell_distances.append((cell.index, distance))
                
                # Track global minimum for this feature
                if distance < feature_min_distance:
                    feature_min_distance = distance

            if debug:
                print(f"\nFeature {feature_idx} Summary:")
                print(f"Minimum distance: {feature_min_distance}")
                print(f"All cell distances: {cell_distances}")

            # Second pass: calculate contributions based on distance
            for class_idx, distance in cell_distances:
                # Contribution is inverse of relative distance
                if feature_min_distance == 0:
                    # Perfect match case
                    contribution = 1.0 if distance == 0 else 0.0
                else:
                    # Normalized contribution based on relative distance
                    contribution = feature_min_distance / max(distance, 1e-8)  # Avoid division by zero

                # Accumulate contributions across features
                class_contributions[class_idx] = class_contributions.get(class_idx, 0.0) + contribution

        # Normalize contributions to probabilities
        total_contribution = sum(class_contributions.values())
        probabilities = np.zeros(len(self.learner.labels_original))

        for class_idx, contrib in class_contributions.items():
            probabilities[class_idx] = contrib / total_contribution if total_contribution > 0 else 0.0

        if debug:
            print("\n=== Probability Calculation ===")
            print(f"Probabilities: {probabilities}")
            print(f"Associated labels: {self.learner.labels_original}")
        
        # Step 3: Prediction
        if classification:
            prediction = self.learner.labels_original[np.argmax(probabilities)]
            if debug:
                print("\n=== Classification Decision ===")
                print(f"Predicted class: {prediction} (index {np.argmax(probabilities)})")
        else:
            prediction = np.dot(probabilities, self.learner.labels_original)
            if debug:
                print("\n=== Regression Calculation ===")
                print(f"Prediction components:")
                for i, (prob, label) in enumerate(zip(probabilities, self.learner.labels_original)):
                    print(f"  Class {i}: prob={prob:.3f} * label={label} = {prob * label:.3f}")
                print(f"Final prediction: {prediction}")
        
        if debug:
            print("\n=== Forward Pass Complete ===")
        
        return {
            'probabilities': probabilities,
            'prediction': prediction
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
    predictions = activator.predict(X_test_class, debug=True)
    
    print("Test Samples:\n", X_test_class)
    print("Predictions:", predictions)
    assert predictions.shape == (3,), "Should return 3 predictions"
    assert all(p in [0, 1] for p in predictions), "Should predict only class 0 or 1"
    print("✓ Classification prediction verified")
    
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
    reg_preds = reg_activator.predict(test_reg, debug=True)
    
    print("Test Values:\n", test_reg)
    print("Predictions:", reg_preds)
    assert len(reg_preds) == 2, "Should return 2 predictions"
    assert all(5 <= p <= 19 for p in reg_preds), "Should stay within training range"
    print("✓ Regression prediction verified")

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
    mixed_preds = mixed_activator.predict(test_mixed, debug=True)
    
    print("Test Values:\n", test_mixed)
    print("Predictions:", mixed_preds)
    assert len(mixed_preds) == 2, "Should return 2 predictions"
    assert all(0 <= p <= 2.6 for p in mixed_preds), "Should respect training range"
    print("✓ Mixed-type handling verified")


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
    example_preds = example_activator.predict(test_example, debug=True)
    
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
    example_activator = QBMCActivator(example_learner)
    
    test_example = np.array([
        [-1, 0, 1, 2, 3, 4],   # X1 test values
        [0, 8, 6, 5, 7, 8]     # X2 test values
    ]).T
    example_preds = example_activator.predict(test_example, debug=True)
    
    print("Test Values:\n", test_example)
    print("Predictions:", example_preds)
    
    print("\n=== All QBMCActivator tests passed ===")
