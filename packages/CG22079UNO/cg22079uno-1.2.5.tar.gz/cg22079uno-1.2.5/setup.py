from setuptools import setup, find_packages

setup(
    name="CG22079UNO",
    version="1.2.5",
    author="Gloria Elena Castellanos Garcia",
    author_email="CG22070@ues.edu.sv",
    description="Librería para resolver sistemas de ecuaciones con métodos numéricos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/CG22079UNO",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
