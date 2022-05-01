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


### Parameter Override

## Usage

