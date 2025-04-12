from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vl16008uno",
    version="0.1.0",  # Actualiza con cada nueva versión
    author="Elmer Oswaldo Ventura Lemus",
    author_email="vl16008@ues.edu.sv",
    description="Paquete para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)