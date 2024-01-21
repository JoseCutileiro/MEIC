file_name = 'keys/secret_Alex_Scott.key'  # Replace with your actual file name

try:
    with open(file_name, 'rb') as file:
        content = file.read()
        hex_representation = content.hex()
        print(hex_representation)
except FileNotFoundError:
    print(f"File '{file_name}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")