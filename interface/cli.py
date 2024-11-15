# cli.py

import argparse
from tracker.tracker import start_tracker
from node.node import start_node
from interface.stats import display_stats
from interface.config import CONFIG

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple Torrent-like Application (STA)")
    parser.add_argument('--start-tracker', action='store_true', help="Start the tracker server")
    parser.add_argument('--start-node', action='store_true', help="Start the node (peer client)")
    parser.add_argument('--stats', action='store_true', help="Display current statistics")
    parser.add_argument('--torrent', type=str, help="Path to the torrent file")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.start_tracker:
        print("Starting tracker...")
        start_tracker(CONFIG['tracker_port'])

    elif args.start_node:
        if not args.torrent:
            print("Please provide a torrent file using --torrent.")
            return
        print(f"Starting node for torrent {args.torrent}...")
        start_node(args.torrent)

    elif args.stats:
        print("Displaying statistics...")
        display_stats()

    else:
        print("Please provide a valid argument. Use --help for options.")

if __name__ == "__main__":
    main()
