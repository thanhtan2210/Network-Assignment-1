#create_torrent_file.py

import os
import hashlib
import bencodepy

def calculate_pieces(file_path, piece_size):
    """
    Tính toán mã băm SHA-1 cho từng mảnh của file.
    """
    try:
        pieces = []
        with open(file_path, "rb") as f:
            while chunk := f.read(piece_size):
                pieces.append(hashlib.sha1(chunk).digest())
        return b"".join(pieces)  # Nối các mã băm thành chuỗi byte
    except Exception as e:
        print(f"Error calculating pieces: {e}")
        raise

def create_torrent(file_path, tracker_url, save_path):
    """
    Tạo file torrent từ file nguồn.
    """
    try:
        piece_size = 524288  # 512 KB mỗi mảnh
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

        # Lưu file torrent
        with open(save_path, 'wb') as f:
            f.write(bencodepy.encode(torrent_data))
        print(f"Torrent file saved to {save_path}")
    except Exception as e:
        print(f"Failed to create torrent file: {e}")
        raise

def generate_magnet(torrent_file_path):
    """
    Tạo liên kết magnet từ file torrent.
    """
    if not os.path.exists(torrent_file_path):
        raise FileNotFoundError(f"Torrent file {torrent_file_path} does not exist.")

    with open(torrent_file_path, "rb") as f:
        torrent_data = bencodepy.decode(f.read())
    
    # Lấy info_hash
    info = torrent_data[b'info']
    info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()

    # Lấy tên file
    file_name = torrent_data[b'info'][b'name'].decode("utf-8")

    # Tạo magnet link
    tracker_url = torrent_data[b'announce'].decode("utf-8")
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={file_name}&tr={tracker_url}"
    return magnet_link