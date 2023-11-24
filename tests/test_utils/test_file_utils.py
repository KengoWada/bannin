import os
from unittest import TestCase

from cryptography.fernet import Fernet

from bannin.utils import (
    DEFAULT_SALT_FILE_NAME,
    generate_fernet_key,
    generate_salt,
    get_directory_and_filename,
    read_file_data,
    write_to_file,
)


class TestReadWriteToFile(TestCase):
    def setUp(self):
        self.filename = "./tests/test_utils/testfile.txt"

    def test_read_file_data(self):
        data = b"Testing bannin read file data"
        with open(self.filename, "wb") as file:
            file.write(data)

        self.assertTrue(os.path.isfile(self.filename))
        file_data = read_file_data(self.filename)
        self.assertEqual(file_data, data)

    def test_write_to_file(self):
        data = b"Testing bannin write data"
        write_to_file(self.filename, data)
        self.assertTrue(os.path.isfile(self.filename))
        with open(self.filename, "rb") as file:
            file_data = file.read()
            self.assertEqual(file_data, data)

    def tearDown(self):
        os.remove(self.filename)


class TestSaltAndFernetKeyGeneration(TestCase):
    def setUp(self):
        self.salt_file_dir = "./tests/test_utils"
        self.salt_filepath = os.path.join(self.salt_file_dir, DEFAULT_SALT_FILE_NAME)

    def test_generate_salt(self):
        salt = generate_salt(self.salt_file_dir)

        self.assertTrue(os.path.isfile(self.salt_filepath))
        with open(self.salt_filepath, "rb") as file:
            data = file.read()
            self.assertEqual(data, salt)

    def test_generate_salt_custom_name(self):
        filename = "Secret.key"
        salt = generate_salt(self.salt_file_dir, filename)
        self.salt_filepath = os.path.join(self.salt_file_dir, filename)

        self.assertTrue(os.path.isfile(self.salt_filepath))
        with open(self.salt_filepath, "rb") as file:
            data = file.read()
            self.assertEqual(data, salt)

    def test_generate_fernet_key(self):
        salt = Fernet.generate_key()
        fernet_key = generate_fernet_key("password", salt)
        self.assertTrue(isinstance(fernet_key, bytes))
        self.assertEqual(len(fernet_key), 44)

        new_fernet_key = generate_fernet_key("password", salt)
        self.assertTrue(isinstance(new_fernet_key, bytes))
        self.assertEqual(len(new_fernet_key), 44)
        self.assertEqual(new_fernet_key, fernet_key)

        new_salt = Fernet.generate_key()
        invalid_salt_fernet_key = generate_fernet_key("password", new_salt)
        self.assertTrue(isinstance(invalid_salt_fernet_key, bytes))
        self.assertEqual(len(invalid_salt_fernet_key), 44)
        self.assertNotEqual(invalid_salt_fernet_key, fernet_key)

        invalid_password_fernet_key = generate_fernet_key("fake_password", salt)
        self.assertTrue(isinstance(invalid_password_fernet_key, bytes))
        self.assertEqual(len(invalid_password_fernet_key), 44)
        self.assertNotEqual(invalid_password_fernet_key, fernet_key)

    def tearDown(self):
        if os.path.isfile(self.salt_filepath):
            os.remove(self.salt_filepath)


class TestGetDirectoryDetails(TestCase):
    def setUp(self):
        self.directory = "./tests/dummy_files/"
        self.filename = "sample.txt"
        self.filepath = os.path.join(self.directory, self.filename)

    def test_get_file_directory_details(self):
        directory, filename = get_directory_and_filename(filepath=self.filepath)
        self.assertEqual(directory, self.directory[:-1])
        self.assertEqual(filename, self.filename)
        self.assertEqual(os.path.join(directory, filename), self.filepath)

        directory, filename = get_directory_and_filename(
            directory=self.directory, filename=self.filename
        )
        self.assertEqual(directory, self.directory[:-1])
        self.assertEqual(filename, self.filename)
        self.assertEqual(os.path.join(directory, filename), self.filepath)

        directory, filename = get_directory_and_filename()
        self.assertIsNone(filename)
        self.assertEqual(directory, os.getcwd())

    def test_get_file_directory_details_invalid_data(self):
        data = {"directory": "./fake_dir"}
        with self.assertRaises(ValueError):
            get_directory_and_filename(**data)

        data = {"directory": self.directory, "filename": "fake.file"}
        with self.assertRaises(ValueError):
            get_directory_and_filename(**data)

        data = {"filepath": os.path.join("./fake_dir", "fake.file")}
        with self.assertRaises(ValueError):
            get_directory_and_filename(**data)
