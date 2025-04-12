# setup.py
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='DM23004UNO',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',  # Añade cualquier dependencia adicional
    ],
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Marvin',
    author_email='dm23004@ues.edu.sv',
    url='https://github.com/DM23004/DM23004UNO',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
