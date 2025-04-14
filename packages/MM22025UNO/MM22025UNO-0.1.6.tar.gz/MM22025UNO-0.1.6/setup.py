from setuptools import setup, find_packages

setup(
    name='MM22025UNO',
    version='0.1.6',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'scipy',
    ],
    author='Roberto Mena',
    author_email='mm22025@ues.edu.sv',
    description='Librería para resolver sistemas de ecuaciones lineales y no lineales',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Robertmez03/MM22025UNO',
    license="MIT", 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)