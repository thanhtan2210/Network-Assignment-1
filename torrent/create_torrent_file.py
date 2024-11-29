#create_torrent_file.py

import os
import hashlib
import bencodepy

def calculate_pieces(file_path, piece_size):
    try:
        pieces = []
        with open(file_path, "rb") as f:
            while chunk := f.read(piece_size):
                pieces.append(hashlib.sha1(chunk).digest())
        return b"".join(pieces)
    except Exception as e:
        print(f"Error calculating pieces: {e}")
        raise

def create_torrent(file_path, tracker_url, save_path):
    try:
        piece_size = 524288
        pieces = calculate_pieces(file_path, piece_size)

        torrent_data = {
            'announce': tracker_url,
            'info': {
                'name': os.path.basename(file_path),
                'length': os.path.getsize(file_path),
                'piece length': piece_size,
                'pieces': pieces
            }
        }
        with open(save_path, 'wb') as f:
            f.write(bencodepy.encode(torrent_data))
        print(f"Torrent file saved to {save_path}")
    except Exception as e:
        print(f"Failed to create torrent file: {e}")
        raise

def generate_magnet(torrent_file_path):
    if not os.path.exists(torrent_file_path):
        raise FileNotFoundError(f"Torrent file {torrent_file_path} does not exist.")

    with open(torrent_file_path, "rb") as f:
        torrent_data = bencodepy.decode(f.read())
    info = torrent_data[b'info']
    info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()
    file_name = torrent_data[b'info'][b'name'].decode("utf-8")
    tracker_url = torrent_data[b'announce'].decode("utf-8")
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={file_name}&tr={tracker_url}"
    return magnet_link