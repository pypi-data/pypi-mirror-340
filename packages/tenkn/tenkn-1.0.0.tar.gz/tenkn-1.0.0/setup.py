
from setuptools import setup

setup(
    name="tenkn",
    version="1.0.0",
    py_modules=["tenkn"],
    author="blueradiance",
    author_email="none@example.com",
    description="10KN: Unicode Hangul-based 10,000-radix numeral system.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dzbuit/10KN",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
