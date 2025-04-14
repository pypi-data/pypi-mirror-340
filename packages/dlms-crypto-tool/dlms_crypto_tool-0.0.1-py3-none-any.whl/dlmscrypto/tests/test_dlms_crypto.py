import sys
import os

# Determine the absolute path of the project root.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert it at the beginning of sys.path so that Python see it first.
sys.path.insert(0, project_root)

# Import package
from dlms_crypto_tool.dlms_crypto import encrypt_apdu, decrypt_apdu, auth_apdu, create_iv
import unittest

class TestDLMSCrypto(unittest.TestCase):

    def setUp(self):

        self.system_title = "5249435249435249" # 8 bytes hex
        self.frame_counter = "80000001" # 4 bytes
        self.encryption_key = "454E4352595054494F4E4B45594B4559" # 16 bytes
        self.aad = "41555448454E5449434154494F4E4B45" # Additional auth data (4 bytes)
        self.plaintext = "c001810001000060010aff0200" # Sample APDU

    def test_encryption_decrypt(self):

        encrypted_text = encrypt_apdu(
            self.system_title,
            self.frame_counter,
            self.encryption_key,
            self.aad,
            self.plaintext
        )

        decrypted_hex = decrypt_apdu(
            self.system_title,
            self.frame_counter,
            self.encryption_key,
            self.aad,
            encrypted_text[:-32]
        )

        self.assertEqual(decrypted_hex[:-32], self.plaintext, "Decrypted APDU does not match the original!")

    def test_auth_apdu_length(self):

        tag = auth_apdu(
            self.system_title,
            self.frame_counter,
            self.encryption_key,
            "41555448454E5449434154494F4E4B45", # Sample authentication key
            "0de63f2331a09aa85e8830f5f3" # Sample StoC
        )

        self.assertEqual(len(tag), 24, "Authentication tag len is not as expected")

    def test_create_iv(self):

        iv = create_iv(self.system_title, self.frame_counter)

        self.assertEqual(len(iv), 12, "IV length is not 12 bytes")

if __name__ == '__main':

    unittest.main()
