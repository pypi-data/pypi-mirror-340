import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

from . import binary

def get_version() -> str:
    """Get the package version from multiple sources."""
    try:
        # Try getting version from installed package
        from importlib.metadata import version
        return version("thira")
    except ImportError:
        try:
            # Try getting version from pyproject.toml for development
            import tomli
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)
            return pyproject["tool"]["poetry"]["version"]
        except Exception:
            # Fallback to hardcoded version for development
            return "1.20.0"

def download_binary(url: str, dest: Path) -> None:
    """Download the binary from the given URL."""
    if os.getenv("THIRA_MOCK_DOWNLOAD"):
        print(f"[TEST] Would download from: {url}")
        # Create a mock archive structure
        if dest.suffix == ".zip":
            with ZipFile(dest, 'w') as zf:
                binary_name = binary.get_binary_name()
                mock_binary = f"#!/bin/sh\necho 'Thira Test Binary v{get_version()}'\n"
                zf.writestr(binary_name, mock_binary)
        else:
            # For tar.gz files
            with tarfile.open(dest, 'w:gz') as tar:
                binary_name = binary.get_binary_name()
                mock_binary = f"#!/bin/sh\necho 'Thira Test Binary v{get_version()}'\n"

                # Create a temporary file with the mock content
                with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
                    tmp.write(mock_binary)
                    tmp.flush()

                    # Make the temp file executable
                    os.chmod(tmp.name, 0o755)

                    # Add it to the tar archive
                    tar.add(tmp.name, arcname=binary_name)

                    # Clean up the temp file
                    os.unlink(tmp.name)
        return

    print(f"Downloading from: {url}")
    urlretrieve(url, dest)

def extract_archive(archive_path: Path, extract_dir: Path) -> Path:
    """Extract the archive and return the path to the binary."""
    print("Extracting archive...")
    binary_name = binary.get_binary_name()

    if archive_path.suffix == ".zip":
        with ZipFile(archive_path) as zip_file:
            # List contents for debugging
            print(f"Archive contents: {zip_file.namelist()}")
            zip_file.extractall(extract_dir)
    else:
        with tarfile.open(archive_path) as tar:
            # List contents for debugging
            print(f"Archive contents: {tar.getnames()}")
            tar.extractall(extract_dir)

    # Find the binary in the extracted files
    extracted_files = list(extract_dir.rglob(binary_name))

    if not extracted_files:
        # For debugging, list all files in extract directory
        print("Files in extract directory:")
        for file in extract_dir.rglob("*"):
            print(f"  {file}")
        raise FileNotFoundError(f"Binary not found in extracted files: {binary_name}")

    return extracted_files[0]

def install_binary():
    """Install the binary."""
    thira_version = get_version()
    print(f"\nInstalling thira v{thira_version}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Archive name: {binary.get_archive_name()}")
    print(f"Binary name: {binary.get_binary_name()}")

    binary_dir = binary.get_binary_dir()
    binary_path = binary.get_binary_path()

    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        archive_path = temp_dir_path / binary.get_archive_name()

        try:
            # Download binary
            download_binary(binary.get_binary_url(thira_version), archive_path)
            print("✓ Download complete")

            # Extract archive
            extracted_binary = extract_archive(archive_path, temp_dir_path)
            print("✓ Extraction complete")

            # Create installation directory
            binary_dir.parent.mkdir(parents=True, exist_ok=True)
            binary_dir.mkdir(exist_ok=True)

            # Install binary
            shutil.copy2(extracted_binary, binary_path)
            print(f"✓ Binary installed to: {binary_path}")

            # Set executable permissions on Unix
            if platform.system() != "Windows":
                binary_path.chmod(0o755)
                print("✓ Executable permissions set")

            # Mock verification in test mode
            if os.getenv("THIRA_MOCK_DOWNLOAD"):
                print("✓ Binary verification successful (mock)")
            else:
                # Verify installation
                result = subprocess.run([str(binary_path), "--version"], capture_output=True)
                if result.returncode == 0:
                    print("✓ Binary verification successful")
                else:
                    raise RuntimeError("Binary verification failed")

            print("\n✅ Installation successful! You can now use the 'thira' command.\n")

        except Exception as e:
            print(f"\n❌ Installation failed: {str(e)}")
            if isinstance(e, FileNotFoundError):
                print("\nDebug information:")
                print(f"Archive path: {archive_path}")
                print(f"Archive exists: {archive_path.exists()}")
                print(f"Extract directory: {temp_dir_path}")
                print(f"Binary name to find: {binary.get_binary_name()}")
            sys.exit(1)

if __name__ == "__main__":
    install_binary()
