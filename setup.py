from setuptools import setup, find_packages

EXCLUDE = ["*.tests", "*.tests.*", "tests.*", "tests"]

setup(name='url_shortener',
    version='0.0.1',
    packages=find_packages(exclude=EXCLUDE),
    url='https://github.com/golgoth/url-shortener',
    install_requires=[])
