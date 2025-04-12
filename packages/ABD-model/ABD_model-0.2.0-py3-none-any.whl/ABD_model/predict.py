import torch
import cv2
import os
from pathlib import Path

def get_model_path():
    """
    Returns the full path to the ABD.pt model file bundled with the package.
    """
    return os.path.join(os.path.dirname(__file__), "ABD.pt")

def load_model():
    """
    Load the YOLOv8 model from the local ABD.pt file included in the package.
    """
    weights_path = get_model_path()

    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights not found at: {weights_path}")

    model = torch.hub.load('ultralytics/yolov8', 'custom', path=weights_path, force_reload=False)
    return model

def predict_image(model, image_path):
    """
    Run prediction on the given image using the YOLOv8 model.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    results = model(image_path)
    results.print()
    results.show()
    return results

def run_model(image_path):
    """
    Full pipeline: load model and run prediction.
    """
    model = load_model()
    results = predict_image(model, image_path)
    return results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Predict atoms and bonds from a molecular image.")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the image (.png, .jpg, etc.)")

    args = parser.parse_args()

    try:
        run_model(args.input_path)
    except Exception as e:
        print(f"Error: {e}")
