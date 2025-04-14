from setuptools import setup, find_packages

setup(
    name="fibcrypt",
    version="0.1.0",
    description="A fast Fibonacci-based cryptographic toolkit",
    author="Hakan Damar",
    author_email="hakan.damar@linux.com",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.19.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography"
    ],
)
