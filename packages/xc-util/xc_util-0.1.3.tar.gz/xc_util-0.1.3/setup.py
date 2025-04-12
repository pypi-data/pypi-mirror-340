from setuptools import setup, find_packages

setup(
    name="xc-util",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "cryptography>=36.0.0",
    ],
    python_requires=">=3.7",
)