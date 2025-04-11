from setuptools import setup, find_packages

setup(
    name="yolo-inference",
    version="1.0.0",
    description="YOLO inference library for object detection",
    author="Shubham Nayak",
    author_email="shubham.nayak@godigit.com",
    url="https://bitbucket.org/godigit/cv_motor_4wclaim_gpuservices",
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