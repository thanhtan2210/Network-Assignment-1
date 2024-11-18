import socket
import threading
import requests

# Announce to the tracker
def announce_to_tracker(peer_id, port, tracker_url):
    params = {"peer_id": peer_id, "port": port}
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

# Start the peer server in a separate thread
def start_peer_server(peer_id, port):
    threading.Thread(target=peer_server, args=(peer_id, port), daemon=True).start()
