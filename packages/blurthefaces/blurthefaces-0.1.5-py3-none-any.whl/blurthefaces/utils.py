import numpy as np
import cv2

def decode_image(file_bytes: bytes) -> np.ndarray:
    buffer = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)
