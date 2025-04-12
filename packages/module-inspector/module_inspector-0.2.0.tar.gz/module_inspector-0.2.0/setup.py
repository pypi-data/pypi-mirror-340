# setup.py
from setuptools import setup, find_packages

setup(
    name="module-inspector",
    version="0.2.0",
    author="Luong Nguyen Thanh",
    author_email="ph.ntluong95@gmail.com",
    description="A utility package to inspect imported packages and their aliases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ntluong95/module-inspector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
