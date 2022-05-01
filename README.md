# MyConfig

![Splash](splash.jpg)

## Introduction

This package supports the provision of application configuration information via toml files.  The main features are:

- Allows for the composition of the final configuration information based on files stored in the config folder
- Allows for the overwriting of data stored in the main file via a selection of supporting files
- Allows for the overwriting of data via a load parameter
- Stores confidential information is a seperate file that is applied to the final configuration data as a last step.

## Installation

The package can be installed from Github via the following command:

```
pip install git+https://github.com/dooley-ch/myconfig
```

## Config Structure

The configuration information is stored in a series of files that are assempled into a single configuration dictionary
for use by the application.

### Configuration Folder

All the configuration files need to be stored in a single folder and by convention this folder is called config and
is located of the current working foder.  The location of this folder can be overritten by passing a variable to the 
loading function indicating that the fold is located else where.

### Core File

The package relies on a main file called core.toml, this file has two functions:

- Provides the bulk of the information needed to configure an application
- It indicates how the final configuration must be constructed.

The section that defines how the configuration is constructed is called 'composition' and looks like this:

```
    [composition]
        includes = ['logging', 'db']
        overrides = {db = 'db-dev'}
```
The section has two entries, one called 'includes', which tells the package which files need to be included in the
final configuration data object.  And one called 'overrides' which tells the package how to override the contents of
existing sections.

### Include Files

The package is designed to take a list of files, load then and include then into the final configuraton as a section 
under the name provided.  The package takes the list of files provided by the 'includes' property as described above 
and iterates over them.  For each name provided, the package finds a file with that name and the toml extension in the 
config folder and if found loads the file into a section of the same name in the final configuration.

### Overwrite Files

In addition to handling include files the package also supports overrite files.  The package takes the overrides 
describe above and tries to file with the value given in the dictionary in the config folder.  If the exists it is
loaded and used to update a section in the configuraton information with the name of the key provided by the overrite
collection.

### Parameter Override

In addition to the overwrite files, the package is capable of dynamically loading overwrite files at runtime via a 
parameter of the load function.

```python
    def config_load(config_folder: str | Path | None = None, overrides: dict[str, str] | None = None,
            secrets: str | Path | None = None) -> ConfigDict:
```
### Secrets 

When composing the configuration information the last step is to apply the contents of the secrets file to the sections
in the final composition.  The package searches for a file called secrets.toml in the config folder and if found it is 
loaded and applied to the final composition.  The secrets file contains a series of entries using the same section names.
The package iterates over them and does an update of each section in the composition using the contents of the secrets
file.

For example, the following enter for the database credentials would be defined in the secrets file:

```
    [db]
    user = 'root'
    password = 'root*347'
```

## Usage

Once the package has been installed in the application, the next step is to import the package:

```python
import myconfig
```
or 
```python
from myconfig import config_load, ConfigDict
```

To obtain the config information in the application make a call to the function:

```python
def config_load(config_folder: str | Path | None = None, overwrites: dict[str, str] | None = None,
            secrets: str | Path | None = None) -> ConfigDict:
```

The function takes the following parameters:

| Parameter     | Data Type            | Default | Comment                                                                                                                                                                        |
|---------------|----------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| config_folder | str or Path or None  | None    | The name of the folder where the config information is stored.  If None, the package tries to load the config information from the config folder located in the working folder |
| overwrites    | dict[str, str]       | None    | A dictionary containing the parameterised overwrites                                                                                                                           |
| secrets       | str or Path  or None | None    | The name of an alternative secrets file to use.  If None, the package searches for a file called secrets.toml located inthe config folder                                      |

The test script contains example of how to call the function.

## Example

A very common use case is to define the database connection and to overwrite it in running the test suite. The first 
step is to indicate the package that the database details must be included in the final composition.  This is done by
indicating that the database definition must be included in the compostion.  This is done by adding the instruction to
the composition secton in the core.toml file:

```
    [composition]
        includes = ['logging', 'db']
        overrides = {db = 'db-dev'}
```

The instruction to load the db files is listed in the includes attributed and so the following will be included in the
final composition:

```
    host = '127.0.0.1'
    port = 3306
    user = 'user'
    password = 'password'
    database = 'demo-prod'
```

so at this point the entry will looks like this:

```
    [db]
    host = '127.0.0.1'
    port = 3306
    user = 'user'
    password = 'password'
    database = 'demo-prod'
```

The next step is to switch to the development database, this is done by providing an overwrite instucion through the 
composition section in the core file.  Once that step is applied the entry looks like this:

```
    [db]
    host = '127.0.0.1'
    port = 3306
    user = 'user'
    password = 'password'
    database = 'demo-dev'
```

The final step is to apply the secrets file in order to provide the correct connection details.  After this the entry
will look like this:

```
    [db]
    host = '127.0.0.1'
    port = 3306
    user = 'dev-user'
    password = 'dev-password'
    database = 'demo-dev'
```

## Security

To protect your secrets, don't check it into version control.