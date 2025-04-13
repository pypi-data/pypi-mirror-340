
from setuptools import setup

setup(
    name="thirtykn",
    version="1.0.0",
    py_modules=["thirtykn"],
    author="blueradiance",
    author_email="none@example.com",
    description="30KN: Unicode-based high-compression numeral system combining Hangul and Hanja for 30,000-radix encoding.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blueradiance/30kn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
