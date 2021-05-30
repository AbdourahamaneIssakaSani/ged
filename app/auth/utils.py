import binascii
import hashlib
import os
from app.models import User


def email_is_unique(email):
    user = User.query.filter_by(email=email).first()
    print(email, user)
    if user:
        return False
    return True


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt,
        100000
    )
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    password_hash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    password_hash = binascii.hexlify(password_hash).decode('ascii')
    return password_hash == stored_password
