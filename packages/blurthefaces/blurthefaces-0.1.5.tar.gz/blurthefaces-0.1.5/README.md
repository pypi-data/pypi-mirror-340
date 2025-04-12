# blurthefaces

A Python package to blur faces in images using MTCNN and OpenCV.

## 🔒 About

BlurTheFaces is primarily focused on protecting people's privacy in images by automatically detecting and blurring facial features.

## 📦 Installation

```bash
pip install blurthefaces
```

## 🚀 Usage

```python
import cv2
from blurthefaces import blur_faces

image = cv2.imread("photo.jpg")
blurred = blur_faces(image, blur_depth=75)
cv2.imwrite("output.jpg", blurred)
```

## 📫 Contact

Author: Harichselvam
Email: harichselvamc@gmail.com
GitHub: harichselvamc