from flask import Flask, request, jsonify
import time
from threading import Thread

app = Flask(__name__)

# In-memory peer list
peers_list = []  # Format: [{"peer_id": "peer1", "ip": "127.0.0.1", "port": 6000, "last_seen": 12345678}]

# Maximum time a peer can stay inactive (in seconds)
PEER_TIMEOUT = 30

@app.route('/announce', methods=['GET'])
def announce():
    peer_id = request.args.get('peer_id')
    ip = request.remote_addr
    port = request.args.get('port')

    if peer_id and port:
        # Refresh or add the peer
        peer_info = {"peer_id": peer_id, "ip": ip, "port": int(port), "last_seen": time.time()}
        for peer in peers_list:
            if peer["peer_id"] == peer_id:
                peer.update(peer_info)  # Update existing peer info
                break
        else:
            peers_list.append(peer_info)

    # Respond with the current list of peers
    response = {
        "tracker_id": "1",
        "peers": [{"peer_id": p["peer_id"], "ip": p["ip"], "port": p["port"]} for p in peers_list]
    }
    return jsonify(response)

# Background thread to clean up inactive peers
def cleanup_peers():
    while True:
        current_time = time.time()
        peers_list[:] = [peer for peer in peers_list if current_time - peer["last_seen"] <= PEER_TIMEOUT]
        time.sleep(5)  # Check every 5 seconds

@app.route("/peers", methods=["GET"])
def get_peers():
    return jsonify({"peers": peers_list})

if __name__ == "__main__":
    Thread(target=cleanup_peers, daemon=True).start()  # Start cleanup thread
    app.run(host="0.0.0.0", port=8000)