import os
import sys
import platform
import shutil
import tarfile
import zipfile
from pathlib import Path
import tempfile
import requests
from . import binary

def download_file(url: str, dest_path: Path) -> None:
    """
    Download a file from URL to destination path with progress indicator.
    """
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = int(100 * downloaded / total_size)
                        sys.stdout.write(f"\rProgress: {percent}% [{downloaded}/{total_size} bytes]")
                        sys.stdout.flush()

        print("\n✓ Download complete")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download file: {str(e)}")

def list_directory_contents(path: Path, indent: str = "") -> None:
    """
    Recursively list contents of a directory for debugging.
    """
    print(f"\nContents of {path}:")
    for item in path.iterdir():
        print(f"{indent}├── {item.name}")
        if item.is_dir():
            list_directory_contents(item, indent + "│   ")

def install() -> None:
    """
    Install the Thira binary for the current platform.
    """
    try:
        # Get package version
        from . import __version__
        version = __version__

        # Get platform info
        system = platform.system().lower()
        machine = platform.machine().lower()

        print(f"\nInstalling thira v{version}")
        print(f"Platform: {system} {machine}")

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            archive_path = temp_dir / binary.get_archive_name()

            # Download archive
            url = binary.get_binary_url(version)
            download_file(url, archive_path)

            if not archive_path.exists():
                raise Exception(f"Archive not downloaded successfully to {archive_path}")

            # Create extract directory
            extract_dir = temp_dir / "extract"
            extract_dir.mkdir(exist_ok=True)

            # Extract archive
            print("Extracting archive...")
            try:
                if sys.platform == "win32":
                    with zipfile.ZipFile(archive_path) as zf:
                        zf.extractall(extract_dir)
                        print("Archive contents:")
                        for name in zf.namelist():
                            print(f"- {name}")
                else:
                    with tarfile.open(archive_path, "r:gz") as tf:
                        tf.extractall(extract_dir)
                        print("Archive contents:")
                        for member in tf.getmembers():
                            print(f"- {member.name}")
            except (zipfile.BadZipFile, tarfile.TarError) as e:
                raise Exception(f"Failed to extract archive: {str(e)}")

            # List extracted contents for debugging
            list_directory_contents(extract_dir)

            # Get binary path and ensure directory exists
            bin_dir = binary.get_binary_dir()
            bin_dir.parent.mkdir(parents=True, exist_ok=True)
            bin_dir.mkdir(exist_ok=True)

            # Find the platform-specific binary and rename it
            platform_binary_name = f"thira-{system}-{machine}"
            binary_name = binary.get_binary_name()

            print(f"\nLooking for binary: {platform_binary_name}")

            # Find the binary in the extracted files
            extracted_binary = None
            for file in extract_dir.glob("**/*"):
                if file.name == platform_binary_name:
                    # Rename the file to the correct binary name
                    new_path = file.parent / binary_name
                    file.rename(new_path)
                    extracted_binary = new_path
                    print(f"✓ Renamed {platform_binary_name} to {binary_name}")
                    break

            if not extracted_binary:
                raise FileNotFoundError(
                    f"Could not find binary '{platform_binary_name}' in extracted files. "
                    f"Please ensure the archive contains the correct binary."
                )

            dest_path = bin_dir / binary_name
            print(f"\nCopying binary to {dest_path}")

            # Remove existing binary if it exists
            if dest_path.exists():
                dest_path.unlink()

            # Copy the binary
            shutil.copy2(extracted_binary, dest_path)
            print(f"✓ Binary installed to: {dest_path}")

            # Set executable permissions on Unix
            if sys.platform != "win32":
                dest_path.chmod(0o755)
                print("✓ Executable permissions set")

            # Verify installation
            if not dest_path.exists():
                raise Exception("Binary was not installed correctly")

            if sys.platform != "win32":
                if not os.access(dest_path, os.X_OK):
                    raise Exception("Binary is not executable")

        print("\n✅ Installation successful!")
        print(f'You can now use the "thira" command.\n')
        print(f"Binary location: {dest_path}")
        print(f"Version installed: {version}")

    except Exception as e:
        print("\n❌ Installation failed!")
        print(f"Error: {str(e)}")
        print("\nDebug information:")
        print(f"- System: {platform.system()}")
        print(f"- Machine: {platform.machine()}")
        print(f"- Python version: {sys.version}")
        print(f"- Binary name: {binary.get_binary_name()}")
        print(f"- Archive name: {binary.get_archive_name()}")
        sys.exit(1)

def main():
    """
    Main entry point when running installer directly.
    """
    print("Running Thira installer...")
    install()

if __name__ == "__main__":
    main()
