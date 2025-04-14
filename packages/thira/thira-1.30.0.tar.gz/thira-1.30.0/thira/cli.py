import sys
import subprocess
from . import binary, ensure_binary

def main():
    try:
        binary_path = binary.get_binary_path()

        if not binary_path.exists():
            print("Thira binary not found. Running installer...")
            ensure_binary()

        # Execute the binary with all arguments
        result = subprocess.run([str(binary_path)] + sys.argv[1:])
        sys.exit(result.returncode)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
