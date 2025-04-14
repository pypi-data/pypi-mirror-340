import os
import platform
import sys
from pathlib import Path

def get_binary_name() -> str:
    """Get the binary name based on the platform."""
    return "thira.exe" if platform.system() == "Windows" else "thira"

def get_arch_name() -> str:
    """Get the architecture name."""
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return "x86_64"
    elif machine in ("arm64", "aarch64"):
        return "arm64"
    raise ValueError(f"Unsupported architecture: {machine}")

def get_archive_name() -> str:
    """Get the archive name based on platform and architecture."""
    prefix = "thira"
    system = platform.system().lower()
    arch = get_arch_name()

    if system == "windows":
        return f"{prefix}-windows-{arch}.zip"
    elif system == "darwin":
        return f"{prefix}-darwin-{arch}.tar.gz"
    elif system == "linux":
        return f"{prefix}-linux-{arch}.tar.gz"
    raise ValueError(f"Unsupported platform: {system}")

def get_binary_url(version: str) -> str:
    """Get the binary download URL."""
    base_url = "https://github.com/ervan0707/thira/releases/download"
    return f"{base_url}/v{version}/{get_archive_name()}"

def get_binary_dir() -> Path:
    """Get the directory where the binary should be stored."""
    if hasattr(sys, "real_prefix") or sys.base_prefix != sys.prefix:
        # Running in a virtual environment
        binary_dir = Path(sys.prefix) / "lib" / "thira" / "bin"
    else:
        # Global installation
        if platform.system() == "Windows":
            binary_dir = Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData")) / "thira" / "bin"
        else:
            binary_dir = Path("/usr/local/lib/thira/bin")

    return binary_dir

def get_binary_path() -> Path:
    """Get the full path to the binary."""
    return get_binary_dir() / get_binary_name()
