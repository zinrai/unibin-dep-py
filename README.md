# unibin-dep-py: Unix Binary Deployment Tool

`unibin-dep-py` is a Python-based command-line tool designed for Unix systems (Linux and macOS) that facilitates the safe download and deployment of binary files. It ensures that only compatible binaries are deployed to the specified directory.

[unibin-dep (Golang Version)](https://github.com/zinrai/unibin-dep): This is the Golang implementation of the unibin-dep tool.

## Features

- Downloads files from specified URLs
- Utilizes the `file` command to detect file types and binary compatibility
- Checks binary compatibility with the host system (Linux and macOS)
- Safely handles downloads using temporary files
- Moves compatible binaries to the specified directory
- Automatically sets executable permissions for compatible binaries
- Cleans up incompatible binaries

## Requirements

- Python 3.6+
- Unix-like operating system (Linux or macOS)
- `file` command (usually pre-installed on most Unix systems)

## Usage

The basic syntax for using `unibin-dep-py` is:

```
$ ./unibin-dep.py -u <download_url> -d <save_directory> [-f <custom_filename>]
```

Example:

```
$ ./unibin-dep.py -u https://github.com/kubernetes-sigs/kind/releases/download/v0.24.0/kind-linux-amd64 -d ~/bin -f kind
```

## How it works

1. The tool checks if the `file` command is available on the system.
2. It downloads the file from the specified URL to a temporary location.
3. Using the `file` command, it determines the type of the downloaded file.
4. For binary files, it verifies compatibility with the host system.
5. Compatible binaries are moved to the specified directory and given executable permissions.
6. Incompatible binaries are removed.
7. Non-binary files are moved to the specified directory without additional checks.

## Supported Systems

`unibin-dep-py` is designed to work on:

- Linux: x86_64 (amd64), ARM64
- macOS: x86_64 (amd64), ARM64

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) for details.
