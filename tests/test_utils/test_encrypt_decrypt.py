import os
import shutil
from unittest import TestCase

from bannin.utils import decrypt_data, encrypt_data


class TestEncryptData(TestCase):
    def setUp(self):
        self.directory = "./tests/dummy_files"
        self.password = "password"
        self.remove_directory = None

    def test_encrypt_file(self):
        data = {
            "dirname": self.directory,
            "password": self.password,
            "filename": "sample.txt",
            "salt": None,
            "salt_filename": "FolderKey.key",
            "extensions": None,
        }
        encrypt_data(**data)

        self.remove_directory = os.path.join(self.directory, "sample")
        salt_filepath = os.path.join(self.remove_directory, data["salt_filename"])
        encrypted_filepath = os.path.join(
            self.remove_directory, f"{data['filename']}.enc"
        )

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertTrue(os.path.isfile(encrypted_filepath))

    def test_encrypt_directory(self):
        directory = os.path.join(self.directory, "new_folder")
        data = {
            "dirname": directory,
            "password": self.password,
            "filename": None,
            "salt": None,
            "salt_filename": "FolderKey.key",
            "extensions": None,
        }
        encrypt_data(**data)

        self.remove_directory = os.path.join(directory, "encrypted_new_folder")
        salt_filepath = os.path.join(self.remove_directory, data["salt_filename"])
        encrypted_files = [
            file for file in os.listdir(self.remove_directory) if file.endswith(".enc")
        ]

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertEqual(len(encrypted_files), 2)

    def test_encrypt_directory_with_extensions(self):
        directory = os.path.join(self.directory, "new_folder")
        data = {
            "dirname": directory,
            "password": self.password,
            "filename": None,
            "salt": None,
            "salt_filename": "FolderKey.key",
            "extensions": [".txt", ".mp3"],
        }
        encrypt_data(**data)

        self.remove_directory = os.path.join(directory, "encrypted_new_folder")
        salt_filepath = os.path.join(self.remove_directory, data["salt_filename"])
        encrypted_files = [
            file for file in os.listdir(self.remove_directory) if file.endswith(".enc")
        ]

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertEqual(len(encrypted_files), 1)

    def tearDown(self):
        if self.remove_directory:
            shutil.rmtree(self.remove_directory)


class TestDecryptData(TestCase):
    def setUp(self):
        self.directory = "./tests/dummy_files/encrypted_folder"
        self.password = "password"
        self.remove_file = None

    def test_decrypt_file(self):
        data = {
            "dirname": self.directory,
            "password": self.password,
            "filename": "sample.txt.enc",
            "salt": None,
            "salt_filename": "FolderKey.key",
        }
        decrypt_data(**data)

        self.remove_file = os.path.join(self.directory, "sample.txt")
        self.assertTrue(os.path.isfile(self.remove_file))
        with open(self.remove_file, "rb") as file:
            file_data = file.read()
            self.assertEqual(file_data, b"Bannin test sample file.\n")

    def test_decrypt_file_invalid_data(self):
        data = {
            "dirname": self.directory,
            "password": self.password,
            "filename": "sample.txt.enc",
            "salt": None,
            "salt_filename": "fake.file",
        }
        with self.assertRaises(ValueError):
            decrypt_data(**data)

        data = {
            "dirname": self.directory,
            "password": self.password,
            "filename": "sample.txt",
            "salt": None,
            "salt_filename": "FolderKey.key",
        }
        decrypt_data(**data)
        filepath = os.path.join(self.directory, data["filename"])
        self.assertFalse(os.path.isfile(filepath))

    def test_decrypt_directory(self):
        data = {
            "dirname": self.directory,
            "password": self.password,
            "salt": None,
            "salt_filename": "FolderKey.key",
        }
        decrypt_data(**data)

        self.remove_file = os.path.join(self.directory, "sample.txt")
        self.assertTrue(os.path.isfile(self.remove_file))
        with open(self.remove_file, "rb") as file:
            file_data = file.read()
            self.assertEqual(file_data, b"Bannin test sample file.\n")

    def tearDown(self):
        if self.remove_file:
            os.remove(self.remove_file)
