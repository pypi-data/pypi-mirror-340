import argparse
import os
import logging
from dlms_crypto import encrypt_apdu, decrypt_apdu, auth_apdu

def read_file_content(file_path: str) -> str:

    """ Read and return the content of the given file, stripped of surrounding whitespace. """
    with open(file_path, 'r') as f:

        return f.read().strip()

def write_file_content(file_path: str, content: str):

    """ Write the provided content to the specified file. """
    with open(file_path, 'w') as f:

        f.write(content)

def main():

    parser = argparse.ArgumentParser(
        description= " Tool for encrypting, decrypting, and authenticating DLMS APDU",
        prog= 'DLMS CLI'
    )

    parser.add_argument(
        '-e', '--enc', nargs=5,
        metavar=('SYSTEM_TITEL', 'FRAME_COUNTER', 'ENCRYPTION_KEY', 'AAD', 'APDU'),
        help= 'Encrypt APDU (expecting hex strings for all arguments)'
    )

    parser.add_argument(
        '-d', '--dec', nargs=5,
        metavar=('SYSTEM_TITEL', 'FRAME_COUNTER', 'ENCRYPTION_KEY', 'AAD', 'APDU'),
        help= 'Decrypt APDU (expecting hex strings for all arguments)'
    )

    parser.add_argument(
        '-a', '--auth', nargs=5,
        metavar=('SYSTEM_TITLE', 'FRAME_COUNTER', 'ENCRYPTION_KEY', 'AUTHENTICATION_KEY', 'STOC'),
        help='Authenticate APDU (expecting hex strings for all arguments)'
    )
    parser.add_argument(
        '-k', '--key', action='store_true',
        help='Generate a random 16-byte encryption key (displayed in hex)'
    )
    parser.add_argument(
        '--infile', type=str, help='Path to input file for APDU/ciphertext (hex string)'
    )
    parser.add_argument(
        '--outfile', type=str, help='Path to output file to save the result'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable verbose mode for additional logging'
    )

    args = parser.parse_args()

    # Configure logging based on the verbose flag.
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    if args.key:

        key = os.urandom(16).hex()
        logging.debug(f"Generated encryption key: {key}")
        print(f"Encryption Key: {key}")

    result_output = None

    if args.enc:

        system_title, frame_counter, encryption_key, aad, apdu = args.enc

        if args.infile:

            logging.debug(f"Reading APDU from file: {args.infile}")
            apdu = read_file_content(args.infile)

        logging.debug("Starting encryption process")
        encrypted_hex = encrypt_apdu(system_title, frame_counter, encryption_key, aad, apdu)

        # The last 32 hex digits represent the authentication tag.
        encrypted_apdu = encrypted_hex[:-32]
        auth_tag = encrypted_hex[-32:]
        result_output = f"Encrypted APDU: {encrypted_apdu}\nAuthentication TAG: {auth_tag}"
        logging.debug("Encryption process completed")

    if args.dec:

        system_title, frame_counter, encryption_key, aad, ciphertext = args.dec

        if args.infile:

            logging.debug(f"Reading ciphertext from file: {args.infile}")
            ciphertext = read_file_content(args.infile)

        logging.debug("Starting decryption process")

        try:

            plaintext_hex = decrypt_apdu(system_title, frame_counter, encryption_key, aad, ciphertext)
            result_output = f"Decrypted APDU: {plaintext_hex[:-32]}"
            logging.debug("Decryption process completed successfully")

        except Exception as e:

            result_output = f"Decryption failed: {e}"
            logging.error("Decryption process failed", exc_info=True)

    if args.auth:

        system_title, frame_counter, encryption_key, authentication_key, stoc = args.auth
        logging.debug("Starting authentication process")
        tag = auth_apdu(system_title, frame_counter, encryption_key, authentication_key, stoc)
        result_output = f"Authentication TAG: {tag}"
        logging.debug("Authentication process completed")

    if result_output:

        if args.outfile:

            logging.debug(f"Writing output to file: {args.outfile}")
            write_file_content(args.outfile, result_output)

        else:

            print(result_output)

if __name__ == "__main__":
    main()
