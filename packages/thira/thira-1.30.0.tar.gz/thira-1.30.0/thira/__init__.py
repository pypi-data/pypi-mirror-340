__version__ = "1.20.0"

def ensure_binary():
    """Ensure the binary is installed."""
    from . import cli
    if not cli.binary.get_binary_path().exists():
        from . import installer
        installer.install()
