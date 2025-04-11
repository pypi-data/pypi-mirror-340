from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="RC23104UNO",
    version="0.1.3",
    author="Stanley Ramirez",
    author_email="stanleyramirez087@gmail.com",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stan23rzc/RC23104UNO.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
    ],
)