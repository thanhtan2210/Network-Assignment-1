#download.py

import socket
import threading
import json
import os

BUFFER_SIZE = 1024

def connect_to_tracker(tracker_host, tracker_port):
    """Kết nối tới tracker để lấy danh sách các peer."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((tracker_host, tracker_port))
            s.sendall(b'GET /peers')  # Gửi yêu cầu lấy danh sách peers
            data = s.recv(BUFFER_SIZE).decode()
            return json.loads(data)  # Đảm bảo an toàn khi xử lý dữ liệu JSON
    except (socket.error, json.JSONDecodeError) as e:
        print(f"Failed to connect to tracker: {e}")
        return []

def download_from_peer(peer_ip, peer_port, file_name):
    """Tải dữ liệu từ peer khác."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer_ip, peer_port))
            s.sendall(f"REQUEST_FILE {file_name}".encode())  # Yêu cầu tải file

            # Nhận dữ liệu file
            file_data = s.recv(1024)
            full_file_data = b""
            
            while file_data:
                full_file_data += file_data
                file_data = s.recv(1024)

            # Lưu file vào thư mục shared_files
            shared_folder = "./shared_files"
            os.makedirs(shared_folder, exist_ok=True)
            file_path = os.path.join(shared_folder, file_name)
            with open(file_path, "wb") as f:
                f.write(full_file_data)

            print(f"Downloaded {file_name} from {peer_ip}:{peer_port}")
    except socket.error as e:
        print(f"Failed to download {file_name} from {peer_ip}:{peer_port}: {e}")
