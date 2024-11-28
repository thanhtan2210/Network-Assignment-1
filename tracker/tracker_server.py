# tracker_server.py

from flask import Flask, request, jsonify
import time
from threading import Thread

app = Flask(__name__)
peers = []

# Cơ sở dữ liệu lưu thông tin torrent và peer
torrent_db = {}
PEER_TIMEOUT = 30  # Thời gian timeout (giây)

@app.route("/announce", methods=["GET"])
def announce():
    peer_id = request.args.get("peer_id")
    port = request.args.get("port")
    info_hash = request.args.get("info_hash")

    if not peer_id or not port or not info_hash:
        return "Missing required parameters", 400

    # Lưu thông tin peer vào danh sách peers
    peer = {"peer_id": peer_id, "port": port, "info_hash": info_hash}
    if peer not in peers:
        peers.append(peer)

    return "Announced successfully", 200

def cleanup_peers():
    """
    Xóa các peer không hoạt động.
    """
    while True:
        current_time = time.time()
        for info_hash, torrent in list(torrent_db.items()):
            torrent["peers"] = [
                peer for peer in torrent["peers"] if current_time - peer["last_seen"] <= PEER_TIMEOUT
            ]
        time.sleep(5)


@app.route("/peers", methods=["GET"])
def get_peers():
    """
    Trả về danh sách các peer.
    """
    return jsonify({"peers": peers})


if __name__ == '__main__':
    Thread(target=cleanup_peers, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
