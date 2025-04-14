import socket
import json

PORT = 50000
seen_messeages = set()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PORT))


def decrypt(encrypted_message, key):
    if len(key) != 4:
        raise ValueError("Key must be 4 characters long")
    
    for char in key:
        if not (char.isupper() or char.isdigit()):
            raise ValueError("Key must contain only uppercase letters and digits")
    
    decrypted = ""
    key_index = 0
    
    for char in encrypted_message:
        if char.isalpha():
            current_key_char = key[key_index % 4]
            
            if current_key_char.isupper():
                key_shift = ord(current_key_char) - ord('A')
            else:  # digit
                key_shift = int(current_key_char)
            
            if char.islower():
                decrypted += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
            else:
                decrypted += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
            
            key_index += 1
        else:
            decrypted += char
    
    return decrypted


def get_message_from_sender(code):
    decrypted_message = ""
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode('utf-8'))
            message = msg.get('message', '')


            if  message not in seen_messeages:
                if message[0] == code[0]:
                    decrypted_message = decrypt(message[1:], code)
                    break
                else:
                    pass
                seen_messeages.add(message)


        except Exception as e:
            print(f"Error decoding message: {e}")
    return decrypted_message
