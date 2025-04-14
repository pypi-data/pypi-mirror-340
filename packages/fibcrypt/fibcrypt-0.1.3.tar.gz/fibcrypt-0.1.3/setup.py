from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fibcrypt",
    version="0.1.3",
    description="A fast Fibonacci-based cryptographic toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hakan Damar",
    author_email="hakan.damar@linux.com",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.22.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography"
    ],
)
