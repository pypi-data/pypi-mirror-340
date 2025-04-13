import unittest
from neurovortex.model_loader import detect_model_format

class TestModelLoader(unittest.TestCase):
    def test_detect_model_format(self):
        self.assertEqual(detect_model_format("model.onnx"), "onnx")
        self.assertEqual(detect_model_format("model.pth"), "pytorch")
        self.assertEqual(detect_model_format("model.h5"), "keras")
        self.assertEqual(detect_model_format("model.pb"), "tensorflow")
        self.assertEqual(detect_model_format("model.tflite"), "tflite")
        self.assertEqual(detect_model_format("model.pt"), "pytorch")
        self.assertEqual(detect_model_format("model.ckpt"), "pytorch")
        self.assertEqual(detect_model_format("unknown_model.format"), "Unknown Format")

if __name__ == "__main__":
    unittest.main()