import socket
import time
import json
import os

BROADCAST_IP = '255.255.255.255'
PORT = 50000

current_dir = os.path.dirname(os.path.abspath(__file__))  
messages_path = os.path.join(current_dir, 'message.json')  



while True:
    try:
        with open(messages_path, 'r') as file:
            content = file.read().strip()
            if not content:
                continue  
            message = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        continue  
    if message.get('message') is None:
        pass
    else:
        if time.time() > message.get('expireTime', 0):
            with open(messages_path, 'w') as file:
                file.write("{}")
        else:
            print(f"Sending message... {message.get('message')}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            data = json.dumps(message).encode('utf-8')
            sock.sendto(data, (BROADCAST_IP, PORT))
    time.sleep(0.5)