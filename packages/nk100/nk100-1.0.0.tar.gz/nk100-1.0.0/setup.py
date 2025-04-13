from setuptools import setup

setup(
    name="nk100",
    version="1.0.0",
    py_modules=["nk100"],
    author="blueradiance",
    author_email="none@example.com",
    description="Layered Unicode base-100000 numeral system using Hangul, Hanja, and CJK extensions.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dzbuit/nk100",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
