# *******************************************************************************************
#  File:  __init__.py
#
#  Created: 29-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  29-04-2022: Initial version
#
# *******************************************************************************************

"""
This package supports the use of toml to provide condiguration information for an application
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['config_load', 'ConfigDict']

from ._core import *
from ._configdict import *
