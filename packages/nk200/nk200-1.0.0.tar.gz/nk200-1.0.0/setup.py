from setuptools import setup

setup(
    name="nk200",
    version="1.0.0",
    py_modules=["nk200"],
    author="blueradiance",
    author_email="none@example.com",
    description="Unicode-based Base-200,000 numeral encoding system for ultra-high-compression of numbers.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dzbuit/nk200",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
