from setuptools import setup

setup(
    name="nk10",
    version="1.0.0",
    py_modules=["nk10"],
    author="blueradiance",
    author_email="none@example.com",
    description="Unicode Hangul base-10000 numeric compression",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dzbuit/nk10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
