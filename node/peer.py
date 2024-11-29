#peer.py

import os
import socket
import threading
import hashlib
import bencodepy
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Peer:
    def __init__(self, peer_id, port, tracker_url):
        self.peer_id = peer_id
        self.port = port
        self.tracker_url = tracker_url
        self.peers = []
        self.shared_file = []  # Thực sự thêm file vào đây

    def add_shared_file(self, file_name):
        """Thêm file vào danh sách các file chia sẻ của peer."""
        if file_name not in self.shared_file:
            self.shared_file.append(file_name)
            print(f"File {file_name} added to shared files.")

        # Thiết lập retry cho các request HTTP
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def get_info_hash(self, torrent_file_path):
        """
        Đọc file torrent và trả về hash của nội dung.
        """
        try:
            with open(torrent_file_path, "rb") as f:
                content = f.read()
                # Tính toán hash từ nội dung
                info_hash = hashlib.sha1(content).hexdigest()
                return info_hash
        except Exception as e:
            print(f"Error getting info_hash: {e}")
            raise
        
    def announce_to_tracker(self, info_hash):
        url = f"{self.tracker_url}/announce"
        params = {
            "peer_id": self.peer_id,
            "port": self.port,
            "info_hash": info_hash
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Peer {self.peer_id} announced to tracker successfully.")
        else:
            print(f"Failed to announce to tracker: {response.status_code}")

    def start_server(self):
        """Khởi chạy server để nhận kết nối từ các peer khác."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", self.port))
        server_socket.listen(5)
        print(f"Peer {self.peer_id} listening on port {self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """Xử lý yêu cầu từ peer khác."""
        try:
            data = client_socket.recv(1024).decode()
            print(f"Received from peer: {data}")

            # Kiểm tra nếu yêu cầu tải file
            if data.startswith("DOWNLOAD"):
                file_name = data.split(" ")[1]  # Tên file được yêu cầu tải
                self.download_file(file_name, client_socket)
            else:
                client_socket.send(f"Unknown request: {data}".encode())
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.send(f"Error: {e}".encode())
        finally:
            client_socket.close()

            
            
    def get_peers(self):
        """
        Lấy danh sách các peer đã đăng ký từ tracker.
        """
        try:
            response = requests.get(f"{self.tracker_url}/peers")
            if response.status_code == 200:
                return response.json().get("peers", [])
            else:
                print(f"Failed to fetch peers: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error while fetching peers: {e}")
            return []

    def connect_to_peer(self, target_ip, target_port, message):
        try:
            # Logic để kết nối với peer qua socket
            # Ví dụ: sử dụng socket để kết nối
            print(f"Connecting to peer at {target_ip}:{target_port} with message: {message}")
            # Kết nối và gửi thông điệp
        except Exception as e:
            print(f"Error connecting to peer: {e}")
            raise
    
    def download_file(self, file_name):
        """
        Tải file từ thư mục shared_files và gửi cho peer yêu cầu.
        """
        shared_folder = "./shared_files"
        file_path = os.path.join(shared_folder, file_name)
        
        # Kiểm tra xem file có tồn tại không
        if not os.path.exists(file_path):
            print(f"File {file_name} not found in shared folder.")
            return "File not found"  # Trả về thông báo lỗi
    
        # Đọc file và gửi dữ liệu cho peer
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
    
            # Gửi dữ liệu file cho peer
            print(f"Sending file {file_name}...")
            return file_data  # Trả về dữ liệu file cho peer hoặc client
    
        except Exception as e:
            print(f"Error reading or sending file {file_name}: {e}")
            return f"Error: {e}"  # Trả về lỗi nếu có
