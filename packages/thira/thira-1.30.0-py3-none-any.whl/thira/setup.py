from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install_egg_info import install_egg_info

from thira.installer import install as install_binary
from thira.uninstaller import uninstall as uninstall_binary

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            install_binary()
        except Exception as e:
            print(f"Warning: Failed to install binary during pip install: {e}")

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        try:
            install_binary()
        except Exception as e:
            print(f"Warning: Failed to install binary during pip install: {e}")

class PreUninstallCommand(install):
    def run(self):
        try:
            uninstall_binary()
        except Exception as e:
            print(f"Warning: Failed to uninstall binary: {e}")
        install.run(self)

setup(
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
        'uninstall': PreUninstallCommand,
    },
)
