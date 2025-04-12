"""
Descripttion:
version:
Author: Mengwei Li
Date: 2025-01-27 16:20:57
LastEditors: Mengwei Li
LastEditTime: 2025-01-27 16:21:05
"""

from setuptools import setup, find_packages
long_description = open("README.md", encoding="utf-8").read() + "\n\n" + open("CHANGELOG.md", encoding="utf-8").read()

setup(
    name="PopComm",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "joblib",
        "matplotlib",
        "networkx",
        "numpy",
        "pandas",
        "scanpy",
        "scikit_learn",
        "scipy",
        "seaborn",
        "statsmodels"
    ],
    author="Mengwei Li",
    author_email="limengwei833@gmail.com",
    description="Population-level cell-cell communication analysis tool",
    url="https://github.com/yourgithub/popcomm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
)