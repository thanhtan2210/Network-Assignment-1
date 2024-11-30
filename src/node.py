#node.py

import os
import time
import socket
import threading
import hashlib
import bencodepy
import requests
from tkinter import filedialog, messagebox

def reconstruct_file(torrent_path, pieces_data, save_path):
    try:
        # Đọc tệp torrent
        with open(torrent_path, "rb") as f:
            torrent_data = bencodepy.decode(f.read())

        # Trích xuất thông tin từ torrent
        info = torrent_data[b"info"]
        file_name = info[b"name"].decode()
        piece_length = info[b"piece length"]
        pieces_hashes = info[b"pieces"]

        # Đảm bảo thư mục lưu trữ tồn tại
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Tạo tệp mới từ dữ liệu các mảnh
        reconstructed_file_path = os.path.join(save_path, file_name)
        with open(reconstructed_file_path, "wb") as f:
            for i, piece_data in enumerate(pieces_data):
                # Kiểm tra hash từng mảnh
                expected_hash = pieces_hashes[i * 20:(i + 1) * 20]
                actual_hash = hashlib.sha1(piece_data).digest()
                if actual_hash != expected_hash:
                    raise ValueError(f"Hash mismatch for piece {i}")
                f.write(piece_data)

        print(f"File successfully reconstructed: {reconstructed_file_path}")
        return reconstructed_file_path
    except Exception as e:
        print(f"Failed to reconstruct file: {e}")
        raise

class Node:
    def __init__(self, peer_id, port, tracker_url):
        self.peer_id = peer_id
        self.port = port
        self.tracker_url = tracker_url
        self.peers = []
        self.shared_file = [] #shared file path
    
    def announce_to_tracker(self):
        url = f"{self.tracker_url}/announce"
        params = {
            "peer_id": self.peer_id,
            "port": self.port
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"Peer {self.peer_id} announced to tracker successfully.")
        else:
            print(f"Failed to announce to tracker: {response.status_code}")
    
    def peer_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(5)
        print(f"Peer {self.peer_id} listening on port {self.port}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected by {client_address}")
            client_socket.sendall("Hello from peer!".encode())
            client_socket.close()
            
    def connect_peer(ip, port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect((ip, int(port)))
            print(f"Connected to peer {ip}:{port}")
            response = peer_socket.recv(1024).decode()
            print(f"Peer says: {response}")
        except Exception as e:
            print(f"Error connecting to peer {ip}:{port} -> {e}")
        finally:
            peer_socket.close()

    def connect_to_peer(self, target_ip, target_port, message):
        try:
            Node.connect_peer(target_ip, target_port)
            print(f"Connecting to peer at {target_ip}:{target_port} with message: {message}")
        except Exception as e:
            print(f"Error connecting to peer: {e}")
            raise

    def calculate_pieces(file_path, piece_size):
        try:
            pieces = []
            with open(file_path, "rb") as f:
                while chunk := f.read(piece_size):
                    pieces.append(hashlib.sha1(chunk).digest())
            return b"".join(pieces)
        except Exception as e:
            print(f"Error calculating pieces: {e}")
            raise

    def create_torrent(file_path, tracker_url, save_path):
        try:
            piece_size = 524288
            pieces = Node.calculate_pieces(file_path, piece_size)

            torrent_data = {
                'announce': tracker_url,
                'info': {
                    'name': os.path.basename(file_path),
                    'length': os.path.getsize(file_path),
                    'piece length': piece_size,
                    'pieces': pieces
                }
            }
            with open(save_path, 'wb') as f:
                f.write(bencodepy.encode(torrent_data))
            print(f"Torrent file saved to {save_path}")
        except Exception as e:
            print(f"Failed to create torrent file: {e}")
            raise

    def generate_magnet(torrent_file_path):
        if not os.path.exists(torrent_file_path):
            raise FileNotFoundError(f"Torrent file {torrent_file_path} does not exist.")

        with open(torrent_file_path, "rb") as f:
            torrent_data = bencodepy.decode(f.read())
        info = torrent_data[b'info']
        info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()
        file_name = torrent_data[b'info'][b'name'].decode("utf-8")
        tracker_url = torrent_data[b'announce'].decode("utf-8")
        magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={file_name}&tr={tracker_url}"
        return magnet_link

    def upload(self, file_path):
        file_name = os.path.basename(file_path)
        shared_folder = "{self.peer_id}/shared_files"
        os.makedirs(shared_folder, exist_ok=True)
        destination_path = os.path.join(shared_folder, file_name)
        with open(file_path, "rb") as src, open(destination_path, "wb") as dst:
            dst.write(src.read())
        print(f"File {file_name} upload to {shared_folder} successfully.")

    def download_file(self, torrent_file_path):
    # Yêu cầu người dùng chọn thư mục lưu
        save_folder = filedialog.askdirectory(title="Select Folder to Save Downloaded File")
        if not save_folder:
            messagebox.showwarning("Download Error", "Please select a folder to save the file.")
            return

        try:
            os.makedirs(save_folder, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

            # Sao chép file torrent cục bộ vào thư mục đích
            pieces_data = [b"...", b"..."]
            torrent_file = os.path.basename(torrent_file_path)
            file_name = os.path.basename(torrent_file_path)
            save_path = os.path.join(save_folder, file_name)
            reconstruct_file(torrent_file_path, pieces_data, save_folder)
        except Exception as e:
            print(f"Error copying file: {e}")
            return f"Error: {e}"
