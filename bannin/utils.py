import base64
import os
import shutil

from argon2 import PasswordHasher
from cryptography.fernet import Fernet

DEFAULT_SALT_FILE_NAME = "FolderKey.key"
PASSWORD_HASHER = PasswordHasher(hash_len=24)
ENCRYPTED_FILE_EXTENSION = ".enc"


def write_to_file(filepath: str, data: bytes) -> None:
    with open(filepath, "wb") as file:
        file.write(data)


def read_file_data(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        data = file.read()

    return data


def generate_salt(dirname: str, filename: str = None) -> bytes:
    """Generate salt to be used when hashing password for encryption.

    Arguments
    ---------
    dirname str
        The directory to create the file to store the salt value.
    filename str
        The name of the file that will store the salt value.
        If None, filename will be set to DEFAULT_SALT_FILE_NAME.

    Returns
    -------
    key bytes
        The salt value generated.
    """
    name = filename if filename else DEFAULT_SALT_FILE_NAME
    salt_filename = os.path.join(dirname, name)

    key = Fernet.generate_key()
    write_to_file(salt_filename, key)

    return key


def generate_fernet_key(password: str, salt: bytes) -> bytes:
    """Generate key to be used by Fernet to encrypt and decrypt data.

    Arguments
    ---------
    password str
        The password to be used to generate a hash to generate the Fernet key.
    salt bytes
        The salt to be used by PASSWORD_HASHER when generating a hash.

    Returns
    -------
    key bytes
        The Fernet key to be used in encryption or decryption.
    """
    password_hash = PASSWORD_HASHER.hash(password, salt=salt)

    encryption_key = bytes(password_hash.split("$")[-1].encode("utf-8"))
    return base64.urlsafe_b64encode(encryption_key)


def get_directory_and_filename(
    directory: str = None, filename: str = None, filepath: str = None
) -> tuple:
    """Get the directory name and file name to be encrypted or decrypted.

    The filepath is given priority over directory and filename.

    Arguments
    ---------
    directory str
        The directory containing the file(s) to encrypt or decrypt.
        If filepath is not None, the base directory of filepath will be used.
        If directory and filepath are None, then it uses the current working directory.
    filename str
        The name of the file to encrypt or decrypt.
        If filepath is present, the file from the filepath is used.
    filepath str
        The path of the file to encrypt or decrypt.

    Returns
    -------
    (directory, filename) tuple
        The directory and filename to encrypt or decrypt.
    """
    if filepath is not None:
        if os.path.isfile(filepath):
            return os.path.dirname(filepath), os.path.split(filepath)[1]

        raise ValueError("Invalid file path provided.")

    if directory is not None and not os.path.isdir(directory):
        raise ValueError("Invalid directory provided.")

    if directory is None:
        directory = os.getcwd()

    if filename is not None and not os.path.isfile(os.path.join(directory, filename)):
        raise ValueError("Invalid file name provided")

    if directory.endswith("/"):
        directory = os.path.dirname(directory)

    return directory, filename


class Bannin:
    def __init__(
        self,
        directory: str,
        password: str,
        filename: str = None,
        salt: bytes = None,
        salt_filename: str = None,
        extensions: list = None,
    ):
        self.directory = directory
        self.password = password
        self.filename = filename
        self.salt = salt
        self.salt_filename = salt_filename
        self.extensions = extensions

    def __encrypt_file(self, filepath, filename, output_directory):
        data_to_encrypt = read_file_data(filepath)
        encrypted_data = self.fernet.encrypt(data_to_encrypt)
        output_filepath = os.path.join(
            output_directory, f"{filename}{ENCRYPTED_FILE_EXTENSION}"
        )
        write_to_file(output_filepath, encrypted_data)

    def __decrypt_file(self, filepath, filename):
        data_to_decrypt = read_file_data(filepath)
        decrypted_data = self.fernet.decrypt(data_to_decrypt)
        output_filepath = os.path.join(
            self.directory, filename.replace(ENCRYPTED_FILE_EXTENSION, "")
        )
        write_to_file(output_filepath, decrypted_data)

    def encrypt(self):
        if self.filename:
            output_directory = os.path.join(
                self.directory, os.path.splitext(self.filename)[0]
            )
        else:
            name = f"encrypted_{os.path.basename(self.directory)}"
            output_directory = os.path.join(self.directory, name)
        os.mkdir(output_directory)

        if self.salt is None:
            self.salt = generate_salt(output_directory, self.salt_filename)
        fernet_key = generate_fernet_key(self.password, self.salt)
        self.fernet = Fernet(fernet_key)

        if self.filename:
            filepath = os.path.join(self.directory, self.filename)
            return self.__encrypt_file(filepath, self.filename, output_directory)

        encrypted_file_counter = 0
        for file in os.listdir(self.directory):
            filepath = os.path.join(self.directory, file)
            if not os.path.isfile(filepath):
                continue

            if self.extensions and not any(
                file.endswith(extension) for extension in self.extensions
            ):
                continue

            self.__encrypt_file(filepath, file, output_directory)
            encrypted_file_counter += 1

        if encrypted_file_counter == 0:
            shutil.rmtree(output_directory)

    def decrypt(self):
        if self.salt is None:
            salt_filepath = os.path.join(self.directory, self.salt_filename)
            if not os.path.isfile(salt_filepath):
                raise ValueError("Salt file not found.")
            self.salt = read_file_data(salt_filepath)

        fernet_key = generate_fernet_key(self.password, self.salt)
        self.fernet = Fernet(fernet_key)

        if self.filename:
            if not self.filename.endswith(ENCRYPTED_FILE_EXTENSION):
                raise ValueError(
                    f"File to encrypt does not end with {ENCRYPTED_FILE_EXTENSION}."
                )

            filepath = os.path.join(self.directory, self.filename)
            return self.__decrypt_file(filepath, self.filename)

        for file in os.listdir(self.directory):
            filepath = os.path.join(self.directory, file)
            if not os.path.isfile(filepath):
                continue

            if not file.endswith(ENCRYPTED_FILE_EXTENSION):
                continue

            self.__decrypt_file(filepath, file)
