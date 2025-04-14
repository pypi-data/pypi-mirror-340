try:
    from importlib.metadata import version
    __version__ = version("thira")
except ImportError:
    import tomli
    from pathlib import Path

    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        __version__ = tomli.load(f)["tool"]["poetry"]["version"]
