import subprocess
import sys

from . import binary

def main():
    """Main entry point for the thira command."""
    try:
        binary_path = binary.get_binary_path()

        if not binary_path.exists():
            print(f"Error: Binary not found at {binary_path}")
            print("Try reinstalling the package")
            sys.exit(1)

        # Execute the binary with all arguments
        result = subprocess.run([str(binary_path)] + sys.argv[1:])
        sys.exit(result.returncode)

    except Exception as e:
        print(f"Error executing thira: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
