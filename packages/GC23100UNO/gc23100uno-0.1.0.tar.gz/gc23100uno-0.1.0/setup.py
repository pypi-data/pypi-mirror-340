from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GC23100UNO",
    version="0.1.0",
    author="gc23100",
    author_email="gc23100@example.com",
    description="Libreria de metodos numericos para resolucion de ecuaciones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gc23100/GC23100UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.19.0",
    ],
    include_package_data=True
)
