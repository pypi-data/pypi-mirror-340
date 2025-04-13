from setuptools import setup, find_packages

setup(
    name="nku",
    version="1.0.1",
    packages=["nku"],
    author="blueradiance",
    author_email="none@example.com",
    description="Unified controller for NK Unicode numeral systems (nk10, nk20, nk30, nk100, nk200, nk256). Handles compact number encoding and decoding across multiple radices.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dzbuit/nku",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
