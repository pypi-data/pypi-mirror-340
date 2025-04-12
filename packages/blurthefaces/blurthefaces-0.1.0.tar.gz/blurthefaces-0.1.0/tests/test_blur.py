from blurthefaces.blur import blur_faces
import cv2

def test_blur_faces():
    image = cv2.imread("tests/sample.jpg")
    result = blur_faces(image, blur_depth=50)
    assert result is not None
