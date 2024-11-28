#upload.py

import socket
import threading

BUFFER_SIZE = 1024

def serve_pieces(port, file_path):
    """
    Khởi chạy server để chia sẻ dữ liệu.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Upload server is running on port {port}...")

    def handle_request(client_socket):
        try:
            request = client_socket.recv(BUFFER_SIZE).decode()
            if request.startswith("REQUEST_PIECE"):
                _, piece_index = request.split()
                piece_index = int(piece_index)
                with open(file_path, "rb") as f:
                    f.seek(piece_index * BUFFER_SIZE)
                    data = f.read(BUFFER_SIZE)
                    client_socket.sendall(data)
                    print(f"Sent piece {piece_index} to client.")
        except Exception as e:
            print(f"Error during upload: {e}")
        finally:
            client_socket.close()

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_request, args=(client_socket,), daemon=True).start()