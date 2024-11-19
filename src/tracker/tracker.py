# tracker.py

from flask import Flask, request, jsonify
import time
from threading import Thread

app = Flask(__name__)

# In-memory peer list
# Format: [{"peer_id": "peer1", "ip": "127.0.0.1", "port": 6000, "last_seen": 12345678}]
peers_list = []

torrents = {"hash123": {"name": "example_file",
                        "piece_length": 512, "pieces": 10}}  # Example metadata

# Maximum time a peer can stay inactive (in seconds)
PEER_TIMEOUT = 30


@app.route('/announce', methods=['GET'])
def announce():
    peer_id = request.args.get('peer_id')
    ip = request.remote_addr
    port = request.args.get('port')
    event = request.args.get('event')  # started, stopped, completed
    magnet_hash = request.args.get('info_hash')

    if not peer_id or not port or not magnet_hash:
        return jsonify({"failure reason": "Missing required parameters"}), 400

    if magnet_hash not in torrents:
        return jsonify({"failure reason": "Torrent not found"}), 404

    # Handle peer events
    if event == "stopped":
        peers_list[:] = [
            peer for peer in peers_list if peer["peer_id"] != peer_id]
    elif event in ["started", "completed"]:
        peer_info = {"peer_id": peer_id, "ip": ip,
                     "port": int(port), "last_seen": time.time()}
        for peer in peers_list:
            if peer["peer_id"] == peer_id:
                peer.update(peer_info)  # Update existing peer info
                break
        else:
            peers_list.append(peer_info)            

    if peer_id and port:
        # Refresh or add the peer
        peer_info = {"peer_id": peer_id, "ip": ip,
                     "port": int(port), "last_seen": time.time()}
        for peer in peers_list:
            if peer["peer_id"] == peer_id:
                peer.update(peer_info)  # Update existing peer info
                break
        else:
            peers_list.append(peer_info)
     # Respond with peer list
    response = {
        "tracker_id": "track ai bay gio day",
        "peers": [{"peer_id": p["peer_id"], "ip": p["ip"], "port": p["port"]} for p in peers_list],
        "warning message": "Ensure correct magnet text and info_hash."
    }
    return jsonify(response)

@app.route('/update', methods=['POST'])
def update_pieces():
    data = request.json
    peer_id = data.get("peer_id")
    pieces = data.get("pieces")  # Danh sách khối mà peer sở hữu

    for peer in peers_list:
        if peer["peer_id"] == peer_id:
            peer["pieces"] = pieces
            break
    else:
        return jsonify({"failure reason": "Peer not found"}), 404

    return jsonify({"success": True})

@app.route('/get_piece', methods=['GET'])
def get_piece():
    piece_index = int(request.args.get("piece_index"))
    peer_id = request.args.get("peer_id")

    for peer in peers_list:
        if peer["peer_id"] == peer_id:
            # Trả về dữ liệu khối (giả định nội dung khối là string)
            return jsonify({"piece_index": piece_index, "data": f"Data for piece {piece_index}"})
    return jsonify({"failure reason": "Piece not available"}), 404

# Background thread to clean up inactive peers

def cleanup_peers():
    while True:
        current_time = time.time()
        peers_list[:] = [peer for peer in peers_list if current_time -
                         peer["last_seen"] <= PEER_TIMEOUT]
        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    Thread(target=cleanup_peers, daemon=True).start()  # Start cleanup thread
    app.run(host="0.0.0.0", port=5000)