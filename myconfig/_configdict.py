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

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['ConfigDict', 'ConfigDictQuery']

from typing import Any
from .errors import SectionNotFound


class ConfigDictQuery:
    _data: dict[str, Any]
    _section_names = list[str]

    def __init__(self, data: dict[str, Any], section_name: str) -> None:
        self._data = data
        self._section_names = list()
        self._section_names.append(section_name)

    def section(self, section_name: str) -> 'ConfigDictQuery':
        self._section_names.append(section_name)
        return self

    def get(self, key: str, default: Any | None = None) -> Any | None:
        data: dict[str, Any] = self._data

        for name in self._section_names:
            if name in data:
                data = data[name]
            else:
                raise SectionNotFound(f"Section not found: {name}")

        return data.get(key, default)


class ConfigDict:
    _data: dict[str, Any]

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def section(self, name: str) -> ConfigDictQuery:
        return ConfigDictQuery(self._data, name)

    def get(self, name: str, default_value: Any | None = None) -> Any:
        data = self._data.get(name, default_value)

        if data is not None:
            if isinstance(data, dict):
                raise ValueError(f"Get can't return a section ({name})")

        return data

    @property
    def data(self) -> dict[str, Any]:
        return self._data
