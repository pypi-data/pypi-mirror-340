import cv2
import numpy as np
from .detector import FaceDetector

def blur_faces(image: np.ndarray, blur_depth: int = 75):
    """
    Blurs detected faces in the input image using MTCNN and Gaussian Blur.

    Parameters:
        image (np.ndarray): The input image in BGR format.
        blur_depth (int): Intensity of the Gaussian blur. Default is 75.

    Returns:
        np.ndarray: The image with blurred faces.
        str: Error message if no image or faces are detected.
    """
    if image is None or image.size == 0:
        return "Image not found"

    detector = FaceDetector()
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb_image)

    if not faces:
        return "No faces detected"

    for face in faces:
        x, y, w, h = face['box']
        roi = rgb_image[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(roi, (47, 47), blur_depth)
        rgb_image[y:y+h, x:x+w] = blurred

    return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
