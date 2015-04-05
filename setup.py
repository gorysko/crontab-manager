"""Setup module."""

from src.utils import read
from setuptools import setup

setup(
    name='cron tab manager',
    version='0.0.1',
    author='Igor Lushchyk',
    author_email='gorysko@gmail.com',
    description=('Crontab manager'),
    license='BSD',
    keywords='',
    url='',
    packages=['src'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
