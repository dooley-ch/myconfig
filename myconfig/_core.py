# *******************************************************************************************
#  File:  _core.py
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
__all__ = ['config_load']

from pathlib import Path
from os import getcwd
from typing import Any
import tomli
from .errors import *
from ._configdict import ConfigDict


def _get_config_folder(folder: str | Path | None = None) -> Path:
    """
    This function determines the path to the config folder
    :param folder: The proposed config folder
    :return: A valid folder
    """

    # If no folder is provided, then default to a config folder located in the working directory
    if folder is None:
        folder = Path(getcwd()).joinpath('config')

    # if the folder was passed as a string, create a Path object
    if isinstance(folder, str):
        folder = Path(folder)

    if folder.exists():
        return folder

    raise ConfigFolderError(f"Config folder not found: {folder.resolve()}")


def _load_config_file(file: Path) -> dict[str, Any]:
    """
    This function loads and parses a toml file
    :param file: the qualified file name to load
    :return: A dictionary based on the toml file loaded
    """
    if not file.exists():
        raise ConfigFolderError(f"Configuration file not found: {file.resolve()}")
    with file.open('rb') as f:
        return tomli.load(f)


def config_load(config_folder: str | Path | None = None, overrides: dict[str, str] | None = None,
        secrets: str | Path | None = None) -> dict[str, Any]:
    """
    This function populates a ConfigParser based on the configuration information stored in the
    config_folder in toml format
    :param config_folder: The folder where the configuration information is stored
    populate the ConfigParser
    :param overrides: This list of overrides replace andy defined in the core config file
    :param secrets:
    :return: A populated ConfigParser object
    """
    config_folder = _get_config_folder(config_folder)
    if overrides is None:
        overrides = dict()

    core = _load_config_file(config_folder.joinpath('core.toml'))

    # Compose the final toml contents
    composition = core.get('composition')
    if composition:
        # Add include files
        files = composition.get('includes')
        if files:
            for name in files:
                file = config_folder.joinpath(f"{name}.toml")
                data = _load_config_file(file)

                core[name] = data

        # Apply override files
        file_overrides: dict[str, Any] = composition.get('overrides')
        if file_overrides:
            for name, file_name in file_overrides.items():
                if name in overrides:
                    continue

                file = config_folder.joinpath(f"{file_name}.toml")
                data = _load_config_file(file)

                current_data: dict[str, Any] = core.get(name)
                current_data.update(data)

        # Apply command line override files
        if overrides:
            for name, file_name in overrides.items():
                file = config_folder.joinpath(f"{file_name}.toml")
                data = _load_config_file(file)

                current_data: dict[str, Any] = core.get(name)
                current_data.update(data)

        # Apply secrets
        if secrets:
            file = config_folder.joinpath(f"{secrets}.toml")
            data = _load_config_file(file)

            for name, data in data.items():
                current_data: dict[str, Any] = core.get(name)
                if current_data:
                    current_data.update(data)

    return ConfigDict(core)
