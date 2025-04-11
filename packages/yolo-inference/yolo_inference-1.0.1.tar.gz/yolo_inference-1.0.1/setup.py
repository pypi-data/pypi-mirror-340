from setuptools import setup, find_packages

setup(
    name="yolo_inference",
    version="1.0.1",
    description="YOLO inference library for object detection",
    author="Shubham Nayak",
    author_email="sn85076@outlook.com",
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)