#! /usr/bin/python

# LICENSE

from core.Console import Console
from core.Configuration import Configuration
from core.Toolbox import Toolbox
from core.Installer import Installer

# First we create an output mode.
# This will generates debug and output messages.
console = Console()

# We need to load the configuration.
config = Configuration(console)
config.load_arguments()
config.load_core_config()
config.load_user_config()

console.dump_config(config)

# Then we build the toolbox.
toolbox = Toolbox(config)
toolbox.build()

# Finally, we launch the install/update process.
installer = Installer(config, toolbox)
installer.start()

# Once everything's installed, we clear the config (delete of log file)
config.clean()
