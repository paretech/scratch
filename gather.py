import argparse
from pathlib import Path
import subprocess

def copy_symlink_targets(src_dir, dest_dir):
    # Check if source and destination directories exist
    if not src_dir.exists() or not dest_dir.exists():
        print("Source or destination directory does not exist.")
        return

    # Iterate over the items in the source directory
    for item in src_dir.iterdir():
        # Check if the item is a symlink
        if item.is_symlink():
            target = item.resolve()  # Get the absolute path of the target
            target_name = target.name  # Get the name of the target

            # Construct the rsync command
            rsync_command = ["rsync", "-avz", str(target), str(dest_dir / target_name)]

            # Execute the rsync command
            try:
                subprocess.run(rsync_command, check=True)
                print(f"Successfully copied {target} to {dest_dir / target_name}")
            except subprocess.CalledProcessError as e:
                print(f"Rsync failed for {target}: {e}")

def main():
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description='Copy symlink targets from source to destination directory')
    parser.add_argument('source_directory', help='Path to the source directory')
    parser.add_argument('destination_directory', help='Path to the destination directory')

    args = parser.parse_args()

    # Convert string paths to Path objects
    source_directory = Path(args.source_directory)
    destination_directory = Path(args.destination_directory)

    # Run the function with the provided arguments
    copy_symlink_targets(source_directory, destination_directory)

if __name__ == '__main__':
    main()
