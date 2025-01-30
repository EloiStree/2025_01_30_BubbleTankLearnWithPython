

import socket

"""
127.0.0.1:8008
192.168.1.102:8008
127.0.0.118:8008
"""




def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8008))
    server_socket.listen(5)
    print("Server listening on port 8008")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        data = client_socket.recv(1024)
        if data:
            print(f"Received data: {data.decode('utf-8')}")
        client_socket.close()

if __name__ == "__main__":
    start_server()