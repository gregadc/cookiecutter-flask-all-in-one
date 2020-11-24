import os
from setuptools import setup, find_packages

__version__ = '0.1'

def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name="app",
    version=__version__,
    author="gregadc",
    author_email='adc.greg@gmail.com',
    description="Cookiecutter Flask All-In-One",
    long_description=read_file('README.rst'),
    packages=find_packages(exclude=['tests']),
    install_requires=read_file('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            'app=app.manage:cli'
        ]
    }
)
