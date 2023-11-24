import os
import shutil
from unittest import TestCase

from bannin.utils import Bannin


class TestEncryptData(TestCase):
    def setUp(self):
        self.directory = "./tests/dummy_files"
        self.password = "password"
        self.remove_directory = None

    def test_encrypt_file(self):
        bannin = Bannin(
            directory=self.directory,
            password=self.password,
            filename="sample.txt",
            salt_filename="FolderKey.key",
        )
        bannin.encrypt()

        self.remove_directory = os.path.join(self.directory, "sample")
        salt_filepath = os.path.join(self.remove_directory, "FolderKey.key")
        encrypted_filepath = os.path.join(self.remove_directory, "sample.txt.enc")

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertTrue(os.path.isfile(encrypted_filepath))

    def test_encrypt_directory(self):
        directory = os.path.join(self.directory, "new_folder")
        bannin = Bannin(
            directory=directory,
            password=self.password,
            salt_filename="FolderKey.key",
        )
        bannin.encrypt()

        self.remove_directory = os.path.join(directory, "encrypted_new_folder")
        salt_filepath = os.path.join(self.remove_directory, "FolderKey.key")
        encrypted_files = [
            file for file in os.listdir(self.remove_directory) if file.endswith(".enc")
        ]

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertEqual(len(encrypted_files), 2)

    def test_encrypt_directory_with_extensions(self):
        directory = os.path.join(self.directory, "new_folder")
        bannin = Bannin(
            directory=directory,
            password=self.password,
            salt_filename="FolderKey.key",
            extensions=[".txt", ".mp3"],
        )
        bannin.encrypt()

        self.remove_directory = os.path.join(directory, "encrypted_new_folder")
        salt_filepath = os.path.join(self.remove_directory, "FolderKey.key")
        encrypted_files = [
            file for file in os.listdir(self.remove_directory) if file.endswith(".enc")
        ]

        self.assertTrue(os.path.isdir(self.remove_directory))
        self.assertTrue(os.path.isfile(salt_filepath))
        self.assertEqual(len(encrypted_files), 1)

    def test_encrypt_empty_directory(self):
        self.remove_directory = os.path.join(self.directory, "empty_directory")
        os.mkdir(self.remove_directory)
        self.assertTrue(os.path.isdir(self.remove_directory))

        bannin = Bannin(
            directory=self.remove_directory,
            password=self.password,
            salt_filename="FolderKey.key",
        )
        bannin.encrypt()

        encrypted_directory = os.path.join(
            self.remove_directory, "encrypted_empty_directory"
        )
        self.assertFalse(os.path.isfile(encrypted_directory))

    def tearDown(self):
        if self.remove_directory:
            shutil.rmtree(self.remove_directory)


class TestDecryptData(TestCase):
    def setUp(self):
        self.directory = "./tests/dummy_files/encrypted_folder"
        self.password = "password"
        self.remove_file = None

    def test_decrypt_file(self):
        bannin = Bannin(
            directory=self.directory,
            password=self.password,
            filename="sample.txt.enc",
            salt_filename="FolderKey.key",
        )
        bannin.decrypt()

        self.remove_file = os.path.join(self.directory, "sample.txt")
        self.assertTrue(os.path.isfile(self.remove_file))
        with open(self.remove_file, "rb") as file:
            file_data = file.read()
            self.assertEqual(file_data, b"Bannin test sample file.\n")

    def test_decrypt_file_invalid_data(self):
        bannin = Bannin(
            directory=self.directory,
            password=self.password,
            filename="sample.txt.enc",
            salt_filename="fake.file",
        )
        with self.assertRaises(ValueError):
            bannin.decrypt()

        bannin = Bannin(
            directory=self.directory,
            password=self.password,
            filename="sample.txt",
            salt_filename="FolderKey.key",
        )
        with self.assertRaises(ValueError):
            bannin.decrypt()
        filepath = os.path.join(self.directory, "sample.txt")
        self.assertFalse(os.path.isfile(filepath))

    def test_decrypt_directory(self):
        bannin = Bannin(
            directory=self.directory,
            password=self.password,
            salt_filename="FolderKey.key",
        )
        bannin.decrypt()

        self.remove_file = os.path.join(self.directory, "sample.txt")
        self.assertTrue(os.path.isfile(self.remove_file))
        with open(self.remove_file, "rb") as file:
            file_data = file.read()
            self.assertEqual(file_data, b"Bannin test sample file.\n")

    def tearDown(self):
        if self.remove_file:
            os.remove(self.remove_file)
