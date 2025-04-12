from setuptools import setup, find_packages
import pathlib

# Lee el README automáticamente
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="vl16008uno",
    version="0.1.1",  # ¡Actualiza la versión!
    author="Elmer Oswaldo Ventura Lemus",
    author_email="vl16008@ues.edu.sv",
    description="Paquete para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},  # Opcional si usas estructura src/
    packages=find_packages(where="src"),  # Busca paquetes en src/
    install_requires=[
        "numpy>=1.19.0",
    ],
    python_requires=">=3.6",
    # NUEVOS ELEMENTOS AÑADIDOS:
    include_package_data=True,  # Incluye archivos no-Python
    package_data={
        "vl16008uno": ["*.txt", "*.md"],  # Patrones de archivos a incluir
    },
    entry_points={
        "console_scripts": [
            "vl16008uno-demo=vl16008uno.demo:main",  # Comando CLI
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="numerical-methods linear-equations nonlinear-equations",
    project_urls={
        "Bug Reports": "https://github.com/tuusuario/vl16008uno/issues",
        "Source": "https://github.com/tuusuario/vl16008uno",
    },
)