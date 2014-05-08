# Pentoolbox #

## About ##

Pentoolbox (Pentester's toolbox) is a project which goal is to allow penetration tester to quickly retrieve commonly used tools and update them. You can view it as a package manager but which solely purpose is to keep pentetration testing tools up to date (from sources).

## Disclaimer ##

The project has started recently. There's still a lot to do and several bugs.

Pentoolbox has been thought NOT to be started as root. Try not to.
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

### Installing tools ###

Then you'll probably want to install one or more tools:

	python pentoolbox.py install toolName otherToolName

### Updates ###

With time, you'll probably want to update a tool:

	python pentoolbox.py update toolName otherToolName

Or even all the tools at once:

	python pentoolbox.py update-all

### Removing tools ###

To remove a specific tool:

	python pentoolbox.py remove toolName otherToolName

## Licensing ##

See LICENCE file for informations.
