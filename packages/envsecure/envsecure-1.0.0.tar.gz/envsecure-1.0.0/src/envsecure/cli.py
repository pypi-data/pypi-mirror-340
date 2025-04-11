import argparse
from envsecure.core import generate_key, encrypt_file, decrypt_file

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt .env files securely.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate-key
    parser_key = subparsers.add_parser("generate-key", help="Generate a new AES-256 encryption key")

    # encrypt
    parser_encrypt = subparsers.add_parser("encrypt", help="Encrypt a file")
    parser_encrypt.add_argument("input", help="Path to the input file (e.g., .env)")
    parser_encrypt.add_argument("output", help="Path to write the encrypted file")
    parser_encrypt.add_argument("key", help="Base64-encoded key")

    # decrypt
    parser_decrypt = subparsers.add_parser("decrypt", help="Decrypt a file")
    parser_decrypt.add_argument("input", help="Path to the encrypted file")
    parser_decrypt.add_argument("output", help="Path to write the decrypted file")
    parser_decrypt.add_argument("key", help="Base64-encoded key")

    args = parser.parse_args()

    if args.command == "generate-key":
        print(generate_key())
    elif args.command == "encrypt":
        encrypt_file(args.input, args.output, args.key)
        print(f"Encrypted {args.input} -> {args.output}")
    elif args.command == "decrypt":
        decrypt_file(args.input, args.output, args.key)
        print(f"Decrypted {args.input} -> {args.output}")
