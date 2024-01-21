import requests

url = 'http://localhost:5000/list/1'  # Replace this with your Flask app's URL

try:
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)  # This will print the response body
    else:
        print(f"Request failed with status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Request failed: {e}")