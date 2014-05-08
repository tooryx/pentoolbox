#! /usr/bin/python

# This file is part of pentoolbox.
# Please see LICENSE for details.

from core.Console import Console
from core.Configuration import Configuration
from core.Toolbox import Toolbox
from core.Installer import Installer

# First we create an output mode.
# This will generates debug and output messages.
console = Console()
console.banner()

# We need to load the configuration.
config = Configuration(console)
config.load_arguments()
config.load_core_config()
config.load_user_config()
config.load_saved_tools()

console.dump_config(config)
console.dump_installed_tools(config)

if not console.prompt():
	exit(1)

# Then we build the toolbox.
toolbox = Toolbox(config)
toolbox.build()

# Finally, we launch the install/update process.
installer = Installer(config, toolbox)
installer.start()

# Before exiting, we add the installed tools to a config file.
# This file is: {{install-dir}}/._config
toolbox.save_tools()
config.end()
