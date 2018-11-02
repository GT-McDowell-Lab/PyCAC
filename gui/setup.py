# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of PyCAC requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install pycac
This will install the latest version of PyCAC which works on your
version of Python. 
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    
    name='pycac',  # Required
    version='0.2.5',  # Required
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description='Graphical user interface for CAC simulator',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='http://www.pycac.org',  # Optional
    author='Kevin Chu, Alex Selimov, Shuozhi Xu',  # Optional
    author_email='kchu41@gatech.edu',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='concurrent atomistic continuum simulation interface',  # Optional
    
    
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    
    install_requires=['paramiko', 'pyqt5', 'numpy'],  # Optional
    
    package_data={  # Optional
        'pycac': ['template.pbs', 'template.sl', 'icon.png'],
    },
    include_package_data=True,
    
)
