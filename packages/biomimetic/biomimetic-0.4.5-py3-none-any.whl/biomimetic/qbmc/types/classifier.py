import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.activation import QBMCActivator
from core.learning import QBMCLearner

BINSIZE = 9

class QBMC_Classifier:
    def __init__(self, binsize=BINSIZE, debug=False):
        self.binsize = binsize
        self.debug = debug
        self.learner = None
        self.activator = None
    
    def fit(self, X, y):
        self.learner = QBMCLearner(binsize=self.binsize)
        self.learner.fit(X, y, debug=self.debug)
        self.activator = QBMCActivator(
            learner=self.learner,
            classification=True,
            binsize=self.binsize
        )
    
    def predict(self, X):
        return self.activator.predict(X, debug=self.debug)
    
if __name__ == "__main__":
    import numpy as np
    
    # Sample data
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    y = np.array([1.5, 1.5, 3.5])
    
    # Create and train the regressor
    regressor = QBMC_Classifier(debug=True)
    regressor.fit(X, y)
    
    # Make predictions
    predictions = regressor.predict(X)
    print(f"Predictions: {predictions}")
