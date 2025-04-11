import struct
import os
from tqdm import tqdm
identifier = "<EOF>"



def WriteFile(command, client):
    # Vérifier si le fichier existe côté client
    exist = client.recv(1024).decode()
    if exist == "yes":
        print("File exists on client side.")
        filename = command.split(" ", 1)[-1].strip()

        # Recevoir la taille du fichier
        filesize = struct.unpack('<Q', client.recv(8))[0]
        print(f"File size: {filesize} bytes")

        with tqdm(total=filesize, unit='B', unit_scale=True, desc=f"Downloading {filename}") as pbar:
            with open(filename, "wb") as f:
                while True:
                    chunk = client.recv(1024)
                    if chunk.endswith(identifier.encode()):
                        chunk = chunk[:-len(identifier)]
                        f.write(chunk)
                        pbar.update(len(chunk))
                        break
                    f.write(chunk)
                    pbar.update(len(chunk))
        print("File downloaded successfully.")
    else:
        print("File not found on client side.")


def ReadFile(command, client):
    filename = command.split(" ", 1)[-1].strip()
    if os.path.exists(filename):
        client.send("yes".encode())
        filesize = os.path.getsize(filename)
        client.send(struct.pack('<Q', filesize))

        with open(filename, "rb") as f:
            while chunk := f.read(1024):
                client.send(chunk)
            client.send(identifier.encode())
        print(f"File '{filename}' sent successfully.")
    else:
        client.send("no".encode())
        print(f"File '{filename}' not found.")