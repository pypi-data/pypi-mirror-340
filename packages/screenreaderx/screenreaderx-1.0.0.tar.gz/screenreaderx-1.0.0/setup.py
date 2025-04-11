from setuptools import setup, find_packages

setup(
    name="screenreaderx",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "easyocr",
        "pytesseract",
        "pyautogui",
        "opencv-python",
        "numpy",
        "Pillow"
    ],
    entry_points={
        'console_scripts': [
            'screenreaderx = screenreaderx.__main__:main'
        ]
    },
    author="Ruzgar",
    description="Advanced screen OCR reader with CLI support",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruzgar/screenreaderx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)