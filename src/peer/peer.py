#peer.py

import socket
import threading
import requests

# Announce to the tracker
def announce_to_tracker(peer_id, port, tracker_url, info_hash, event):
    params = {
        "peer_id": peer_id,
        "port": port,
        "info_hash": info_hash,
        "event": event
    }
    response = requests.get(tracker_url, params=params)
    if response.status_code == 200:
        print("Announced to tracker.")
        return response.json().get("peers", [])
    else:
        print("Failed to announce to tracker:", response.status_code)
        return []

# Peer server to listen for incoming connections
def peer_server(peer_id, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Peer {peer_id} listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")
        client_socket.sendall("Hello from peer!".encode())
        client_socket.close()

# Connect to another peer
def connect_to_peer(ip, port):
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

peer_pieces = set()  # Lưu các khối mà peer đã tải xong
peer_bandwidth = {}  # Cấu trúc: {"peer_id": {"uploaded": 1024, "downloaded": 512}}
request_queue = {}

def update_bandwidth(peer_id, uploaded=0, downloaded=0):
    """Cập nhật băng thông tải lên/tải xuống cho peer."""
    if peer_id not in peer_bandwidth:
        peer_bandwidth[peer_id] = {"uploaded": 0, "downloaded": 0}
    peer_bandwidth[peer_id]["uploaded"] += uploaded
    peer_bandwidth[peer_id]["downloaded"] += downloaded

def add_to_request_queue(piece_index, peer_id):
    """Thêm yêu cầu tải khối vào hàng đợi."""
    if piece_index not in request_queue:
        request_queue[piece_index] = {"status": "pending", "peer": peer_id}


def mark_as_downloading(piece_index):
    """Đánh dấu khối đang tải."""
    if piece_index in request_queue:
        request_queue[piece_index]["status"] = "downloading"


def mark_as_completed(piece_index):
    """Đánh dấu khối đã tải xong."""
    if piece_index in request_queue:
        request_queue[piece_index]["status"] = "completed"


def select_piece_to_request(peer_pieces, all_pieces):
    """Chọn khối cần yêu cầu từ peer."""
    for piece in peer_pieces:
        if piece not in all_pieces and request_queue.get(piece, {}).get("status") != "completed":
            return piece
    return None

def update_tracker_pieces(peer_id, tracker_url, info_hash):
    """Cập nhật khối mà peer sở hữu lên tracker."""
    try:
        response = requests.post(
            f"{tracker_url}/update",
            json={"peer_id": peer_id, "pieces": list(peer_pieces), "info_hash": info_hash},
        )
        print(f"Tracker updated: {response.json()}")
    except Exception as e:
        print(f"Failed to update tracker: {e}")

def request_piece(ip, port, piece_index):
    """Yêu cầu tải khối từ peer khác."""
    try:
        response = requests.get(
            f"http://{ip}:{port}/get_piece", params={"piece_index": piece_index}
        )
        if response.status_code == 200:
            data = response.json().get("data")
            peer_pieces.add(piece_index)
            print(f"Downloaded piece {piece_index}: {data}")
        else:
            print(f"Failed to download piece {piece_index}: {response.json()}")
    except Exception as e:
        print(f"Error requesting piece {piece_index}: {e}")

# Start the peer server in a separate thread
def start_peer_server(peer_id, port):
    threading.Thread(target=peer_server, args=(peer_id, port), daemon=True).start()