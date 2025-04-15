from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="maxminconquer",
    version="0.1.3",
    packages=find_packages(),
    description="A package to find the max and min values using divide and conquer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GIK",
    author_email="giksecon28@gmail.com",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
