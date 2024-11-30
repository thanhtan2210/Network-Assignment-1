import os
import hashlib
import bencodepy

def reconstruct_file(torrent_path, pieces_data, save_path):
    try:
        # Đọc tệp torrent
        with open(torrent_path, "rb") as f:
            torrent_data = bencodepy.decode(f.read())

        # Trích xuất thông tin từ torrent
        info = torrent_data[b"info"]
        file_name = info[b"name"].decode()
        piece_length = info[b"piece length"]
        pieces_hashes = info[b"pieces"]

        # Đảm bảo thư mục lưu trữ tồn tại
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Tạo tệp mới từ dữ liệu các mảnh
        reconstructed_file_path = os.path.join(save_path, file_name)
        with open(reconstructed_file_path, "wb") as f:
            for i, piece_data in enumerate(pieces_data):
                # Kiểm tra hash từng mảnh
                expected_hash = pieces_hashes[i * 20:(i + 1) * 20]
                actual_hash = hashlib.sha1(piece_data).digest()
                if actual_hash != expected_hash:
                    raise ValueError(f"Hash mismatch for piece {i}")
                f.write(piece_data)

        print(f"File successfully reconstructed: {reconstructed_file_path}")
        return reconstructed_file_path
    except Exception as e:
        print(f"Failed to reconstruct file: {e}")
        raise



if __name__ == "__main__":
    pieces_data = [b"...", b"..."]  # Dữ liệu từng mảnh
    torrent_file = "file1.torrent"
    save_directory = "./output"
    reconstructed_file = reconstruct_file(torrent_file, pieces_data, save_directory)
