#! /usr/bin/python

# This file is part of pentoolbox.
# Please see LICENSE for details.

from core.Console import Console
from core.Configuration import Configuration
from core.Toolbox import Toolbox
from core.Installer import Installer

# First the output console is loaded.
# This will generate output messages.
console = Console()
console.banner()

# Then the configuration manager.
config = Configuration(console)
config.load_arguments()
config.load_core_config()
config.load_user_config()
config.load_saved_tools()

# We print some information to the screen...
console.dump_config(config)
console.dump_installed_tools(config)

# ...and ensure that's what the user asked for.
if not console.prompt():
	exit(1)

# Then we build the toolbox.
toolbox = Toolbox(config)
toolbox.build()

# We launch the install/update process.
installer = Installer(config, toolbox)
installer.start()

# Finally, we save the current tools in {{install-dir}}/._config
toolbox.save_tools()

# And we properly close the configuration.
config.end()
