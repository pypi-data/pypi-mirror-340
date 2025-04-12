from setuptools import setup, find_packages

setup(
    name="xjy-util",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "cryptography>=36.0.0",
    ],
    python_requires=">=3.7",
)