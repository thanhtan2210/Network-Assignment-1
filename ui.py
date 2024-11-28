#ui.py

import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import time
from node.peer import Peer
from torrent.create_torrent_file import create_torrent, generate_magnet

# Biến toàn cục
peers = []  # Danh sách các peer đang hoạt động
tracker_url = "http://127.0.0.1:8000"  # URL của tracker server

# Hàm thông báo với tracker
def announce(peer_instance):
    try:
        # Đường dẫn file torrent
        torrent_file_path = "D:/Bon Bon/project 1/git/STA/torrent/output.txt"
        info_hash = peer_instance.get_info_hash(torrent_file_path)

        # Gửi thông tin peer tới tracker
        peer_instance.announce_to_tracker(info_hash)

        # Hiển thị thông báo thành công
        print(f"Peer {peer_instance.peer_id} on port {peer_instance.port} announced successfully!")
        messagebox.showinfo("Announce Success", f"Announced peer {peer_instance.peer_id} to tracker.")
    except requests.exceptions.ConnectionError:
        print("Tracker server is not reachable. Please check if it's running.")
        messagebox.showerror("Connection Error", "Tracker server is not reachable. Check if it's running.")
    except Exception as e:
        print(f"Failed to announce: {e}")
        messagebox.showerror("Announce Error", f"Failed to announce: {e}")

# Kết nối tới peer được chọn
def connect_to_selected_peer(peer_instance):
    selected = peer_list_box.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("Connection Error", "Please select a peer.")
        return

    # Lấy giá trị port từ trường nhập
    port_input = port_entry.get().strip()
    if not port_input.isdigit():
        messagebox.showwarning("Invalid Port", "Please enter a valid port number.")
        return

    port = int(port_input)  # Chuyển port thành số nguyên

    try:
        # Chia tách peer_id từ chuỗi trong Listbox (giả sử cấu trúc peer_id (127.0.0.1:port))
        peer_id = selected.split(" (127.0.0.1:")[0]
        peer_instance.connect_to_peer("127.0.0.1", port, "Hello, Peer!")
        messagebox.showinfo("Connection Success", f"Connected to peer {peer_id} on port {port}.")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {e}")

# Gửi heartbeat đến tracker
def send_heartbeat(peer_instance):
    while True:
        try:
            torrent_file_path = filedialog.askopenfilename(title="Select Torrent File")
            if not torrent_file_path:
                continue
            info_hash = peer_instance.get_info_hash(torrent_file_path)
            peer_instance.announce_to_tracker(info_hash)
        except Exception as e:
            print(f"Heartbeat error: {e}")
        time.sleep(10)

# Upload file và tạo file torrent
def upload_file():
    file_path = filedialog.askopenfilename(title="Select File to Share")
    if not file_path:
        messagebox.showwarning("Upload Error", "Please select a file to share.")
        return

    save_path = filedialog.asksaveasfilename(
        title="Save Torrent File As",
        defaultextension=".torrent",
        filetypes=[("Torrent Files", "*.torrent")]
    )
    if not save_path:
        messagebox.showwarning("Save Error", "Please specify a save location for the torrent file.")
        return

    try:
        create_torrent(file_path, tracker_url, save_path)
        magnet_link = generate_magnet(save_path)
        magnet_label.config(text=f"Magnet Link: {magnet_link}", wraplength=400)
        messagebox.showinfo("Upload Success", "Torrent file created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create torrent file: {e}")

# Download file từ magnet link
def download_file(peer_instance):
    magnet_link = magnet_entry.get().strip()
    if not magnet_link:
        messagebox.showwarning("Download Error", "Please enter a valid magnet link.")
        return

    try:
        peer_instance.download_from_magnet(magnet_link)
        messagebox.showinfo("Download Success", f"Download started for: {magnet_link}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start download: {e}")

# UI chính
def start_ui(peer_instance):
    global peer_list_box, magnet_label, magnet_entry, port_entry  # Thêm port_entry

    root = tk.Tk()
    root.title(f"Peer {peer_instance.peer_id} - BitTorrent Client")

    tk.Label(root, text=f"Peer {peer_instance.peer_id}", font=("Arial", 14)).pack(pady=10)

    announce_button = tk.Button(root, text="Announce to Tracker", command=lambda: announce(peer_instance))
    announce_button.pack(pady=5)

    peer_list_box = tk.Listbox(root, width=50)
    peer_list_box.pack(pady=5)

    # Thêm Entry cho người dùng nhập port
    tk.Label(root, text="Enter Port:").pack(pady=5)
    port_entry = tk.Entry(root, width=50)
    port_entry.pack(pady=5)

    connect_button = tk.Button(root, text="Connect to Peer", command=lambda: connect_to_selected_peer(peer_instance))
    connect_button.pack(pady=5)

    upload_button = tk.Button(root, text="Upload File", command=upload_file)
    upload_button.pack(pady=5)

    tk.Label(root, text="Magnet Link:").pack()
    magnet_entry = tk.Entry(root, width=50)
    magnet_entry.pack(pady=5)

    download_button = tk.Button(root, text="Download File", command=lambda: download_file(peer_instance))
    download_button.pack(pady=5)

    magnet_label = tk.Label(root, text="", fg="blue")
    magnet_label.pack(pady=5)

    # Khởi động danh sách peer cập nhật liên tục
    Thread(target=update_peer_list_ui, args=(peer_instance,), daemon=True).start()
    root.mainloop()


# Cập nhật danh sách peer trong giao diện
def update_peer_list_ui(peer_instance):
    """
    Cập nhật danh sách peer trong Listbox từ tracker.
    """
    try:
        response = requests.get(f"{tracker_url}/peers")
        if response.status_code == 200:
            data = response.json()
            peer_list = data.get("peers", [])
            peer_list_box.delete(0, tk.END)  # Xóa tất cả các peer cũ
            if peer_list:  # Nếu có peer
                for peer in peer_list:
                    peer_id = peer["peer_id"]
                    port = peer["port"]
                    peer_list_box.insert(tk.END, f"{peer_id} (127.0.0.1:{port})")
            else:
                print("No peers found in the response.")
        else:
            print(f"Failed to fetch peers: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to update peer list: {e}")


if __name__ == "__main__":
    peer_id = input("Enter Peer ID: ").strip()
    while not peer_id:
        print("Peer ID cannot be empty. Please try again.")
        peer_id = input("Enter Peer ID: ").strip()

    while True:
        try:
            peer_port = int(input("Enter Peer Port: ").strip())
            break  # Thoát vòng lặp nếu nhập hợp lệ
        except ValueError:
            print("Invalid input. Peer Port must be a number. Please try again.")

    peer_instance = Peer(peer_id, peer_port, tracker_url)

    # Khởi chạy heartbeat
    Thread(target=send_heartbeat, args=(peer_instance,), daemon=True).start()

    # Khởi chạy UI
    start_ui(peer_instance)
