from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
import string
import secrets
import os
def random_string(size):        
        letters = string.ascii_lowercase+string.ascii_uppercase+string.digits            
        return ''.join(secrets.choice(letters) for i in range(size))
generated_salt = os.environ.get('SALT', random_string(2048).encode())
def generate_key_from_string(string_key):
    # Derive a cryptographic key from the input string key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=generated_salt,
        iterations=100000,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(string_key.encode()))
    return key

def encrypt_string(input_string, string_key):
    key = generate_key_from_string(string_key)
    fernet = Fernet(key)
    return fernet.encrypt(input_string.encode()).decode()

def decrypt_string(encrypted_string, string_key):
    key = generate_key_from_string(string_key)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_string.encode()).decode()
