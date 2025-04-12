"""
Descripttion:
version:
Author: Mengwei Li
Date: 2025-01-27 16:20:57
LastEditors: Mengwei Li
LastEditTime: 2025-01-27 16:21:05
"""

from setuptools import setup, find_packages

setup(
    name="PopComm",
    version="0.1.3",
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
)