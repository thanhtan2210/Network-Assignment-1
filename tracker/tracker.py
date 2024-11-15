# tracker.py

import socket
import json
from database import PeerDatabase
from config import TRACKER_HOST, TRACKER_PORT

class Tracker:
    def __init__(self):
        self.peer_db = PeerDatabase()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((TRACKER_HOST, TRACKER_PORT))
        self.server_socket.listen(5)
        print(f"Tracker is listening on {TRACKER_HOST}:{TRACKER_PORT}")
    
    def start(self):
        """Start the tracker server and handle incoming peer requests."""
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_request(client_socket)
    
    def handle_request(self, client_socket):
        """Handle incoming requests from peers (e.g., announce, get peers)."""
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)

        if request['type'] == 'announce':
            response = self.announce(request)
        elif request['type'] == 'get_peers':
            response = self.get_peers(request)
        else:
            response = {'failure': 'Unknown request type'}
        
        client_socket.sendall(json.dumps(response).encode('utf-8'))
        client_socket.close()

    def announce(self, request):
        """Handle announce requests from peers."""
        peer_id = request['peer_id']
        file_hash = request['file_hash']
        pieces = request['pieces']
        self.peer_db.add_peer(peer_id, file_hash, pieces)
        return {'status': 'success'}

    def get_peers(self, request):
        """Handle get peers requests for a specific torrent."""
        file_hash = request['file_hash']
        peers = self.peer_db.get_peers_for_file(file_hash)
        return {'peers': peers}

if __name__ == "__main__":
    tracker = Tracker()
    tracker.start()
