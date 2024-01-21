import secrets

aes_key = secrets.token_bytes(32)

# Write the key to a file
with open("keys/secret.key", "wb") as key_file:
    key_file.write(aes_key)

print("Generated new  AES key with sucess!")