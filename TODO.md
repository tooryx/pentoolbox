# Dependencies #

For now only aptitude dependencies are handled.
It would be great to be able to handle dependencies such as CPAN.

# Argument system #

The current argument system is counter intuitive.
Typing: `python pentoolbox.py --install -t nmap` is not cool.
The best would be something like: `python pentoolbox.py install nmap`

# Packages #

The package system aims to give users another level of customization over tools.
For example, a custom installation directory, custom symlink and so on.
It would also be cool to be able to download things such as wordlists.

# Configuration files #

What about downloading configuration files from a repository/whatever to
automatically apply the configuration to an installed tool ?
Obviously, this would go in the package section.
