import torch
import cv2
import os
from pathlib import Path

def load_model(weights_path='ABD.pt'):
    """
    Load the YOLOv5 model from the specified weights file.
    """
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=False)
    return model

def predict_image(model, image_path):
    """
    Run prediction on the given image using the YOLOv5 model.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    results = model(image_path)
    results.print()
    results.show()  # Show image with bounding boxes
    return results

def run_model(image_path):
    """
    Complete pipeline: load model, run inference, and return results.
    """
    model = load_model()
    results = predict_image(model, image_path)
    return results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Predict atoms and bonds from a molecular image.")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the image (.png)")

    args = parser.parse_args()
    run_model(args.input_path)
