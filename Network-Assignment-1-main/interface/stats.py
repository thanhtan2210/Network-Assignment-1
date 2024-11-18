# stats.py

import time
from node.node import get_node_stats
from tracker.tracker import get_tracker_stats

def display_stats():
    """Display the current statistics for the tracker and nodes."""
    print("Displaying stats...\n")
    
    tracker_stats = get_tracker_stats()
    node_stats = get_node_stats()

    print("Tracker Stats:")
    print(f"Active Peers: {tracker_stats['active_peers']}")
    print(f"Torrent Files: {tracker_stats['torrent_files']}")

    print("\nNode Stats:")
    print(f"Downloaded Pieces: {node_stats['downloaded_pieces']}")
    print(f"Uploaded Pieces: {node_stats['uploaded_pieces']}")
    print(f"Download Speed: {node_stats['download_speed']} KB/s")
    print(f"Upload Speed: {node_stats['upload_speed']} KB/s")
    print("\nPress Ctrl+C to exit.")
    
    while True:
        time.sleep(5)  # Refresh stats every 5 seconds
        print("\nRefreshing stats...")
        print(f"Download Speed: {node_stats['download_speed']} KB/s")
        print(f"Upload Speed: {node_stats['upload_speed']} KB/s")
