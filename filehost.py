import socket
import os

HOST = '34.125.76.169'
PORT = 8000
BUFFER_SIZE = 4096

def serve_forever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Получен запрос на соединение от {addr[0]}:{addr[1]}")
            handle_connection(conn)

def handle_connection(conn):
    request = conn.recv(BUFFER_SIZE).decode()
    if not request:
        return
    filename = request.split()[1][1:]
    if not os.path.isfile(filename):
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.sendall(response.encode())
        return
    with open(filename, 'rb') as file:
        response = "HTTP/1.1 200 OK\r\n\r\n"
        conn.sendall(response.encode())
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            conn.sendall(data)
    conn.close()

if __name__ == '__main__':
    serve_forever()