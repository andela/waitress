import os
from setuptools import setup, find_packages

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='Waitress',
    version='1.0',
    description='Waitress',
    author='Waitress Andela',
    author_email='waitress-andela@mailserver.com',
    url='http://www.python.org/sigs/distutils-sig/',
    packages=find_packages(),
    include_package_data=True,
)
