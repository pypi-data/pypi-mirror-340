from mtcnn import MTCNN

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def detect_faces(self, image):
        return self.detector.detect_faces(image)
