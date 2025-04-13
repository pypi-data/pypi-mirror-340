from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="HA23039UNO",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/HA23039UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)