from setuptools import setup, find_packages

setup(
    name='CM23137UNO',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='tu.email@dominio.com',
    url='https://github.com/tu_usuario/ecuaciones_solver',
    license='MIT', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
