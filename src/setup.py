"""
setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from codecs import open
import os
from setuptools import setup
import sys
import warnings


# Don't import AP module here, since deps may not be installed
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ap_python_sdk'))
# from version import VERSION

install_requires = []

# To use a consistent encoding
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if sys.version_info < (2, 7):
    warnings.warn(
        'Alternative Payments library is tested against python 2.7+.'
        'Please use appropriate version so everything works as expected.',
        DeprecationWarning)

install_requires.append('requests >= 0.8.8')

setup(
    name='ap_python_sdk',
    version='0.0.3',
    description='SDK for python application to use Alternative Payments',
    long_description=long_description,

    url='https://github.com/AlternativePayments/ap-python-sdk',

    author='Marjan Stojanovic',
    author_email='marjan.stojanovic90@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='alternative payments python sdk development',
    install_requires=install_requires,
    package_data={},
    packages=['ap_python_sdk'],
    data_files=[],
    
)
