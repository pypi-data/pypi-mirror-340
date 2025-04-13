from setuptools import setup, find_packages

setup(
    name='MS23056UNO',
    version='0.1.1',
    author='Moises Jonathan Martinez Saravia',
    author_email='ms23056@ues.edu.sv',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MOiUES23/MS230565UNO',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy'],
    
)