import os
from setuptools import setup, find_packages

__version__ = '0.1'

def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name="{{cookiecutter.app_name}}",
    version=__version__,
    author='Gregory Amorim (gregadc)',
    author_email='adc.greg@gmail.com',
    description="Cookiecutter Flask All-In-One",
    long_description=read_file('README.rst'),
    packages=find_packages(exclude=['tests']),
    install_requires=read_file('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            '{{cookiecutter.app_name}}={{cookiecutter.app_name}}.manage:cli'
        ]
    }
)
