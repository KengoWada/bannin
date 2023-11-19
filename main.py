import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
# from getpass import getpass

from cryptography.fernet import InvalidToken

from utils import decrypt_data, encrypt_data, get_file_directory_details, read_file_data

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument("action", help="Action to perform.", choices=["encrypt", "decrypt"])
parser.add_argument("-f", "--filepath", help="File path to encrypt or decrypt.")
parser.add_argument(
    "-F",
    "--filename",
    help=(
        "File name to encrypt or decrypt. "
        "Uses current working directory. "
        "Will be ignored if --filepath is set."
    ),
)
parser.add_argument(
    "-d",
    "--dir",
    dest="directory",
    help="Directory path to encrypt or decrypt.",
)
parser.add_argument(
    "-s",
    "--salt-filepath",
    help="Salt file name path to use for encrypttion or decryption.",
)
parser.add_argument(
    "-S",
    "--salt-filename",
    default="FolderKey.key",
    help="Salt file name to use for encryption.",
)
parser.add_argument(
    "-e",
    "--extensions",
    help="A list of comma separated file extensions to encrypt. Ignored when filepath is set.",
    default="",
)


def main():
    # password = getpass()
    args = vars(parser.parse_args())

    data = {
        "directory": args.get("directory"),
        "filename": args.get("filename"),
        "filepath": args.get("filepath"),
    }
    try:
        base_dir, filename = get_file_directory_details(data)
    except ValueError as error:
        print(str(error))
        return

    if base_dir[-1] == "/":
        base_dir = base_dir[:-1]

    salt = None
    salt_filepath = args.get("salt_filepath")
    if salt_filepath:
        if not os.path.isfile(salt_filepath):
            print("Invalid salt file path provided.")
            return
        salt = read_file_data(salt_filepath)

    if args.get("action") == "encrypt":
        data = {
            "dirname": base_dir,
            "password": "password",
            "filename": filename,
            "salt": salt,
            "salt_filename": args.get("salt_filename"),
            "extensions": args.get("extensions").split(","),
        }
        encrypt_data(**data)
        return

    if args.get("action") == "decrypt":
        data = {
            "dirname": base_dir,
            "password": "password",
            "filename": filename,
            "salt": salt,
            "salt_filename": args.get("salt_filename"),
        }
        try:
            decrypt_data(**data)
        except InvalidToken:
            print("Invalid password or salt provided.")


if __name__ == "__main__":
    main()
