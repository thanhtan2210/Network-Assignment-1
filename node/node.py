# node.py

import socket
import os
import threading
from peer_protocol import PeerProtocol
from file_manager import FileManager
from config import NODE_HOST, NODE_PORT, DOWNLOAD_DIR

class Node:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.peer_protocol = PeerProtocol()
        self.file_manager = FileManager(torrent_file)
        self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node_socket.bind((NODE_HOST, NODE_PORT))
        self.node_socket.listen(5)
        print(f"Node is listening on {NODE_HOST}:{NODE_PORT}")
    
    def start(self):
        print(f"Starting node for {self.torrent_file}")
        # Start the download/upload process in a separate thread
        download_thread = threading.Thread(target=self.download)
        download_thread.start()
        self.handle_connections()
    
    def download(self):
        """Logic for downloading pieces from peers"""
        while True:
            pieces_to_download = self.file_manager.get_pieces_to_download()
            for piece in pieces_to_download:
                # Request piece from peers
                peers = self.peer_protocol.get_peers(self.torrent_file)
                for peer in peers:
                    self.peer_protocol.request_piece(peer, piece)
                    # After downloading the piece, update file manager
                    self.file_manager.update_piece(piece)
    
    def handle_connections(self):
        """Handle incoming connections from other peers for uploading"""
        while True:
            client_socket, addr = self.node_socket.accept()
            print(f"Connection from {addr}")
            peer_protocol = PeerProtocol(client_socket)
            peer_protocol.handle_peer_requests()

if __name__ == "__main__":
    # You can pass the path to the torrent file as an argument
    torrent_file = './sample.torrent'
    node = Node(torrent_file)
    node.start()
