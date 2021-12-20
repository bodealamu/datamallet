from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="datamallet",
    version="0.4.2",
    description="Helper tools for the data science workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Olabode Alamu",
    author_email="",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["datamallet", "datamallet.tabular", "datamallet.visualization"],
    include_package_data=True,
    install_requires=['pandas>=1.1.5',
                      'scikit-learn>=0.24.2',
                      'numpy>=1.19.5',
                      'scipy==1.5.4',
                      'plotly>=5.3.1']
)