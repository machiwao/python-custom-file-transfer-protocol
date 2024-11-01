import socket
import os

# Server-side parameters
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def start_server():
    # Create the server socket (TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"[+] {client_address} connected.")

    try:
        # Receive the file metadata (filename and filesize)
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)  # Avoid directory traversal attacks
        filesize = int(filesize)               # Convert filesize to an integer

        print(f"[*] Receiving file: {filename}, Size: {filesize} bytes")

        # Open the file for writing
        with open(filename, "wb") as file:
            total_received = 0
            while total_received < filesize:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break  # No more data received
                file.write(bytes_read)
                total_received += len(bytes_read)
                print(f"[*] Received {total_received}/{filesize} bytes")

        print(f"[+] File {filename} received successfully.")
    except Exception as e:
        print(f"[!] Error during file transfer: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        print("[*] Connection closed.")

if __name__ == "__main__":
    start_server()
