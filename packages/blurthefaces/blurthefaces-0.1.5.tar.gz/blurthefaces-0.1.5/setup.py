from setuptools import setup, find_packages

setup(
    name="blurthefaces",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mtcnn",
        "tensorflow",
        "numpy"
    ],
    description="A Python package to blur faces in images using MTCNN and OpenCV.",
    author="Harichselvam",
    author_email="harichselvamc@gmail.com",
    url="https://github.com/harichselvamc/blurthefaces",
    keywords=["face blur", "opencv", "mtcnn", "image processing", "python package"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
