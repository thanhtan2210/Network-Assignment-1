# utils.py

import hashlib
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def generate_peer_id():
    """Generate a random peer ID."""
    return hashlib.sha1(b"peer").hexdigest()

def hash_file(filename):
    """Generate the SHA1 hash of a file."""
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def log_info(message):
    """Log an info message."""
    logging.info(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)
