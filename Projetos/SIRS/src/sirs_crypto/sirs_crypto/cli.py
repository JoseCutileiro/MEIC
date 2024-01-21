import argparse
import json
from sirs_crypto import encrypt, decrypt

def protect(args):
    if not (args.input_file and args.output_file and args.key_file):
        print("Please provide input-file, output-file, and key-file arguments for the 'protect' command.")
        return

    content = ""
    key = b''

    try:
        with open(args.input_file, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("The input-file does not exist or the path is incorrect.")
    except IOError:
        print("An error occurred while reading the input-file.")

    try:
        with open(args.key_file, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        print("The key-file does not exist or the path is incorrect.")
    except IOError:
        print("An error occurred while reading the key-file.")

    encrypt_info = encrypt.encrypt_text(content, key) 
    
    try:
        with open(args.output_file, 'w') as file:
            json.dump(encrypt_info, file, indent=4)
    except IOError:
        print("An error occurred while writing the file.")

    message = f"Protect {args.input_file} to {args.output_file}."
    print(message)

def check(args):
    if args.input_file:
        message = f"Check file {args.input_file}!."
        print(message)
    else:
        print("Please provide input-file for 'check' commad.")

def unprotect(args):
    if not (args.input_file and args.output_file and args.key_file):
        print("Please provide input-file, output-file, and key-file arguments for the 'protect' command.")
        return

    content = {}
    key = b''

    try:
        with open(args.input_file, 'r') as file:
            content = json.load(file)
    except FileNotFoundError:
        print("The input-file does not exist or the path is incorrect.")
    except IOError:
        print("An error occurred while reading the input-file.")

    try:
        with open(args.key_file, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        print("The key-file does not exist or the path is incorrect.")
    except IOError:
        print("An error occurred while reading the key-file.")

    try:
        decrypt_info = decrypt.decrypt_text(content, key) 

    except ValueError as ve:
        print("ValueError:",ve)
        return 
    
    try:
        with open(args.output_file, 'w') as file:
            file.write(decrypt_info)
    except IOError:
        print("An error occurred while writing the file.")
        return

    message = f"Unprotect {args.input_file} to {args.output_file}."
    print(message)

def main():
    parser = argparse.ArgumentParser(description='Simple Command Line App')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand', help='Available subcommands')

    # Subparser for 'help' command
    help_parser = subparsers.add_parser('help', help='Display help information')
    help_parser.set_defaults(action='help')

    # Subparser for 'protect' command
    protect_parser = subparsers.add_parser('protect', help='Add security to a document')
    protect_parser.add_argument('input_file', type=str, help='input-file')
    protect_parser.add_argument('output_file', type=str, help='output-file')
    protect_parser.add_argument('key_file', type=str, help='key-file')
    protect_parser.set_defaults(func=protect)

    # Subparser for 'check' command
    check_parser = subparsers.add_parser('check', help='Verify security of a document')
    check_parser.add_argument('input_file', type=str, help='input-file')
    check_parser.set_defaults(func=check)

    # Subparser for 'unprotect' command
    unprotect_parser = subparsers.add_parser('unprotect', help='Remove security from a document')
    unprotect_parser.add_argument('input_file', type=str, help='input-file')
    unprotect_parser.add_argument('output_file', type=str, help='output-file')
    unprotect_parser.add_argument('key_file', type=str, help='key-file')
    unprotect_parser.set_defaults(func=unprotect)

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


