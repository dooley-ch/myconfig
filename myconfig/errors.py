# *******************************************************************************************
#  File:  errors.py
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
__all__ = ['ConfigFolderError', 'SectionNotFound']


class _MyConfigError(Exception):
    """
    This is the base class for all custom error classes used by the package
    """
    pass


class ConfigFolderError(_MyConfigError):
    """
    This error is raised when there is an issue with the folder where the configuraiton information should be
    found, typically the following:
    - Folder not found
    - Core config file not found
    - Missing content files
    """
    pass


class SectionNotFound(_MyConfigError):
    """
    This error is rasied when a requsted section is not defined in the provided configuration information
    """
    pass
