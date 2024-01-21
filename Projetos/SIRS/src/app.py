from flask import Flask, jsonify, request
from sirs_crypto import encrypt,decrypt
from datetime import datetime
import secrets

import random
import hashlib
import psycopg2
import os
import json

app = Flask(__name__)

app.config["last_time"] = 0

def genKey():
    current_directory = os.path.dirname(__file__)
    
    aes_key = secrets.token_bytes(32)
    with open(current_directory + "/codigoBD/keys/alpha_server.key", "wb") as key_file:
        key_file.write(aes_key)

    return aes_key 

def reset_master_key():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT users.username ,users.key_value
    FROM users 
    """
    cursor.execute(query)
    result = cursor.fetchall()

    old_key = load_key()
    new_key = genKey()

    for e in result:
        
        dec = decrypt.decrypt_text(json.loads(json.dumps(e[1])), old_key,1)
        
        key_data = {
        'key': json.loads(dec)["key"],
        'fresh_token': 77
        }
        
        ken = encrypt.encrypt_text(str(key_data) ,new_key)
        
        update_query = """
        UPDATE users
        SET key_value = %s
        WHERE username = %s
        """
        cursor.execute(update_query, (json.dumps(ken,indent=4), e[0]))
  
    query = """
    SELECT music_title ,music_data
    FROM musics
    """
    cursor.execute(query)
    result = cursor.fetchall()

    for e in result:
        
        dec = decrypt.decrypt_text(json.loads(json.dumps(e[1])), old_key,1)
        
        key_data = {
        "mediaContent": json.loads(dec)["mediaContent"],
        'fresh_token': 77
        }
        
        ken = encrypt.encrypt_text(str(key_data) ,new_key)
        
        update_query = """
        UPDATE musics
        SET music_data = %s
        WHERE music_title = %s
        """
        cursor.execute(update_query, (json.dumps(ken,indent=4), e[0]))  
  
    conn.commit()
        
    cursor.close()
    conn.close()
    
    return 0

def autoReset():

    # 10% chance reeset master password on any request
    if (random.randint(0,9) == 0):
        print("RESETED MASTER PASSWORD")
        reset_master_key()

def get_seconds_of_year():
    # Get the current time
    current_time = datetime.now()

    # Get the start of the current year
    start_of_year = datetime(current_time.year, 1, 1)

    # Calculate the difference in seconds between current time and start of the year
    seconds_of_year = (current_time - start_of_year).total_seconds()

    return int(seconds_of_year)

def load_key():
    
    current_directory = os.path.dirname(__file__)

    with open(current_directory + '/codigoBD/keys/alpha_server.key', 'rb') as key_file:
        return key_file.read()

def get_all_musics():
    return ["Crinch","Tetrix"]


def connect_to_db():
    conn = psycopg2.connect(
        dbname='sirs',
        user='musicstore',
        password='m3S8iBg@',
        host='192.168.2.4'  # Change this if your PostgreSQL server is running on a different host
    )
    return conn

def get_user_key(user_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT users.key_value
    FROM users 
    WHERE users.username = %s;
    """
    cursor.execute(query, (user_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is not None and len(result) > 0:
        value = result[0]
        
        dec = decrypt.decrypt_text(json.loads(json.dumps(value)), load_key(),1)
        return bytes.fromhex(json.loads(dec)["key"])
    else:
        return None

def encrypt_data(user_name, data):
    key = get_user_key(user_name)
    if key != None:
        data = encrypt.encrypt_text(data, key)

    return data

def get_music_name(music_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT music_title
    FROM musics
    WHERE music_id = %s
    """

    cursor.execute(query, (music_id,))
    music_name = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return music_name[0] if music_name else None

def get_musics(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT music_ids
    FROM users
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    music_names = [row[0] for row in cursor.fetchall()]    
    cursor.close()
    conn.close()

    return music_names[0]

def get_musics_name(user_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT music_ids
    FROM users
    WHERE username = %s
    """
    cursor.execute(query, (user_name,))
    music_ids = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return music_ids[0] if music_ids else None

def get_music_data_by_name(music_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT music_data
    FROM musics
    WHERE music_title = %s
    """

    cursor.execute(query, (music_id,))
    music_data = cursor.fetchone()[0]
    
    music_data = decrypt.decrypt_text(json.loads(json.dumps(music_data)), load_key(),1)
    
    cursor.close()
    conn.close()

    return music_data if music_data else None 

def valid_music(music_title):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT *
    FROM musics
    WHERE music_title = %s
    """

    cursor.execute(query, (music_title,))
    music_name = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return True if music_name else False

def valid_user(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT *
    FROM users
    WHERE username = %s
    """

    cursor.execute(query, (username,))
    music_name = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return True if music_name else False

def getUserId(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT user_id
    FROM users
    WHERE username = %s
    """

    cursor.execute(query, (username,))
    userId = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return userId[0] if userId else None 

def getUsername(_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT username
    FROM users
    WHERE user_id = %s
    """

    cursor.execute(query, (_id,))
    username = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return username[0] if username else None 

def getFamilyMembers(user_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT members_ids
    FROM family
    WHERE family_id = %s
    """

    user_id = getUserId(user_name)

    cursor.execute(query, (user_id,))
    
    if (not user_id):
        return None
    
    members = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    
    if (len(members[0]) == 0):
        return []
    
    return members[0] if members else None 

def getFamilies(username):
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    userID = getUserId(username)
    
    query = "SELECT family_id FROM family WHERE %s = ANY (members_ids)"
    
    cursor.execute(query, (userID,))
    

    family_ids = cursor.fetchall()

    cursor.close()
    conn.close()

    return family_ids

def getUserKey(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT key_value
    FROM users
    WHERE username = %s
    """

    cursor.execute(query, (username,))
    key = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if (not key):
        return None
    
    return key[0]


def getFamilyMusics(user_name):
    
    fams = getFamilies(user_name)
    
    
    ret = []
    for e in fams:
        ret += [getUsername(e[0]),]  
    
    musics = []
    
    for e in ret:
        musics_ids = get_musics_name(e)
        
        if (not musics_ids):
            pass
        else:
            musics += [get_music_name(music_id) for music_id in musics_ids]
    return set(musics)
            

@app.route('/list_musics/<user_name>', methods=['GET'])
def get_music_for_user(user_name):
    
    autoReset()
    
    if (not valid_user(user_name)):
        return jsonify({'error': 'Username not found'}), 404
    
    music_ids = get_musics_name(user_name)
    
    family_musics = getFamilyMusics(user_name)
    
    if music_ids or family_musics:
        music_names = [get_music_name(music_id) for music_id in music_ids ]
        music_names += list(family_musics)
        
        music_names = list(set(music_names))
        
        data = {"data": music_names, "fresh_token": 124}

        json_str = json.dumps(data, indent=4)
        return encrypt_data(user_name, json_str), 200
    else:
        return jsonify({'error': 'You cant acess any music yet'}), 404

@app.route('/download_music/<user_name>/<music_name>', methods=['GET'])
def download_music(user_name, music_name):
    
    autoReset()
    
    if (not valid_music(music_name)):
        return jsonify({'error': 'That music is not available on our platform'}), 404

    if (not valid_user(user_name)):
        return jsonify({'error': 'Username not found'}), 404
 
    music_ids = get_musics_name(user_name)
    
    family_musics = getFamilyMusics(user_name)
    
    musics_available = [get_music_name(music_id) for music_id in music_ids ]

    musics_available += list(family_musics)
    
    musics_available = list(set(musics_available))

    if (music_name in musics_available):
        music_data = get_music_data_by_name(music_name)

        data = {"data": music_data, "fresh_token": 124}
        json_str = json.dumps(data, indent=4)
        return encrypt_data(user_name, json_str), 200
    else:
        return jsonify({'error': 'You need to buy the music first'}), 405

@app.route('/family_members/<user_name>', methods=['GET'])
def family_members(user_name):
    
    autoReset()
    
    if (not valid_user(user_name)):
        return jsonify({'error': 'Username not found'}), 404
    
    members = getFamilyMembers(user_name)
    
    if (len(members) == 0):
        return jsonify({'error': 'You need to add members to your family'}), 403
    
    ret = []
    for e in members:
        
        ret += [getUsername(e),]
    
    
    data = {"data": ret, "fresh_token": 124}
    json_str = json.dumps(data, indent=4)
    return encrypt_data(user_name, json_str), 200

@app.route('/family_check/<user_name>', methods=['GET'])
def family_check(user_name):
    
    autoReset()

    if (not valid_user(user_name)):
        return jsonify({'error': 'Username not found'}), 404

    af = getFamilies(user_name)
    
    if (len(af) == 0):
        return jsonify({'error': 'No one wants to be your friend'}), 403
    
    ret = []
    for e in af:
        ret += [getUsername(e[0]),]
            
    data = {"data": ret, "fresh_token": 124}
    json_str = json.dumps(data, indent=4)
    return encrypt_data(user_name, json_str), 200

@app.route('/add_user_to_family/<user_name>', methods=['POST'])
def add_user_to_family(user_name):
    
    autoReset()
    
    try: 
        if request.is_json:
            enc_data = request.json

        connection = connect_to_db()
        cursor = connection.cursor()

        key = getUserKey(user_name)
        
        try:
            data = json.loads(decrypt.decrypt_text(enc_data, key,app.config["last_time"]))
            new_user_name = data["new_user"]
            app.config["last_time"] = get_seconds_of_year()
        except:
            return jsonify({'error': 'Wrong key provided'}), 403

        user_id = getUserId(user_name)
        new_user_id = getUserId(new_user_name)
    
        cursor.execute("SELECT members_ids FROM family WHERE family_id = %s", (user_id,))
        current_members = cursor.fetchone()

        
        if current_members:
            updated_members = current_members[0] + [new_user_id]
            

            cursor.execute("UPDATE family SET members_ids = %s WHERE family_id = %s", (updated_members, user_id))
            connection.commit()

            return jsonify({"message": f"User {new_user_id} added to family {user_id} successfully."})
        else:
            return jsonify({"error": f'Username not found'}), 404

    except psycopg2.Error as e:
        return jsonify({"error": f"Error: {e}"}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/remove_user_from_family/<user_name>', methods=['POST'])
def remove_user_from_family(user_name):
    
    autoReset()
    
    try:
        if request.is_json:
            enc_data = request.json

        connection = connect_to_db()
        cursor = connection.cursor()

        key = getUserKey(user_name)
        
        try:
            data = json.loads(decrypt.decrypt_text(enc_data,key, app.config["last_time"]))
            new_user_name = data["new_user"]
            app.config["last_time"] = get_seconds_of_year()
        except:
            return jsonify({'error': 'Wrong key provided'}), 403

        user_id = getUserId(user_name)
        new_user_id = getUserId(new_user_name)

        
        cursor.execute("SELECT members_ids FROM family WHERE family_id = %s", (user_id,))
        current_members = cursor.fetchone()

        if current_members:
            
            
            updated_members = current_members[0]
            if new_user_id in updated_members:
                updated_members.remove(new_user_id)

                cursor.execute("UPDATE family SET members_ids = %s WHERE family_id = %s", (updated_members, user_id))
                connection.commit()

                return jsonify({"message": f"User {new_user_id} removed from family {user_id} successfully."})
            else:
                return jsonify({"error": f"User {new_user_id} not found in family {user_id}."}), 404
        else:
            return jsonify({"error": f"Family with ID {user_id} not found."}), 404

    except psycopg2.Error as e:
        return jsonify({"error": f"Error: {e}"}), 500

    finally:
        cursor.close()
        connection.close()



@app.route('/', methods=['GET'])
def index():
    autoReset()
    return str(get_seconds_of_year())

if __name__ == '__main__':
    try:
        app.run(debug=True, ssl_context=('cert.pem', 'key.pem'), host='192.168.1.1', port=5000)
    except Exception as e:
        app.run(debug=True, ssl_context=('/home/kali/t54-guilherme-jose-guilherme/src/cert.pem', '/home/kali/t54-guilherme-jose-guilherme/src/key.pem'), host='192.168.1.1', port=5000)

