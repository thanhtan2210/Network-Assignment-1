# config.py

# Tracker Configuration
TRACKER_HOST = '127.0.0.1'  # IP address where the tracker will run (localhost for testing)
TRACKER_PORT = 6881         # Port number for the tracker

# Node (peer) Configuration
NODE_HOST = '127.0.0.1'  # IP address where the node will connect
NODE_PORT = 6882         # Port for the peer node to listen on

# Torrent and File Settings
DOWNLOAD_DIR = './downloads'  # Directory where downloaded files will be saved
TEMP_DIR = './temp'           # Temporary directory for pieces being downloaded
MAX_PEERS = 5                # Max number of peers to connect to at once
MAX_REQUESTS = 10            # Max number of requests per peer (for controlling concurrency)

# Torrent Info (example placeholder)
TORRENT_FILE_PATH = './sample.torrent'  # Path to the torrent file to be used for testing

# Logging Configuration
LOG_FILE = 'app.log'  # Log file where application logs will be saved
LOG_LEVEL = 'INFO'    # Log level for the application (DEBUG, INFO, WARN, ERROR)

# DHT (Distributed Hash Table) Settings - Optional feature
ENABLE_DHT = False  # Whether to enable DHT for peer discovery
DHT_PORT = 6883     # Port for DHT to communicate over

# Peer Selection Strategy
PEER_SELECTION_STRATEGY = 'rarest_first'  # Example strategy (could be 'rarest_first', 'random', etc.)

# Interval Configuration for Tracker Announcements and Requests
ANNOUNCE_INTERVAL = 120  # Seconds between peer announcements to the tracker
REQUEST_INTERVAL = 2     # Time interval between consecutive piece requests
