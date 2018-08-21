from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='tracker_lib',
    version='1.0',
    author='Darya Novak',
    author_email='daryanovak18@gmail.com',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)