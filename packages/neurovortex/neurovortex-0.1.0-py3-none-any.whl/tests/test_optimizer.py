import unittest
from neurovortex import AIOptimizer

class TestAIOptimizer(unittest.TestCase):
    def test_optimize_model(self):
        optimizer = AIOptimizer(model="dummy_model")
        optimized_model = optimizer.optimize_model()
        self.assetEqual(optimized_model, "dummy_model")

if __name__ == "__main__":
    unittest.main()