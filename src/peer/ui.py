import tkinter as tk
from tkinter import messagebox

import requests
import time
from threading import Thread

from peer import announce_to_tracker, connect_to_peer, start_peer_server

peer_id = "peer3" 
peer_port = 6002   
tracker_url = "http://127.0.0.1:5000"

def announce():
    peers = announce_to_tracker(peer_id, peer_port, tracker_url + "/announce")
    if peers:
        peer_list.delete(0, tk.END)
        for peer in peers:
            peer_list.insert(tk.END, f"{peer['ip']}:{peer['port']} ({peer['peer_id']})")
    else:
        messagebox.showinfo("Tracker Response", "No peers found.")

def connect_to_selected_peer():
    selected = peer_list.get(tk.ACTIVE)
    if selected:
        ip, port = selected.split(" ")[0].split(":")
        connect_to_peer(ip, port)
    else:
        messagebox.showwarning("Connection Error", "No peer selected.")

def send_heartbeat():
    while True:
        try:
            response = requests.get(tracker_url + "/announce", params={"peer_id": peer_id, "port": peer_port})
            print("Announced to tracker:", response.json())
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")
        time.sleep(10)

def start_ui():
    global peer_list
    root = tk.Tk()
    root.title("Simple BitTorrent Peer")

    tk.Label(root, text="Peer ID:").pack()
    tk.Label(root, text=peer_id).pack()

    announce_button = tk.Button(root, text="Announce to Tracker", command=announce)
    announce_button.pack(pady=5)

    peer_list = tk.Listbox(root, width=50)
    peer_list.pack(pady=5)

    connect_button = tk.Button(root, text="Connect to Peer", command=connect_to_selected_peer)
    connect_button.pack(pady=5)

    start_peer_server(peer_id, peer_port)
    root.mainloop()

if __name__ == "__main__":
    Thread(target=send_heartbeat, daemon=True).start()
    start_ui()



