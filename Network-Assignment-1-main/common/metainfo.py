# metainfo.py

import bencoded

def read_torrent(file_path):
    """Reads a .torrent file and returns the decoded dictionary."""
    with open(file_path, 'rb') as f:
        return bencoded.decode(f.read())

def write_torrent(file_path, torrent_dict):
    """Writes the given torrent dictionary to a .torrent file."""
    with open(file_path, 'wb') as f:
        f.write(bencoded.encode(torrent_dict))

def extract_file_hash(torrent_dict):
    """Extracts the file hash from the torrent dictionary."""
    return torrent_dict['info']['hash']

def extract_pieces(torrent_dict):
    """Extracts the list of pieces from the torrent dictionary."""
    return torrent_dict['info']['pieces']
