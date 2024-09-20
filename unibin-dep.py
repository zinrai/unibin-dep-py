#!/usr/bin/env python3

import os
import sys
import urllib.request
import subprocess
import argparse
import shutil
import tempfile
import platform

def check_file_command():
    try:
        subprocess.run(['file', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_file(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
        out_file.write(response.read())

def get_file_info(file_path):
    try:
        result = subprocess.run(['file', '-b', file_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running 'file' command: {e}")
        sys.exit(1)

def is_compatible_binary(file_info):
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == 'linux':
        if 'ELF' not in file_info:
            return False
        if 'x86-64' in file_info and machine == 'x86_64':
            return True
        if 'aarch64' in file_info and machine == 'aarch64':
            return True
    elif system == 'darwin':
        if 'Mach-O' not in file_info:
            return False
        if 'x86_64' in file_info and machine == 'x86_64':
            return True
        if 'arm64' in file_info and machine == 'arm64':
            return True
    return False

def set_executable(file_path):
    current_mode = os.stat(file_path).st_mode
    os.chmod(file_path, current_mode | 0o111)  # Add execute permission

def main(args):
    if platform.system().lower() not in ['linux', 'darwin']:
        print("This tool is designed for Linux and macOS only.")
        sys.exit(1)

    if not check_file_command():
        print("The 'file' command is not available on this system. Please install it to use this tool.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, 'downloaded_file')

        try:
            print(f"Downloading file from {args.url}...")
            download_file(args.url, temp_file_path)
            print("Download completed.")

            file_info = get_file_info(temp_file_path)
            print(f"File type: {file_info}")

            if 'executable' in file_info.lower() or 'shared object' in file_info.lower():
                if is_compatible_binary(file_info):
                    print("The binary is compatible with the current system.")

                    os.makedirs(args.save_dir, exist_ok=True)

                    final_path = os.path.join(args.save_dir, args.filename or os.path.basename(args.url))
                    shutil.move(temp_file_path, final_path)

                    set_executable(final_path)
                    print(f"File saved to: {final_path}")
                    print("Execution permissions granted.")
                else:
                    print("The binary is not compatible with the current system.")
                    print("File will not be saved.")
            else:
                print("The file is not a binary executable.")
                final_path = os.path.join(args.save_dir, args.filename or os.path.basename(args.url))
                shutil.move(temp_file_path, final_path)
                print(f"Non-binary file saved to: {final_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="unibin-dep-py: Unix Binary Deployment Tool (Python Version)")
    parser.add_argument("-u", "--url", required=True, help="URL of the file to download")
    parser.add_argument("-d", "--save-dir", required=True, help="Directory to save the downloaded file")
    parser.add_argument("-f", "--filename", help="Specify a custom filename for the downloaded file")

    args = parser.parse_args()
    main(args)
