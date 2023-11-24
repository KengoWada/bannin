import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from getpass import getpass

from cryptography.fernet import InvalidToken

from .utils import Bannin, get_directory_and_filename, read_file_data

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
    args = vars(parser.parse_args())
    password = getpass()

    directory = args.get("directory")
    filename = args.get("filename")
    filepath = args.get("filepath")
    salt_filepath = args.get("salt_filepath")
    salt_filename = args.get("salt_filename")
    extensions = args.get("extensions").split(",")
    salt = None

    try:
        directory_, filename_ = get_directory_and_filename(
            directory=directory, filename=filename, filepath=filepath
        )
    except ValueError as error:
        print(str(error))
        return

    if salt_filepath is not None:
        if not os.path.isfile(salt_filepath):
            print("Invalid salt file path provided.")
            return

        salt = read_file_data(salt_filepath)

    bannin = Bannin(
        directory=directory_,
        password=password,
        filename=filename_,
        salt=salt,
        salt_filename=salt_filename,
        extensions=extensions,
    )

    if args.get("action") == "encrypt":
        bannin.encrypt()
        print("Done.")
        return

    try:
        bannin.decrypt()
    except InvalidToken:
        print("Invalid password or salt provided.")
    else:
        print("Done.")


if __name__ == "__main__":
    main()
