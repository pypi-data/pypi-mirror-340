from setuptools import setup, find_packages

setup(
    name="image-converter-tool",
    version="1.0.0",
    description="A professional image converter tool built with Python and Tkinter.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=["Pillow"],
    entry_points={
        "console_scripts": [
            "image-converter=src.main:main",
        ],
    },
)