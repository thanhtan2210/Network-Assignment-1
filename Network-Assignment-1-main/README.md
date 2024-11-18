# Simple Torrent-like Application (STA)

STA is a peer-to-peer file-sharing application inspired by BitTorrent. It includes a tracker server and peer clients (nodes) that allow users to download and upload files via torrent files. This project demonstrates core concepts of peer-to-peer file sharing, including multi-file downloading, peer management, and handling torrent metadata.

## Features

- **Tracker Server**: Manages peer announcements and tracks peers' availability for downloading and uploading pieces of a file.
- **Node (Peer Client)**: Downloads and uploads pieces of a file from multiple peers concurrently.
- **Multi-File Torrent Support**: Handles downloading and uploading multiple files in a torrent.
- **Peer-to-Peer Communication**: Implements P2P communication for exchanging file pieces between peers.
- **Download and Upload Statistics**: Tracks and displays download/upload statistics, including peer information.

## Project Structure

```
STA/
├── tracker/                  # Tracker server related files
│   ├── tracker.py            # Main tracker logic
│   ├── database.py           # Peer database
│   ├── config.py             # Configuration settings for the tracker
├── node/                     # Node (peer client) related files
│   ├── node.py               # Main peer logic (download/upload)
│   ├── peer_protocol.py      # P2P communication protocols
│   ├── file_manager.py       # File handling (reading/writing pieces)
│   ├── request_manager.py    # Manages piece requests and uploads
│   ├── config.py             # Configuration settings for the node
├── common/                   # Shared utilities
│   ├── utils.py              # Shared utility functions (e.g., logging, hashing)
│   ├── constants.py          # Constants used across tracker and node
│   ├── metainfo.py           # Handling .torrent file and magnet link processing
├── interface/                # Command-line interface and UI files
│   ├── cli.py                # Command-line interface logic
│   ├── stats.py              # Displays download/upload statistics
│   ├── config.py             # UI configuration settings
├── tests/                    # Unit tests for various modules
│   ├── test_tracker.py       # Tests for tracker functionality
│   ├── test_node.py          # Tests for node functionality
│   ├── test_peer_protocol.py # Tests for P2P communication
│   ├── test_file_manager.py  # Tests for file handling
│   ├── test_metainfo.py      # Tests for torrent metadata
│   ├── test_stats.py         # Tests for statistics display
│   ├── test_config.py        # Tests for configuration
├── config.py                 # Global configuration file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Installation

### Prerequisites

Make sure you have Python 3.x installed. You can download Python from the official [Python website](https://www.python.org/downloads/).

1. Clone the repository:

   ```bash
   git clone https://github.com/thanhtan2210/Network-Assignment-1.git
   cd STA
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Tracker Server

To start the tracker server, run the following command:

```bash
python -m interface.cli --start-tracker
```

This will start the tracker server on the default host and port (defined in `config.py`).

### Running the Node (Peer Client)

To start a node (peer client) and download/upload a torrent, run:

```bash
python -m interface.cli --start-node --torrent path_to_torrent_file
```

Replace `path_to_torrent_file` with the actual path to your `.torrent` file.

### Viewing Statistics

To view the current download/upload statistics, run:

```bash
python -m interface.cli --stats
```

### CLI Arguments

- `--start-tracker`: Starts the tracker server.
- `--start-node`: Starts the node (peer client).
- `--torrent <path>`: The path to the `.torrent` file for the node to process.
- `--stats`: Displays download/upload statistics.

## Testing

To run the unit tests for all modules, use the following command:

```bash
python -m unittest discover tests/
```

Alternatively, you can run individual tests:

```bash
python -m unittest tests.test_tracker
python -m unittest tests.test_node
```

## Configuration

You can modify the following configuration values in `config.py`:

- **Tracker Host**: The host where the tracker server is running.
- **Tracker Port**: The port where the tracker listens for incoming peer connections.
- **Max Peers**: The maximum number of peers the tracker will manage at a time.
- **Chunk Size**: The size of the pieces (chunks) that the node will download/upload.

Example of `config.py`:

```python
CONFIG = {
    'tracker_host': '127.0.0.1',   # Host for the tracker server
    'tracker_port': 6881,          # Port for the tracker
    'max_peers': 10,               # Maximum number of peers
    'chunk_size': 1024 * 128,      # Size of each piece to download/upload (128KB)
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
