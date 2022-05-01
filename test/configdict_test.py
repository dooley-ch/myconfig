# *******************************************************************************************
#  File:  configdict_test.py
#
#  Created: 01-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  01-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import pytest
from pathlib import Path
from myconfig import config_load
from myconfig.errors import ConfigFolderError


# --- Folder

def test_valid_folder():
    assert config_load('config')


def test_invalid_folder():
    with pytest.raises(ConfigFolderError):
        assert config_load('wrong_config')


# -- Core file

def test_core_file():
    cfg = config_load(Path('config'))
    assert cfg

    version = cfg.get('version')
    assert version == '1.0.1'


# -- Include files

def test_include_file():
    cfg = config_load(Path('config'))
    assert cfg

    data = cfg.section('db').get('port')
    assert data == 3306

    with pytest.raises(ValueError):
        cfg.get('logging')


# -- Override files

def test_override_file():
    cfg = config_load(Path('config'))
    assert cfg

    database = cfg.section('db').get('database')
    assert database == 'demo-dev'


# -- Command line overrides

def test_command_line_overrides():
    cfg = config_load(Path('config'), overrides={'db': 'db-test'})
    assert cfg

    database = cfg.section('db').get('database')
    assert database == 'demo-test'


# -- Secrets

def test_secrets():
    cfg = config_load(Path('config'), overrides={'db': 'db-test'}, secrets='secrets')
    assert cfg

    database = cfg.section('db').get('database')
    assert database == 'demo-test'

    user = cfg.section('db').get('user')
    assert user == 'root'

    password = cfg.section('db').get('password')
    assert password == 'root*347'
