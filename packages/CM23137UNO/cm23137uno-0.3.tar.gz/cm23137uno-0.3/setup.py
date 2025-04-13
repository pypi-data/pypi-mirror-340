# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='CM23137UNO',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Manuel Carballo',
    author_email='CM23137@ues.edu.sv',
    license='MIT', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
