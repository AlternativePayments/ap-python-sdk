import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


# Don't import AP module here, since deps may not be installed
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ap_python_sdk'))
# from version import VERSION

install_requires = []

# To use a consistent encoding
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

if sys.version_info < (2, 7):
    warnings.warn(
        'Alternative Payments library is tested against python 2.7+.'
        'Please use appropriate version so everything works as expected.',
        DeprecationWarning)

install_requires.append('requests >= 0.8.8')

setup(
    name='ap_python_sdk',
    version='0.0.6',
    description='SDK for python application to use Alternative Payments',
    long_description=long_description,

     cmdclass={'build_py': build_py},

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
