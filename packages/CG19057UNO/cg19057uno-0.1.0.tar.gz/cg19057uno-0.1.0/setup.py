from setuptools import setup, find_packages

setup(
    name="CG19057UNO",
    version="0.1.0",
    author="Yaquelin Grijalva",
    author_email="cg19057@ues.edu.sv",
    description="Librería para resolver problemas de ecuaciones lineales y no lineales a través de diferentes métodos numéricos.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
