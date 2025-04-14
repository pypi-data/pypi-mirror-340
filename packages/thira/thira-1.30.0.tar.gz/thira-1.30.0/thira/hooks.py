from typing import Any
from poetry.plugin.plugin import Plugin
from poetry.poetry import Poetry
from poetry.utils.env import SystemEnv
from . import installer

class ThiraPlugin(Plugin):
    def activate(self, poetry: Poetry, io: Any) -> None:
        try:
            io.write_line("Installing Thira binary...")
            installer.install()
            io.write_line("Thira binary installation completed")
        except Exception as e:
            io.write_error(f"\nWarning: Failed to install Thira binary: {e}")
