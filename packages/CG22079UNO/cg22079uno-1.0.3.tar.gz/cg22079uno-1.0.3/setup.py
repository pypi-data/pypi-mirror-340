from setuptools import setup, find_packages

setup(
    name='CG22079UNO',
    version='1.0.3',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales con métodos numéricos',
    author='Gloria Elena Castellanos Garcia',
    author_email='cg22079@ues.edu.sv',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    entry_points={
    'console_scripts': [
        'cg22079uno=CG22079UNO.main:menu',  # Asegúrate que apunta al archivo y función correctos
    ]
},

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
