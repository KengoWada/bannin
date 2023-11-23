import base64
import os

from argon2 import PasswordHasher
from cryptography.fernet import Fernet

DEFAULT_SALT_FILE_NAME = "FolderKey.key"
PASSWORD_HASHER = PasswordHasher(hash_len=24)
ENCRYPTED_FILE_EXTENSION = ".enc"


def write_to_file(filename: str, data: bytes) -> None:
    with open(filename, "wb") as file:
        file.write(data)


def read_file_data(filename: str) -> bytes:
    with open(filename, "rb") as file:
        data = file.read()

    return data


def generate_salt(dirname: str, filename: str | None = None) -> bytes:
    name = filename if filename else DEFAULT_SALT_FILE_NAME
    salt_filename = os.path.join(dirname, name)

    key = Fernet.generate_key()
    write_to_file(salt_filename, key)

    return key


def generate_fernet_key(password: str, salt: bytes) -> bytes:
    password_hash = PASSWORD_HASHER.hash(password, salt=salt)

    encryption_key = bytes(password_hash.split("$")[-1].encode("utf-8"))
    return base64.urlsafe_b64encode(encryption_key)


def get_file_directory_details(args: dict) -> tuple[str, str | None]:
    """Get base directory and file name."""
    base_dir = os.getcwd()

    directory = args.get("directory")
    if directory:
        if os.path.isdir(directory):
            base_dir = directory
        else:
            raise ValueError("Invalid directory provided.")

    filename = args.get("filename")
    if filename:
        filepath = os.path.join(base_dir, filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid file name provided.")

    filepath = args.get("filepath")
    if filepath:
        if os.path.isfile(filepath):
            base_dir = os.path.dirname(filepath)
            filename = os.path.split(filepath)[1]
        else:
            raise ValueError("Invalid file path provided.")

    return base_dir, filename


def encrypt_file(
    filepath: str, filename: str, fernet_key: bytes, output_directory: str
):
    fernet = Fernet(fernet_key)
    data_to_encrypt = read_file_data(filepath)
    encrypted_data = fernet.encrypt(data_to_encrypt)
    output_file = f"{filename}{ENCRYPTED_FILE_EXTENSION}"
    write_to_file(os.path.join(output_directory, output_file), encrypted_data)


def decrypt_file(filepath: str, filename: str, fernet_key: bytes, dirname: str):
    fernet = Fernet(fernet_key)
    data_to_decrypt = read_file_data(filepath)
    decrypted_data = fernet.decrypt(data_to_decrypt)
    output_file = f"{filename.replace(ENCRYPTED_FILE_EXTENSION, '')}"
    write_to_file(os.path.join(dirname, output_file), decrypted_data)


def encrypt_data(dirname: str, password: str, **kwargs):
    filename = kwargs.get("filename")
    if filename:
        output_directory = os.path.join(dirname, os.path.splitext(filename)[0])
    else:
        name = f"encrypted_{os.path.basename(dirname)}"
        output_directory = os.path.join(dirname, name)

    os.mkdir(output_directory)

    salt = kwargs.get("salt")
    if not salt:
        salt = generate_salt(output_directory, kwargs.get("salt_filename"))

    fernet_key = generate_fernet_key(password, salt)

    if filename:
        return encrypt_file(
            os.path.join(dirname, filename), filename, fernet_key, output_directory
        )

    extensions = kwargs.get("extensions")
    for file in os.listdir(dirname):
        if not os.path.isfile(os.path.join(dirname, file)):
            continue

        if extensions and not any(file.endswith(extension) for extension in extensions):
            continue

        encrypt_file(os.path.join(dirname, file), file, fernet_key, output_directory)


def decrypt_data(dirname: str, password: str, **kwargs):
    salt = kwargs.get("salt")
    if not salt:
        salt_file_path = os.path.join(dirname, kwargs.get("salt_filename"))
        if not os.path.isfile(salt_file_path):
            raise ValueError("Salt file not found.")

        salt = read_file_data(salt_file_path)

    fernet_key = generate_fernet_key(password, salt)

    filename = kwargs.get("filename")
    if filename:
        return (
            decrypt_file(os.path.join(dirname, filename), filename, fernet_key, dirname)
            if filename.endswith(ENCRYPTED_FILE_EXTENSION)
            else None
        )

    for file in os.listdir(dirname):
        if not os.path.isfile(os.path.join(dirname, file)):
            continue

        if not file.endswith(ENCRYPTED_FILE_EXTENSION):
            continue

        decrypt_file(os.path.join(dirname, file), file, fernet_key, dirname)
