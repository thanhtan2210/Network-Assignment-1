#ui.py
import argparse
import tkinter as tk
from tkinter import messagebox

import requests
import time
from threading import Thread,Event

# from peer import announce_to_tracker, connect_to_peer, start_peer_server
from peer import (
    announce_to_tracker,
    connect_to_peer,
    start_peer_server,
    update_tracker_pieces,
    request_piece,
)

# peer_id = "peer3" 
# peer_port = 6002   
tracker_url = "http://127.0.0.1:5000"
info_hash = "hash123"  # Magnet text hash
peer_list = None
piece_input = None
stop_heartbeat = Event() 

def parse_args():
    parser = argparse.ArgumentParser(description="Run multiple peers.")
    parser.add_argument('peer_ids', metavar='peer_id', type=str, nargs='+', help="List of peer IDs")
    parser.add_argument('--port_start', type=int, default=6001, help="Starting port number for peers.")
    return parser.parse_args()

def announce(peer_id, peer_port,event = "started"):
    peers = announce_to_tracker(peer_id, peer_port, tracker_url + "/announce", info_hash, event)
    if peers:
        peer_list.delete(0, tk.END)
        for peer in peers:
            peer_list.insert(tk.END, f"{peer['ip']}:{peer['port']} ({peer['peer_id']})")
    else:
        messagebox.showinfo("Tracker Response", "No peers found.")

def update_peer_list(peers):
    peer_list.delete(0, tk.END)
    for peer in peers:
        peer_list.insert(tk.END, f"{peer['ip']}:{peer['port']} ({peer['peer_id']})")

def connect_to_selected_peer():
    selected = peer_list.get(tk.ACTIVE)
    if selected:
        ip, port = selected.split(" ")[0].split(":")
        connect_to_peer(ip, port)
    else:
        messagebox.showwarning("Connection Error", "No peer selected.")

def send_heartbeat(peer_id, peer_port):
    while True:
        try:
            params = {
                "peer_id": peer_id,
                "port": peer_port,
                "info_hash": info_hash,
                "event": "started",
            }
            response = requests.get(tracker_url + "/announce", params = params)
            print("Announced to tracker:", response.json())
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")
        time.sleep(10)

def download_piece(peer_id):
    print(f"Downloading piece for peer: {peer_id}")
    selected = peer_list.get(tk.ACTIVE)
    if selected:
        ip, port = selected.split(" ")[0].split(":")
        try:
            piece_index = int(piece_input.get())
            request_piece(ip, int(port), piece_index)
            print(f"Downloading piece {piece_index} from {ip}:{port} for peer {peer_id}")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid piece index.")
    else:
        messagebox.showwarning("Download Error", "No peer selected.")

def upload_pieces(peer_id):
    """Gửi trạng thái khối lên tracker."""
    update_tracker_pieces(peer_id, tracker_url, info_hash)

def start_peer_ui(peer_id, peer_port, root):
    # global peer_list
    # root = tk.Tk()
    # root.title("Simple BitTorrent Peer")

    # tk.Label(root, text="Peer ID:").pack()
    # tk.Label(root, text=peer_id).pack()

    # announce_button = tk.Button(root, text="Announce to Tracker", command=announce)
    # announce_button.pack(pady=5)

    # peer_list = tk.Listbox(root, width=50)
    # peer_list.pack(pady=5)

    # connect_button = tk.Button(root, text="Connect to Peer", command=connect_to_selected_peer)
    # connect_button.pack(pady=5)

    # start_peer_server(peer_id, peer_port)
    # root.mainloop()
    def announce_event(event="started"):
        announce(peer_id, peer_port, event)

    def connect_to_selected_peer_local():
        connect_to_selected_peer()
        
    def download_piece_local():
        download_piece(peer_id)

    def upload_piece_local():
        upload_pieces(peer_id)

    # Tạo cửa sổ con cho mỗi peer
    peer_window = tk.Toplevel(root)
    peer_window.title(f"Peer {peer_id}")

    tk.Label(peer_window, text=f"Peer ID: {peer_id}").pack()

    announce_button = tk.Button(peer_window, text="Announce to Tracker", command=announce_event)
    announce_button.pack(pady=5)

    global peer_list
    peer_list = tk.Listbox(peer_window, width=50)
    peer_list.pack(pady=5)

    connect_button = tk.Button(peer_window, text="Connect to Peer", command=connect_to_selected_peer_local)
    connect_button.pack(pady=5)

    download_button = tk.Button(peer_window, text="Download Piece", command=download_piece_local)
    download_button.pack(pady=5)

    upload_button = tk.Button(peer_window, text="Upload Piece", command=upload_piece_local)
    upload_button.pack(pady=5)

    global piece_input
    piece_input = tk.Entry(peer_window, width=10)
    piece_input.pack()

    # Khởi chạy server cho peer
    start_peer_server(peer_id, peer_port)

# Hàm chạy nhiều peer dựa trên đối số dòng lệnh
def run_peers():
    args = parse_args()
    port = args.port_start
    root = tk.Tk() 
    for peer_id in args.peer_ids:
        Thread(target=send_heartbeat, args=(peer_id, port), daemon=True).start()
        Thread(target=start_peer_ui, args=(peer_id, port, root), daemon=True).start()
        port += 1  # Tăng port cho peer tiếp theo
    root.mainloop()
    
def on_close(root):
    """Đảm bảo dừng tất cả các luồng khi đóng cửa sổ."""
    stop_heartbeat.set()  # Dừng heartbeat thread
    root.quit()  # Thoát khỏi Tkinter main loop

if __name__ == "__main__":
    run_peers()