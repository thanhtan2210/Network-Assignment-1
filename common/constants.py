# constants.py

# Torrent protocol constants
PIECE_SIZE = 16384  # Size of each piece in bytes
BLOCK_SIZE = 1024   # Size of each block (used when downloading/uploading pieces)

# Default configuration values
DEFAULT_TRACKER_HOST = '127.0.0.1'
DEFAULT_TRACKER_PORT = 6881
DEFAULT_PIECE_SIZE = 16384

# Common error messages
ERROR_MESSAGES = {
    'invalid_request': 'Invalid request received.',
    'peer_not_found': 'Peer not found for the specified file hash.',
}

# File paths
TORRENT_FILE_PATH = './torrents/'
