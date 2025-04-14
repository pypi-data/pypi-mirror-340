import sys
from pathlib import Path
from . import binary

def uninstall():
    """Remove the Thira binary."""
    try:
        binary_path = binary.get_binary_path()
        if binary_path.exists():
            print(f"\nRemoving Thira binary from: {binary_path}")
            binary_path.unlink()
            print("✓ Binary removed")

            # Try to remove parent directories if empty
            bin_dir = binary.get_binary_dir()
            try:
                if bin_dir.exists() and not any(bin_dir.iterdir()):
                    bin_dir.rmdir()
                    print("✓ Removed empty binary directory")

                parent_dir = bin_dir.parent
                if parent_dir.exists() and not any(parent_dir.iterdir()):
                    parent_dir.rmdir()
                    print("✓ Removed empty parent directory")
            except Exception as e:
                print(f"Note: Could not remove directories: {e}")

        print("\n✅ Uninstallation successful!")

    except Exception as e:
        print("\n❌ Uninstallation failed!")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    uninstall()
