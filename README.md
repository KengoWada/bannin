# 番人

A python cli app to encrypt and decrypt files.

> [!WARNING]
> **This will encrypt your files and you may not be able to recover them.**

## Getting Started

- Clone the repo

- Create and activate a virtual environment

```sh
python -m venv venv
source venv/bin/activate
```

- Install the dependencies

```sh
pip install --upgrade pip
pip install -r requirements/base.txt
```

### Notes

- Use python >= 3.10

- The password for encrypting and decrypting has been hard coded to `password` for safety purposes.

- Please use this with caution as you may fail to recover your files if you say forget your password or misplace the `FolderKey.key`.

- Read through the code to get an understanding of what is being done before using.

- Don't try to encrypt large files due to [Fernet limitations](https://cryptography.io/en/latest/fernet/#limitations).

### CLI Flags

| Flag | Description |
| :--- | :--- |
| action | Choose to either `encrypt` or `decrypt`. Example: `bannin encrypt` |
| `-f` `--filepath` | This indicates the file you wish to encrypt or decrypt.<br /> This flag is given priority over `--dir` and `--filename` if all are provided. |
| `-d` `--dir` | This indicated the directory whose files you wish to encrypt or decrypt.<br /> This does not encrypt or decrypt files in sub-directories.<br /> If no directory is provided it uses the `--filepath` base directory or the current working directory. |
| `-F` `--filename` | This indicates the file name to encrypt or decrypt.<br /> If `--dir` is not set, it uses the current working directory. |
| `-s` `--saltpath` | This indicates the path to the file that contains the salt value.<br /> The file must return 32 url-safe base64-encoded bytes.<br /> This is given priority over `--salt-filename` if both are provided. |
| `-S` `--salt-filename` | This indicates the name of the file that contains the salt value.<br /> During encryption the salt file will be named this.<br /> During decryption this checks the `--dir` for the file.<br /> This defaults to `FolderKey.key` |
| `-e` `--extensions` | This indicates the file extensions to encrypt in a directory.<br /> These are comma separated: `.txt,.zip,.mp3`. |

### Using Bannin

- Run all [Getting Started](#getting-started) steps.

- Go to `bannin/__main__.py` and make the following changes

```diff
- # from getpass import getpass
+ from getpass import getpass

- # password = getpass()
+ password = getpass()

- "password": "password",
+ "password": password,
```

  **Note**: This will now ask for password before encryption and decryption. Forgetting this password means you won't decrypt any files you encrypted.

- Now install bannin from pip

```sh
pip install -e .
```

- Switch to `safe_space` directory to test out the app.

```sh
cd safe_space
bannin encrypt -F sample.txt
bannin decrypt --dir ./sample
```
