import os
import logging

def detect_model_format(file_path):
    """
    Detect the model format based on the file extension.

    Args:
        file_path (str): Path to the model file.

    Returns:
        str: Detected model format.
    """
    _, file_extension = os.path.splitext(file_path)
    format_mapping = {
        '.ckpt': 'TensorFlow Checkpoint',
        '.h5': 'Keras HDF5',
        '.pth': 'PyTorch',
        '.pt': 'PyTorch',
        '.onnx': 'ONNX',
        '.pb': 'TensorFlow Protocol Buffer',
        '.tflite': 'TensorFlow Lite',
        '.model': 'Generic Model File',
    }

    return format_mapping.get(file_extension.lower(), 'Unknown Format')

def load_model(file_path):
    """
    Load a model based on its format.

    Args:
        file_path (str): Path to the model file.

    Returns:
        object: Loaded model instance.
    """
    logger = logging.getLogger(__name__)
    model_format = detect_model_format(file_path)
    logger.info(f"Detected model format: {model_format}")

    try:
        if model_format == 'TensorFlow Checkpoint':
            import tensorflow as tf
            logger.info("Loading TensorFlow Checkpoint model...")
            model = tf.keras.models.load_model(file_path)
        elif model_format == 'Keras HDF5':
            import tensorflow as tf
            logger.info("Loading Keras HDF5 model...")
            model = tf.keras.models.load_model(file_path)
        elif model_format == 'PyTorch':
            import torch
            logger.info("Loading PyTorch model...")
            model = torch.load(file_path)
        elif model_format == 'ONNX':
            import onnx
            import onnxruntime as ort
            logger.info("Loading ONNX model...")
            model = onnx.load(file_path)
            # Optional: Create an ONNX Runtime session
            session = ort.InferenceSession(file_path)
            logger.info("ONNX Runtime session created.")
            return model, session
        elif model_format == 'TensorFlow Protocol Buffer':
            import tensorflow as tf
            logger.info("Loading TensorFlow Protocol Buffer model...")
            model = tf.saved_model.load(file_path)
        elif model_format == 'TensorFlow Lite':
            import tensorflow as tf
            logger.info("Loading TensorFlow Lite model...")
            interpreter = tf.lite.Interpreter(model_path=file_path)
            interpreter.allocate_tensors()
            logger.info("TensorFlow Lite model loaded and tensors allocated.")
            return interpreter
        elif model_format == 'Generic Model File':
            logger.warning("Generic model loading is not implemented.")
            raise NotImplementedError("Generic model loading not implemented.")
        else:
            logger.error(f"Unknown model format: {model_format}")
            raise ValueError(f"Unsupported model format: {model_format}")

        logger.info("Model loaded successfully.")
        return model

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

def save_model(model, file_path, model_format):
    """
    Save a model to the specified file path in the given format.

    Args:
        model (object): Model instance to save.
        file_path (str): Path to save the model.
        model_format (str): Format to save the model (e.g., 'PyTorch', 'Keras HDF5').

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Saving model in {model_format} format to {file_path}...")

    try:
        if model_format == 'PyTorch':
            import torch
            torch.save(model.state_dict(), file_path)
        elif model_format == 'Keras HDF5':
            import tensorflow as tf
            model.save(file_path)
        elif model_format == 'ONNX':
            import torch.onnx
            torch.onnx.export(model, torch.randn(1, *model.input_shape), file_path)
        elif model_format == 'TensorFlow Protocol Buffer':
            import tensorflow as tf
            tf.saved_model.save(model, file_path)
        elif model_format == 'TensorFlow Lite':
            import tensorflow as tf
            converter = tf.lite.TFLiteConverter.from_keras_model(model)
            tflite_model = converter.convert()
            with open(file_path, 'wb') as f:
                f.write(tflite_model)
        else:
            logger.error(f"Unsupported model format for saving: {model_format}")
            raise ValueError(f"Unsupported model format: {model_format}")

        logger.info("Model saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save model: {e}")
        raise