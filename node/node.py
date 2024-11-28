#node.py

import socket
import threading

def start_peer_server(peer_id, port):
    """Khởi động server để xử lý yêu cầu từ các peer khác."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Peer {peer_id} listening on port {port}...")

    def handle_connection(client_socket, client_address):
        """Xử lý kết nối từ peer khác."""
        try:
            print(f"Connected by {client_address}")
            request = client_socket.recv(1024).decode()
            print(f"Received request: {request}")
            if request.startswith("REQUEST_PIECE"):
                client_socket.sendall(b"Piece data placeholder.")  # Trả về dữ liệu mẫu
            else:
                client_socket.sendall(b"Invalid request.")
        except socket.error as e:
            print(f"Error handling connection from {client_address}: {e}")
        finally:
            client_socket.close()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_connection, args=(client_socket, client_address), daemon=True).start()
