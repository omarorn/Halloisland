"""
Download files from Google Drive using rclone
This is simpler than using the Google Drive API directly.
"""
import subprocess
import os
from pathlib import Path

# Set up directory for downloaded files
DOWNLOAD_DIR = Path("helloiceland_files")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def setup_rclone():
    """Check if rclone is installed and set up"""
    try:
        result = subprocess.run(["rclone", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("rclone is not installed. Installing...")
            subprocess.run(["curl", "https://rclone.org/install.sh", "|", "sudo", "bash"], shell=True)
    except FileNotFoundError:
        print("rclone is not installed. Installing...")
        subprocess.run(["curl", "https://rclone.org/install.sh", "|", "sudo", "bash"], shell=True)
    
    # Check if Google Drive remote is configured
    result = subprocess.run(["rclone", "listremotes"], capture_output=True, text=True)
    if "gdrive:" not in result.stdout:
        print("Google Drive remote is not configured.")
        print("Please run 'rclone config' to set up a Google Drive remote named 'gdrive'")
        print("Follow instructions at https://rclone.org/drive/")
        return False
    
    return True

def download_files():
    """Download files from Google Drive folder"""
    print("Downloading files from 'helloiceland' folder...")
    
    try:
        # List files in the folder
        result = subprocess.run(
            ["rclone", "lsf", "gdrive:My Drive/helloiceland"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error listing files: {result.stderr}")
            return
        
        files = result.stdout.strip().split("\n")
        if not files or files[0] == '':
            print("No files found in the folder.")
            return
        
        print(f"Found {len(files)} files. Starting download...")
        
        # Download the entire folder
        result = subprocess.run(
            ["rclone", "copy", "gdrive:My Drive/helloiceland", str(DOWNLOAD_DIR)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error downloading files: {result.stderr}")
            return
        
        print(f"Downloaded all files to {DOWNLOAD_DIR.absolute()}")
        
        # List downloaded files
        files = os.listdir(DOWNLOAD_DIR)
        print("\nDownloaded files:")
        for file in files:
            print(f"- {file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main function"""
    if setup_rclone():
        download_files()
    else:
        print("\nPlease set up rclone first, then run this script again.")

if __name__ == "__main__":
    main()