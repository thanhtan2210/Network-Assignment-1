#upload.py

import socket
import threading
import os

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

def upload_to_peer(peer_instance, file_path):
    """
    Upload a file to the current peer's storage.
    """
    # Lấy tên file
    file_name = os.path.basename(file_path)

    # Copy file vào thư mục chia sẻ (ví dụ: shared_folder)
    shared_folder = "shared_files"  # Thư mục chia sẻ trên peer
    os.makedirs(shared_folder, exist_ok=True)
    destination_path = os.path.join(shared_folder, file_name)
    with open(file_path, "rb") as src, open(destination_path, "wb") as dst:
        dst.write(src.read())

    print(f"File {file_name} uploaded to {shared_folder} successfully.")

def share_file_with_peers(peer_instance, file_path):
    """
    Notify other peers about the uploaded file.
    """
    file_name = os.path.basename(file_path)
    peer_instance.share_file(file_name)  # Gọi hàm chia sẻ trong lớp Peer
    print(f"File {file_name} shared with peers.")
