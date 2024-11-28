#download.py

import socket
import threading
import json

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

def download_from_peer(peer_ip, peer_port, piece_index):
    """Tải dữ liệu từ peer khác."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer_ip, peer_port))
            s.sendall(f"REQUEST_PIECE {piece_index}".encode())  # Yêu cầu tải mảnh dữ liệu
            data = s.recv(BUFFER_SIZE)
            with open(f"piece_{piece_index}.dat", "wb") as f:
                f.write(data)  # Lưu mảnh tải về vào file
            print(f"Downloaded piece {piece_index} from {peer_ip}:{peer_port}")
    except socket.error as e:
        print(f"Failed to download piece {piece_index} from {peer_ip}:{peer_port}: {e}")

def start_download(tracker_host, tracker_port):
    """Khởi động quá trình tải từ các peer."""
    peer_list = connect_to_tracker(tracker_host, tracker_port)
    if not peer_list:
        print("No peers found from the tracker.")
        return

    threads = []
    for piece_index, peer in enumerate(peer_list):
        peer_ip, peer_port = peer.get('ip'), peer.get('port')
        if peer_ip and peer_port:
            t = threading.Thread(target=download_from_peer, args=(peer_ip, peer_port, piece_index))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()  # Đợi tất cả các thread tải xuống hoàn thành
    print("Download completed.")
