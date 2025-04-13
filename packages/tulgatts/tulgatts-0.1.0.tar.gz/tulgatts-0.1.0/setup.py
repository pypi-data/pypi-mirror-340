from setuptools import setup, find_packages
import os

# Use a simple ASCII description without reading README.md to avoid encoding issues
long_description = "TulgaTTS - AI-based TTS library for generating speech with various voices popular in Kazakhstan"

setup(
    name="tulgatts",
    version="0.1.0",
    author="David Suragan",
    author_email="dauitsuragan002@gmail.com",
    description="TulgaTTS is an AI-based TTS library for generating speech with various voices popular in the region of Kazakhstan",
    long_description=long_description,
    long_description_content_type="text/plain",  # Use plain text format
    url="https://github.com/dauitsuragan002/tulgatts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyCharacterAI>=0.2.0",
        "requests>=2.20.0",
        "python-dotenv>=0.10.0",
    ],
    extras_require={
        "audio": ["pygame>=2.0.0"],
    },
    package_data={
        "tulgatts": ["py.typed"],
    },
) 