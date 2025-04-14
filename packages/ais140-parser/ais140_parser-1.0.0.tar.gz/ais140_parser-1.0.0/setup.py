# setup.py

from setuptools import setup, find_packages

setup(
    name='ais140-parser',
    version='1.0.0',
    description='AIS140 Protocol Parser',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/knarsing/ais140-parser",
    author='knarsing',
    author_email='narsing.pimple@gmail.com',
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
