# database.py

class PeerDatabase:
    def __init__(self):
        self.db = {}

    def add_peer(self, peer_id, file_hash, pieces):
        """Add a new peer for a specific file hash."""
        if file_hash not in self.db:
            self.db[file_hash] = []
        self.db[file_hash].append({'peer_id': peer_id, 'pieces': pieces})
        print(f"Peer {peer_id} added for file {file_hash}")
    
    def get_peers_for_file(self, file_hash):
        """Return the list of peers for a specific file hash."""
        return self.db.get(file_hash, [])
