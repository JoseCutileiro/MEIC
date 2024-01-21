import psycopg2
import json
import random
import secrets
import os
import sys
sys.path.append("/home/kali/t54-guilherme-jose-guilherme/src/sirs_crypto")
from sirs_crypto import encrypt

KEYS_DIR = 'keys'
SERVER_KEY = 'alpha_server.key'

directory_path = 'keys/'


# Get all files and subdirectories in the directory
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)  # Remove file
        elif os.path.isdir(file_path):
            os.rmdir(file_path)  # Remove directory
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")



def genName():

    random_name = random.choice(names)
    random_surname = random.choice(surnames)

    full_name = f"{random_name}_{random_surname}"
    return full_name

def genKey(name):
    aes_key = secrets.token_bytes(32)
    with open(KEYS_DIR + '/secret_' + name +  ".key", "wb") as key_file:
        key_file.write(aes_key)

    return aes_key 

def genMusicOwning(n):
    ret = []
    for i in range(n):
        if (random.randint(0,4) == 0):
            ret.append(i+1)
    return ret

def getMemberRandUserIds(i):
    ret = []
    for _ in range(5):
        if (random.randint(0,4) == 0):
                r = random.randint(0,100)
                if (r != i):
                    ret.append(r)
    
    return [ret]

with open('names.txt', 'r') as names_file:
    names = names_file.read().split(' ')

with open('surnames.txt', 'r') as surnames_file:
    surnames = surnames_file.read().split(' ')

if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

conn = psycopg2.connect(
    dbname='sirs',
    user='musicstore',
    password='m3S8iBg@',
    host='localhost'
)

cursor = conn.cursor()

musics = os.listdir('musics')

sample_users = []
for i in range(100):
    nu = {}
    nu['username'] = genName()
    nu['key_value'] = genKey(nu['username'])
    nu['music_id'] = genMusicOwning(len(musics))
    sample_users += [nu,]

sample_music = []
for file_name in musics:
    with open('musics/' + file_name, 'r') as file:
        json_data = json.load(file)
    sample_music += [json_data,]

query = """
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS musics CASCADE;
DROP TABLE IF EXISTS family CASCADE;

CREATE TABLE musics (
    music_id SERIAL PRIMARY KEY,
    music_title VARCHAR(1024),
    music_data JSON
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(1024),
    key_value JSON,
    music_ids INTEGER[]
);

CREATE TABLE family (
    family_id SERIAL PRIMARY KEY,
    members_ids INTEGER[]
);
"""

aes_key = secrets.token_bytes(32)
with open(KEYS_DIR + '/' + SERVER_KEY, "wb") as key_file:
    key_file.write(aes_key)

cursor.execute(query)

with open(KEYS_DIR + '/' + SERVER_KEY, 'rb') as key_file:
    server_key = key_file.read()

for music in sample_music:
    
    music['fresh_token'] = 77
    
    mc = str(music)
    
    mc_enc = encrypt.encrypt_text(mc, server_key)    
    
    with open('output_file.txt', 'w') as file:
        file.write(json.dumps(mc_enc,indent=4))
    
    cursor.execute(
        "INSERT INTO musics (music_data, music_title) VALUES (%s, %s)",
        (json.dumps(mc_enc,indent=4), music['mediaContent']['title'])
    )

for user in sample_users:
    
    key_data = {
        'key': user['key_value'].hex(),
        'fresh_token': 77
    }
    
    
    ken = encrypt.encrypt_text(str(key_data) ,server_key)
    #user['key_value']
    
    cursor.execute(
        "INSERT INTO users (username, key_value, music_ids) VALUES (%s, %s, %s)",
        (user['username'], json.dumps(ken,indent=4), user['music_id'])
    )
    
for i in range(len(sample_users)):
    cursor.execute(
        "INSERT INTO family (members_ids) VALUES (%s)",
        (getMemberRandUserIds(i))
    )

conn.commit()
cursor.close()
conn.close()

print("Database successfully populated!")
