from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="RF23006UNO",
    version="0.1.1",
    author="Enrique Guillermo Rivera Flores",
    author_email="rf23006@ues.edu.sv",
    description="Librería de métodos numéricos para resolver sistemas de ecuaciones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enrique281104/RF23006UNO",
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