import cv2
from blurthefaces import blur_faces

image = cv2.imread("sample.jpg")
result = blur_faces(image, blur_depth=60)

if isinstance(result, str):
    print("⚠️", result)
else:
    cv2.imwrite("output.jpg", result)
    print("✅ Face blur complete!")
