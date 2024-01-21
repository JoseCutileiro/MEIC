import sys
import requests
import json
import base64
import pygame
import threading
import time
import select
from datetime import datetime
from sirs_crypto import decrypt, encrypt
from io import BytesIO
from pydub import AudioSegment

def get_seconds_of_year():
    # Get the current time
    current_time = datetime.now()

    # Get the start of the current year
    start_of_year = datetime(current_time.year, 1, 1)

    # Calculate the difference in seconds between current time and start of the year
    seconds_of_year = (current_time - start_of_year).total_seconds()

    return int(seconds_of_year)

def decodeMP3(file_name, audio_data):
    # Convert to MP3 using pydub
    audio_segment = AudioSegment.from_mp3(BytesIO(audio_data))
    audio_segment.export("downloads/" + file_name + ".mp3", format="mp3")
    return

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

def get_user_input(stop_event):
    print("Controls: 'pause', 'resume', 'time', 'stop'")
    print("Press enter when song finishes")
    while not stop_event.is_set():
        user_input = input(": ").lower()
        if user_input == 'pause':
            pygame.mixer.music.pause()
        elif user_input == 'resume':
            pygame.mixer.music.unpause()
        elif user_input == 'time':
            playback_time_seconds = pygame.mixer.music.get_pos() / 1000.0
            playback_time_formatted = format_time(playback_time_seconds)
            print(f"Playback Time: {playback_time_formatted}")
        elif user_input == 'stop':
            pygame.mixer.music.stop()
            break
    return

def listPrint(list):
    out = ""
    for string in data:
        out += string + ", "
    out = out[:-2]
    print(out)

def playAudio(audio_data):
    try:
        audio_stream = BytesIO(audio_data)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        stop_event = threading.Event()
        input_thread = threading.Thread(target=get_user_input, args=(stop_event,))
        input_thread.start()
        while pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() > 0: 
            pygame.time.wait(100)
            if not input_thread.is_alive():
                break
        stop_event.set()
        input_thread.join() 
    except Exception as e:
        print(f"Error playing audio: {e}")
    return

if len(sys.argv) != 3:
    print("Please provide a username and the file with the user's key.")
    exit()

user_name = sys.argv[1]
key_path = sys.argv[2] 

with open(key_path, 'rb') as key_file:
    key = key_file.read()

url = "https://192.168.1.1:5000"

try:
    response = requests.get(url + "/", verify='cert.pem')
except requests.ConnectionError as e:
    print("Unable to establish a connection.")
    print(e)
    exit()
except requests.RequestException as e:
    print("Request failed:", e)
    exit()


print("""

  /$$$$$$                                                     /$$$$$$            /$$                              
 /$$__  $$                                                   /$$__  $$          | $$                              
| $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$  /$$    /$$ /$$$$$$ | $$  \__/  /$$$$$$ | $$  /$$$$$$  /$$   /$$ /$$   /$$
| $$ /$$$$ /$$__  $$ /$$__  $$ /$$__  $$|  $$  /$$//$$__  $$| $$ /$$$$ |____  $$| $$ |____  $$|  $$ /$$/| $$  | $$
| $$|_  $$| $$  \__/| $$  \ $$| $$  \ $$ \  $$/$$/| $$$$$$$$| $$|_  $$  /$$$$$$$| $$  /$$$$$$$ \  $$$$/ | $$  | $$
| $$  \ $$| $$      | $$  | $$| $$  | $$  \  $$$/ | $$_____/| $$  \ $$ /$$__  $$| $$ /$$__  $$  >$$  $$ | $$  | $$
|  $$$$$$/| $$      |  $$$$$$/|  $$$$$$/   \  $/  |  $$$$$$$|  $$$$$$/|  $$$$$$$| $$|  $$$$$$$ /$$/\  $$|  $$$$$$$
 \______/ |__/       \______/  \______/     \_/    \_______/ \______/  \_______/|__/ \_______/|__/  \__/ \____  $$
                                                                                                         /$$  | $$
                                                                                                        |  $$$$$$/
                                                                                                         \______/ 

Welcome to GrooveGalaxy - Your ultimate destination for music lovers!
Explore a vast collection of songs, albums, and playlists.

Commands available:
- list: list available musics to download 
- download: downloads a specific music 
- play: plays a specific music
- check-family: checks wich families belongs 
- family-members: prints all family members
- family-add: add user to family
- family-remove: remove user of family
- exit: close program

Enjoy your musical journey with GrooveGalaxy!
""")


while True:
    user_input = input("Enter a command: ")
    if user_input.lower() == 'list':
        try:
            response = requests.get(url + "/list_musics/" + user_name, verify='cert.pem')

            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to get music list.")
            else:
                decrypted_data = decrypt.decrypt_text(data, key, 100)
                data = json.loads(decrypted_data)["data"]
                listPrint(data)
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()
        
    elif user_input.lower() == 'download':
        music_name = input("Enter music name: ")
        try:
            response = requests.get(url + "/download_music/" + user_name + "/" + music_name, verify='cert.pem')
            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to download music.")
            else:
                decrypted_data = decrypt.decrypt_text(data, key, 100)
                data = json.loads(json.loads(decrypted_data)["data"])["mediaContent"]
                audio_data = base64.b64decode(data["audioBase64"])
                if data["format"] == "MP3":
                    decodeMP3(data["title"] + "-" + data["artist"], audio_data)
                print("Download succ!")
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()

    elif user_input.lower() == 'play':
        music_name = input("Enter music name: ")
        try:
            response = requests.get(url + "/download_music/" + user_name + "/" + music_name, verify='cert.pem')
            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to receive music.")
            else:
                decrypted_data = decrypt.decrypt_text(data, key, 100)
                data = json.loads(json.loads(decrypted_data)["data"])["mediaContent"]
                audio_data = base64.b64decode(data["audioBase64"])
                playAudio(audio_data)
                print("Audio track finished!")
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()

    elif user_input.lower() == 'check-family':
        try:
            response = requests.get(url + "/family_check/" + user_name, verify='cert.pem')
            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to check family.")
            else:
                decrypted_data = decrypt.decrypt_text(data, key, 100)
                data = json.loads(decrypted_data)["data"]
                listPrint(data)
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()
        
    elif user_input.lower() == 'family-members':
        try:
            response = requests.get(url + "/family_members/" + user_name, verify='cert.pem')
            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to get family members.")
            else:
                decrypted_data = decrypt.decrypt_text(data, key, 100)
                data = json.loads(decrypted_data)["data"]
                listPrint(data)

        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()

    elif user_input.lower() == 'family-add':
        try:
            new_user = input("Enter the user to add: ")

            encrypt_data = encrypt.encrypt_text(json.dumps({'new_user': new_user, 'fresh_token': get_seconds_of_year()}), key)
            
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url + "/add_user_to_family/" + user_name, data=json.dumps(encrypt_data) ,headers=headers)
            print(response.content)

            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to check family.")
            else:
                print(data)
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()
    elif user_input.lower() == 'family-remove':
        try:
            new_user = input("Enter the user to remove: ")

            encrypt_data = encrypt.encrypt_text(json.dumps({'new_user': new_user, 'fresh_token': get_seconds_of_year()}), key)
            
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url + "/remove_user_from_family/" + user_name, data=json.dumps(encrypt_data) ,headers=headers)
            print(response.content)

            data = json.loads(response.content)
            if response.status_code != 200:
                if 'error' in data: 
                    print(data['error'])
                else:
                    print("Failed to check family.")
            else:
                print(data)
        except requests.ConnectionError:
            print("Unable to establish a connection.")
            exit()
        except requests.RequestException as e:
            print("Request failed:", e)
            exit()
    elif user_input.lower() == 'exit':
        break