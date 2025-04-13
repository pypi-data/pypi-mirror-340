from setuptools import setup, find_packages

setup(
    name='CG22079UNO',
    version='1.0.2',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales con métodos numéricos',
    author='Gloria Elena Castellanos Garcia',
    author_email='cg22079@ues.edu.sv',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'cg22079uno=main:menu'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
