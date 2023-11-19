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
pip install -r requirements.txt
```

### Notes

- Use python >= 3.10

- The password for encrypting and decrypting has been hard coded to `password` for safety purposes.

- Please use this with caution as you may fail to recover your files if you say forget your password or misplace the `FolderKey.key`.

- Read through the code to get an understanding of what is being done before using.

### How To Encrypt Data

This shows how to encrypt files or directories.

```sh
python main.py encrypt -f /path/to/file.txt -d /path/to/dir/ -F filename.txt -s /path/to/salt_file.txt -S saltfile.txt -e .txt,.zip
```

- **`-f` `--filepath`**

  This indicates the file you wish to encrypt. This flag is given priority over `-d` and `-F` if all are provided.

```sh
python main.py encrypt -f /path/to/file_to_encrypt.png
# OR
python main.py encrypt --filepath /path/to/file_to_encrypt.png
```

- **`-d` `--dir`**

  This indicates the directory whose files you wish to encrypt.

  This does not encrypt files in sub-directories. If no directory is provided, the current working directory is used.

```sh
python main.py -d /path/to/secret_folder
# OR
python main.py --dir /path/to/secret_folder
```

- **`-F` `--filename`**

  This indicates the file in the selected directory to be encrypted.

```sh
python main.py encrypt -F new_hit.mp3 # This encrypts the new_hit.mp3 file in the current working directory
# OR
python main.py encrypt --filename new_hit.mp3

python main.py encrypt -d /path/to/album/ -F hit_song.mp3 # This encrypts the hit_song.mp3 file in the album directory
# OR
python main.py encrypt --dir /path/to/album/ --filename hit_song.mp3
```

- **`-s` `--salt-filepath`**

  This indicates the path to the file to use as a salt.

  The file must return 32 url-safe base64-encoded bytes.

```sh
python main.py encrypt -s /path/to/salt_file.key
# OR
python main.py encrypt --salt-filepath /path/to/salt_file.key
```

- **`-S` `--salt-filename`**

  This indicates the file name to store the salt key. Defaults to `FolderKey.key`

```sh
python main.py encrypt -S secret.key
# OR
python main.py encrypt --salt-filename secret.key
```

- **`-e` `--extensions`**

  This indicates the file extensions to encrypt in a directory. All files not having the extension will not be encrypted.

  These are comma separated e.g. `.txt,.zip,.mp3`

```sh
python main.py encrypt -e .txt,.zip,.mp3
#OR
python main.py encrypt --extensions .txt,.zip,.mp3
```

### How To Decrypt Data

This indicates how to decrypt files or directories. Only `*.enc` files will be decrypted.

```sh
python main.py decrypt -f /path/to/file.txt.enc -d /path/to/encrypted_dir -F file.mp3.enc -s /path/to/saltfile.key -S FolderKey.key
```

The flags have the same definitions as above in the encryption with a few exceptions:

- Only `*.enc` files will be decrypted.

- The extensions flag is ignored for decryption.
