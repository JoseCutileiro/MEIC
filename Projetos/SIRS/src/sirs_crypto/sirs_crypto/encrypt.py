from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import os
import hashlib

def digest(text):
    hasher = hashlib.sha256()
    hasher.update(text.encode('utf-8'))
    hash = hasher.hexdigest()
    return hash

def encrypt_text(plaintext: str, key: bytes) -> dict[str, str]:
    """
    Encrypts text using AES and CBC mode.

    Parameters:
    ``plaintext`` (str): Text to encrypt.
    ``key`` (bytes): Key to be used.

    Returns:
    ``dict[str, str]``: Encrypted data and initialization vector (IV) in base64.

    Raises:
    ValueError: If the key length is not 32 bytes for AES.
    """

    if len(key) != 32:
        raise ValueError("Key must be 32 bytes for AES")

    iv = os.urandom(16)

    encryptor = Cipher(
                algorithms.AES(key), 
                modes.CBC(iv)).encryptor()

    # Convert plaintext to bytes and add padding
    data = plaintext.encode()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Encode the encrypted data to Base64
    encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
    encoded_iv = base64.b64encode(iv).decode('utf-8')
    
    hash_data = digest(plaintext + str(key.hex()))

    return {
        "Encrypted_data" : encoded_data,
        "IV" : encoded_iv,
        "Digest": hash_data
    }
