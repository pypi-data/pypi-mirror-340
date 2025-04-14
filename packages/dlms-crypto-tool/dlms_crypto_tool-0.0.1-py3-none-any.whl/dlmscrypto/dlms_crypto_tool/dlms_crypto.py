import os
from binascii import unhexlify
from pydoc import plaintext

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Define security headers for different operations
SECURITY_HEADER = {

    'auth': "10", # Used for authentication AAD header
    'data': "30"  # Used for encrypt/decrypt AAD header
}

def create_iv(system_title: str, frame_counter: str) -> bytes:
    """
    Create an IV by concatenating the system title and frame counter.
    Both inputs are expected as hex strings.

    :param system_title: Hex string representing the system title.
    :param frame_counter: Hex string representing the frame counter.
    :return: The IV as bytes.

    Note: The concatenation mus yeld the expected byte length typically 12 bytes for AES-GCM)
    """

    return unhexlify(system_title + frame_counter)

def encrypt_apdu(system_title: str, frame_counter: str, encryption_key: str,
                 additional_auth_data: str, plaintext: str) -> str:

    """
    Encrypt an APDU message

    :param system_title: Hex string representing the system title.
    :param frame_counter:  Hex string representing the frame counter.
    :param encryption_key: Hex string encryption key.
    :param additional_auth_data: Additional authentication data (hex string without header)
    :param plaintext: Hex string of the APDU to encrypt.
    :return: A hex string containing the ciphertext with the authentication tag appended.
    """

    iv = create_iv(system_title, frame_counter)
    aesgcm = AESGCM(unhexlify(encryption_key))
    aad = unhexlify(SECURITY_HEADER['data'] + additional_auth_data)
    cipheredtext_with_tag = aesgcm.encrypt(iv, unhexlify(plaintext), aad)

    return cipheredtext_with_tag.hex()

def decrypt_apdu(system_title: str, frame_counter: str, encryption_key: str,
                 additional_auth_data: str, ciphertext_with_tag: str) -> str:

    """
    Decrypt an APDU message
    
    :param system_title: Hex string representing the system title. 
    :param frame_counter: Hex string representing the frame counter.
    :param encryption_key: Hex string encryption key.
    :param additional_auth_data: Additional authentication data (hex string without header).
    :param ciphertext_with_tag: Hex string of the cipheretext with appended authentication tag.
    :return: A hex string of the decrypted APDU.
    """

    iv = create_iv(system_title, frame_counter)
    aesgcm = AESGCM(unhexlify(encryption_key))
    aad = unhexlify(SECURITY_HEADER['data'] + additional_auth_data)
    ciphertext_with_tag = unhexlify(ciphertext_with_tag)
    plaintext = aesgcm.encrypt(iv, ciphertext_with_tag, aad)

    return plaintext.hex()

def auth_apdu(system_title: str, frame_counter: str, encryption_key: str,
              authentication_key: str, stoc: str) -> str:

    """
    Generate an authentication tag for an APDU

    :param system_title: Hex string representing the system title.
    :param frame_counter: Hex string representing the frame counter.
    :param encryption_key: Hex string encryption key.
    :param authentication_key: Hex string authentication key.
    :param stoc: Hex string value.
    :return: A truncated authentication tag as a hex string.
    """

    iv = create_iv(system_title, frame_counter)
    aesgcm = AESGCM(unhexlify(encryption_key))
    aad = unhexlify(SECURITY_HEADER['auth'] + authentication_key + stoc)

    # Encrypt an empty plaintext; the output is the tag appended to an empty ciphertext.
    tag_with_empty_ciphertext = aesgcm.encrypt(iv, b'', aad)

    return tag_with_empty_ciphertext.hex()[:-8]