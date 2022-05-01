# *******************************************************************************************
#  File:  setup.py
#
#  Created: 29-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  29-04-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"


from setuptools import setup, find_packages

setup(
    name='myconfig',
    description='A package to support the use of toml in the configuration of an application',
    version='0.0.1',
    author='James Dooley',
    author_email='james@dooley.ch',
    packages=find_packages(exclude=('test',)),
    url='https://github.com/dooley-ch/myconfig'
)
