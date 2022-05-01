# *******************************************************************************************
#  File:  _configdict.py
#
#  Created: 30-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-04-2022: Initial version
#
# *******************************************************************************************

"""
This module implements the ConfigDict class, and it's supporting query class ConfigDictQuery
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['ConfigDict', 'ConfigDictQuery']

from typing import Any
from .errors import SectionNotFound


class ConfigDictQuery:
    """
    This class is used to query the loaded configuration information.  It allows the developer to drill down into
    sections and query a value
    """
    _data: dict[str, Any]
    _section_names = list[str]

    def __init__(self, data: dict[str, Any], section_name: str) -> None:
        self._data = data
        self._section_names = list()
        self._section_names.append(section_name)

    def section(self, section_name: str) -> 'ConfigDictQuery':
        """
        This method just collects the section names in sequence, adding the names to the section names collection.
        When the get method is called it drills down throuh this list to file the required value
        """
        self._section_names.append(section_name)
        return self

    def get(self, key: str, default: Any | None = None) -> Any | None:
        """
        This method drills down throuh the sections provided via the section method to arrive at the
        required value.
        """
        data: dict[str, Any] = self._data

        for name in self._section_names:
            if name in data:
                data = data[name]
            else:
                raise SectionNotFound(f"Section not found: {name}")

        return data.get(key, default)


class ConfigDict:
    """
    This class acts as a container for the config information loaded from the toml files and allows the developer
    to query the loaded data
    """
    _data: dict[str, Any]

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def section(self, name: str) -> ConfigDictQuery:
        """
        This method kicks of a query by returns an instance of the ConfigDictQuery class populated by the selected
        section name
        """
        return ConfigDictQuery(self._data, name)

    def get(self, name: str, default_value: Any | None = None) -> Any:
        """
        This method returns a value from the root collection of the configuration information
        """
        data = self._data.get(name, default_value)

        if data is not None:
            if isinstance(data, dict):
                raise ValueError(f"Get can't return a section ({name})")

        return data

    @property
    def data(self) -> dict[str, Any]:
        """
        This method provides access to the underlying data collection
        """
        return self._data

    @property
    def logging_config(self):
        """
        If the logging configuration imformation is defined, the method provides access to it
        """
        data = self._data['logging']

        if data is not None:
            if isinstance(data, dict):
                return data

        raise ValueError(f"Logging configuration not found")
