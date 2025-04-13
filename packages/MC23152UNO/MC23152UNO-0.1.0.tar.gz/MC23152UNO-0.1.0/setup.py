from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MC23152UNO",
    version="0.1.0",
    author="Moises Isaac Molina Corado",
    author_email="mc23512@ues.edu.sv",
    description="Librería de métodos numéricos para resolver sistemas de ecuaciones (lineales y no lineales)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moisescorado91",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.0',
    ],
)