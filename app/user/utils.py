from cryptography.fernet import Fernet
from flask_uploads import AllExcept, EXECUTABLES, SCRIPTS

ALLOWED_FILES = AllExcept(SCRIPTS + EXECUTABLES)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES


def read_encryption_key():
    with open('file_key.key', 'rb') as file_key:
        stored_key = file_key.read()
        file_key.close()
    return Fernet(stored_key)


def generate_fernet_key():
    k = Fernet.generate_key()
    with open('file_key.key', 'wb') as new_file_key:
        new_file_key.write(k)
        new_file_key.close()
    return k


def encrypt_file_content(filename_with_path):
    with open(filename_with_path, 'rb') as file_to_encrypt:
        data_to_encrypt = file_to_encrypt.read()
        file_to_encrypt.close()

    encrypted_data = read_encryption_key().encrypt(data_to_encrypt)

    with open(filename_with_path, 'wb') as file_encrypted:
        file_encrypted.write(encrypted_data)
        file_encrypted.close()


def decrypt_file_content(filename_with_path):
    with open(filename_with_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
        encrypted_file.close()

    decrypted_data = read_encryption_key().decrypt(encrypted_data)

    with open(filename_with_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
        decrypted_file.close()

# //TODO: Admin must allow all files extensions in the SETTINGS
