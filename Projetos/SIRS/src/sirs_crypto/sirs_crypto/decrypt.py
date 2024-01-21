from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import hashlib
import json
import os
from datetime import datetime

def get_seconds_of_year():
    # Get the current time
    current_time = datetime.now()

    # Get the start of the current year
    start_of_year = datetime(current_time.year, 1, 1)

    # Calculate the difference in seconds between current time and start of the year
    seconds_of_year = (current_time - start_of_year).total_seconds()

    return int(seconds_of_year)

def convert_single_quoted_json(single_quoted_json):
    # Replace single quotes with double quotes
    double_quoted_json = single_quoted_json.replace("'", "\"")
    
    # Load the corrected JSON string
    try:
        parsed_json = json.loads(double_quoted_json)
        return parsed_json
    except json.decoder.JSONDecodeError as e:
        return f"Error: {e}"

def digestFunc(text):
    hasher = hashlib.sha256()
    hasher.update(text.encode('utf-8'))
    hash = hasher.hexdigest()
    return hash

def decrypt_text(encoded_data: dict[str, str], key: bytes,current_fresh_token: int) -> str:
    """
    Decrypts text using AES and CBC mode.

    Parameters:
    ``encoded_data`` (dict[str, str]): Base64 encoded encrypted data, initialization vector (IV) and hash.
    ``key`` (bytes): Key to be used for decryption (must be 32 bytes for AES).

    Returns:
    str: Decrypted plaintext.

    Raises:
    ValueError: If the key length is not 32 bytes for AES.
    """

    if len(key) != 32:
        raise ValueError("Key must be 32 bytes for AES")

    encrypted_data = encoded_data['Encrypted_data']
    encoded_iv = encoded_data['IV']
    digest = encoded_data['Digest']

    # Decode the Base64 encoded data and IV
    try:
        encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
        iv = base64.b64decode(encoded_iv.encode('utf-8'))

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Convert decrypted bytes to plaintext
        plaintext = decrypted_data.decode('utf-8')
    except:
        raise ValueError("(ERROR) Invalid format!")

    new_digest = digestFunc(plaintext + str(key.hex()))

    if (new_digest != digest):
        raise ValueError("(ERROR) Wrong digest!")


    data = convert_single_quoted_json(plaintext)
        
    if (data["fresh_token"] < current_fresh_token):
        raise ValueError("(ERROR) This message has a old fresh token")
    
    if (data["fresh_token"] > get_seconds_of_year()):
        raise ValueError("(ERROR) Your OS clock is invalid, that is unsupported")
    
    del data["fresh_token"]
    
    return json.dumps(data)