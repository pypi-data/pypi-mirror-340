import base64
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY_SIZE = 32  # AES-256
IV_SIZE = 16   # AES block size

def generate_key() -> str:
    key = os.urandom(KEY_SIZE)
    return base64.urlsafe_b64encode(key).decode()

def encrypt_file(input_path: str, output_path: str, key: str):
    key_bytes = base64.urlsafe_b64decode(key.encode())
    iv = os.urandom(IV_SIZE)
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, "rb") as f:
        data = f.read()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_path, "wb") as f:
        f.write(iv + encrypted)

def decrypt_file(input_path: str, output_path: str, key: str):
    key_bytes = base64.urlsafe_b64decode(key.encode())

    with open(input_path, "rb") as f:
        iv = f.read(IV_SIZE)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    with open(output_path, "wb") as f:
        f.write(decrypted)
