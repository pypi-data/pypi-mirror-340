
from setuptools import setup, find_packages

setup(
    name="FF23004UNO",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "scipy"],
    author="Jonathan Fuentes",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    keywords=["gauss", "jacobi", "Descomposición LU","Crammer","Gauss-Jordan","Eliminación de Gauss", "bisección", "sistemas de ecuaciones", "CARNETFF23004"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
