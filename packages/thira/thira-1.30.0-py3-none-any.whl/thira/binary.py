import os
import platform
import sys
from pathlib import Path

def get_binary_name():
    """Get the binary name based on the platform."""
    return "thira.exe" if sys.platform == "win32" else "thira"

def get_arch_name():
    """Get the architecture name."""
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "x86_64"
    elif machine in ["arm64", "aarch64"]:
        return "arm64"
    raise ValueError(f"Unsupported architecture: {machine}")

def get_platform_name():
    """Get the platform name."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "darwin"
    elif system == "linux":
        return "linux"
    raise ValueError(f"Unsupported platform: {system}")

def get_archive_name():
    """Get the archive name based on platform and architecture."""
    prefix = "thira"
    platform_name = get_platform_name()
    arch = get_arch_name()

    if platform_name == "windows":
        return f"{prefix}-{platform_name}-{arch}.zip"
    else:
        return f"{prefix}-{platform_name}-{arch}.tar.gz"

def get_binary_url(version):
    """Get the download URL for the binary."""
    base_url = "https://github.com/ervan0707/thira/releases/download"
    return f"{base_url}/v{version}/{get_archive_name()}"

def get_binary_dir():
    """Get the directory where the binary should be installed."""
    if sys.platform == "win32":
        app_data = os.environ.get("LOCALAPPDATA")
        if not app_data:
            app_data = os.path.join(os.environ["USERPROFILE"], "AppData", "Local")
        return Path(app_data) / "thira" / "bin"
    else:
        return Path.home() / ".local" / "share" / "thira" / "bin"

def get_binary_path():
    """Get the full path to the binary."""
    return get_binary_dir() / get_binary_name()
