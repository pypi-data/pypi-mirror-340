from envsecure.core import generate_key, encrypt_file, decrypt_file
import tempfile
import os

def test_encryption_decryption():
    key = generate_key()
    test_data = b"SECRET_ENV_VAR=VALUE\n"

    with tempfile.NamedTemporaryFile(delete=False) as tf_in:
        tf_in.write(test_data)
        input_path = tf_in.name

    encrypted_path = input_path + ".enc"
    decrypted_path = input_path + ".dec"

    encrypt_file(input_path, encrypted_path, key)
    decrypt_file(encrypted_path, decrypted_path, key)

    with open(decrypted_path, "rb") as f:
        assert f.read() == test_data

    os.remove(input_path)
    os.remove(encrypted_path)
    os.remove(decrypted_path)
