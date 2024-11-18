mport socket
import json

class TrackerClient:
    def __init__(self, node_id, tracker_host, tracker_port):
        self.node_id = node_id
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port

    def announce(self, file_hash, pieces):
        message = {
            "type": "announce",
            "peer_id": self.node_id,
            "file_hash": file_hash,
            "pieces": pieces
        }
        self.send_message(message)

    def get_peers(self, file_hash):
        message = {
            "type": "get_peers",
            "file_hash": file_hash
        }
        response = self.send_message(message)
        return response.get("peers", [])

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.tracker_host, self.tracker_port))
            sock.sendall(json.dumps(message).encode('utf-8'))
            response = sock.recv(1024)
            return json.loads(response.decode('utf-8'))
