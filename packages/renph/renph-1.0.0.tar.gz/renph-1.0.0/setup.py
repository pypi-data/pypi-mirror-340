from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="renph",
    version="1.0.0",
    author="Avinion",
    author_email="shizofrin@gmail.com",
    description="Tool for batch renaming files by removing square brackets content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://x.com/Lanaev0li",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "phren=phren.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)