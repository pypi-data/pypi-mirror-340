from setuptools import setup, find_packages

setup(
    name='RS13036UNO',
    version='0.1.0',
    author='Brayan Fernando Ramírez Salinas',
    author_email='rs13036@ues.edu.sv',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
