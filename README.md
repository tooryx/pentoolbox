# Pentoolbox #

## About ##

Pentoolbox (Pentester's toolbox) is a project which goal is to allow penetration tester to quickly retrieve commonly used tools and update them. You can view it as a package manager but which solely purpose is to keep pentetration testing tools up to date (from sources).

## Disclaimer ##

The project has started only recently. There's still a lot to do and several bugs. Also, you may find some features a bit restricted.

*WARNING*
Some features actually deletes directories or file. Do not provide a system path as installation directory.
Also, pentoolbox has been though NOT to be started as root.

## How to use ##

A normal use scheme is the following:

  * First, make a copy of config.yml.example to config.yml
  * Edit config.yml to meet your needs
  * You can then launch pentoolbox like this: `python pentoolbox.py --install`

For help with options, you can use the `-h` option

## Licensing ##

See LICENCE file for informations.
