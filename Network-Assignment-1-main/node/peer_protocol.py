# peer_protocol.py

import socket
import json
from file_manager import FileManager

class PeerProtocol:
    def __init__(self, client_socket=None):
        if client_socket:
            self.client_socket = client_socket
        else:
            self.client_socket = None

    def get_peers(self, torrent_file):
        """Request list of peers from the tracker"""
        # Dummy function to simulate getting peers
        return [('127.0.0.1', 6883), ('127.0.0.1', 6884)]
    
    def request_piece(self, peer, piece_index):
        """Request a piece from a peer"""
        # Simulate piece request to the peer
        print(f"Requesting piece {piece_index} from {peer}")
        # You can implement actual TCP connection with peers here
        self.send_message(peer, {"type": "request", "piece": piece_index})

    def send_message(self, peer, message):
        """Send message to peer"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(peer)
            s.sendall(json.dumps(message).encode('utf-8'))
    
    def handle_peer_requests(self):
        """Handle incoming requests from other peers (uploading)"""
        data = self.client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)
        
        if request['type'] == 'request':
            piece_index = request['piece']
            # Simulate uploading the piece to the peer
            print(f"Sending piece {piece_index} to the peer.")
            self.send_piece(piece_index)
    
    def send_piece(self, piece_index):
        """Send a specific piece to a peer"""
        # Dummy implementation: Simulate sending a piece
        piece_data = b"sample_piece_data"  # Replace with actual piece data
        self.client_socket.sendall(piece_data)

