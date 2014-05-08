# Pentoolbox #

## About ##

	         PENTOOLBOX
	 '------------------------'
	  |__ '==' ------ '==' __|
	    |                  |
	    |__________________|

Pentoolbox (Pentester's toolbox) is a project which goal is to allow penetration tester to quickly retrieve commonly used tools and update them. You can view it as a package manager but which solely purpose is to keep pentetration testing tools up to date (from sources).

## Disclaimer ##

The project has started recently. There's still a lot to do and several bugs.

*WARNING*
Some options deletes directories or file. Do not provide a system path as an installation directory.
Also, pentoolbox has been thought NOT to be started as root. Try not to.
If required, a sudo access will be prompted for dependecies install.

## Dependencies ##

Pentoolbox only depends on:

  * python-2.7
  * python-yaml

## How to use ##

For help with options, you can use the `-h` option
Here are some classic usage examples.

### Base configuration ###

First you'll need to create a configuration file.
The best way to do so may be to `cp config.yml.example config.yml` and then manually edit the file to meet your needs.

### Tool install ###

If you wish to install one or more specific packages, you could use the following command line:

`python pentoolbox.py --install -t packageName,otherPackageName`

### Tool update ###

Now if you wish to update one or more installed tools, use the following command:

`python pentoolbox.py --update -t packageName,otherPackageName`

### Update all tools ###

To update all installed packages:

`python pentoolbox.py --update-all`

### Remove a tool ###

For now, there's no automatic way to remove a tool.
You should remove all the directories (real path and symlink) of the tool.
Also you *must* manually edit the ._config file, located at the root of the install directory, and remove the line about the tool you wish to remove.

## Licensing ##

See LICENCE file for informations.
