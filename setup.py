import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyrfc6266",
    version="1.0.0",
    author="Anders Jensen",
    author_email="andersandjensen@gmail.com",
    description="RFC6266 implementation in Python",
    license="MIT",
    url="https://github.com/JohnDoee/pyrfc6266",
    py_modules=["pyrfc6266"],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        "pyparsing~=3.0.7",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
)