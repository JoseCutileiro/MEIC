import hashlib
import json
import base64

from sirs_crypto import encrypt 

key_path = "keys/secret.key"

def base64JsonConverter(file_path): 
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    json_str = json.dumps(data)

    encoded_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

    return encoded_data

def base64Decode(data):
    decoded_data = base64.b64decode(data).decode('utf-8')
    print("DECODED DATA:" , decoded_data)
    
def digestFile(file_path):
    with open(file_path, 'r') as file:
        json_data = file.read()

    hasher = hashlib.sha256()
    hasher.update(json_data.encode('utf-8'))
    json_hash = hasher.hexdigest()
    return json_hash

def getJsonPlain(json_file):
    with open(json_file, 'r') as file:
        json_content = json.load(file)
        plaintext = json.dumps(json_content)

    return plaintext

def main():
    json_plain = getJsonPlain("data/data.json")

    # Fresh token TODO: Ver onde guardar isto
    json_data = json.loads(json_plain)
    json_data["fresh_token"] = 123
    json_plain = json.dumps(json_data, indent=4)
    
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
        data = encrypt.encrypt_text(json_plain,key)

    # Define the file name
    file_name = "data/dataSend.json"

    # Write the data to a JSON file
    with open(file_name, "w") as json_file:
        print(data)
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    main()
