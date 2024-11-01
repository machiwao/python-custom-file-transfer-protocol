import socket
import os
import sys

BUFFER_SIZE = 4096
SEPARATOR = ""

def send_file(server_host, filename):
    server_port = 5001
    filesize = os.path.getsize(filename)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Connecting to {server_host}:{server_port}")

    try:
        client_socket.connect((server_host, server_port))
        print(f"[+] Connected to {server_host}:{server_port}")
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

        with open(filename, "rb") as file:
            while (bytes_read := file.read(BUFFER_SIZE)):
                client_socket.sendall(bytes_read)

        print(f"[+] File {filename} sent successfully.")
        print("SUCCESS")  # Indicate success for the UI
    except Exception as e:
        print(f"[!] Error during file transfer: {e}")
        print("FAILURE")  # Indicate failure for the UI
    finally:
        client_socket.close()
        print("[*] Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Client.py <server_host> <filename>")
        sys.exit(1)
    server_host = sys.argv[1]
    filename = sys.argv[2]
    send_file(server_host, filename)
