from setuptools import setup, find_packages

setup(
    name='sistemas_ecuaciones',  
    version='1.0.0',  # 
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),  # Lee la documentación desde el README
    long_description_content_type='text/markdown',
    author='Balmore',
    author_email='LR20029@ues.edu.sv',
    packages=find_packages(),  # Encuentra automáticamente los paquetes en la estructura
    install_requires=[
        'numpy',  # Dependencias necesarias
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python
)
