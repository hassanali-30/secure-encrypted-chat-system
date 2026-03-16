import socket
import threading
import sys
import time
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import pickle
import struct

# ================= CONFIG =================
PORT = 4444

# ✅ EXACT LENGTHS
SESSION_KEY = b"0123456789ABCDEF0123456789ABCDEF"  # 32 bytes
SESSION_IV  = b"ABCDEF0123456789"                  # 16 bytes

USERS = {
    "Hassan": {"password": "1234", "avatar": "🧑‍💻"},
    "Haider": {"password": "abcd", "avatar": "👨‍🔧"},
    "Ali": {"password": "adminpass", "avatar": "🛡️"},
}

PHISHING_KEYWORDS = [
    "verify your account", "click this link",
    "urgent login", "password reset",
    "bank alert", "free money"
]

clients = {}
last_msg_time = {}

# ================= ENCRYPTION =================
def encrypt_data(data: bytes):
    cipher = Cipher(algorithms.AES(SESSION_KEY), modes.CFB(SESSION_IV))
    return cipher.encryptor().update(data)

def decrypt_data(data: bytes):
    cipher = Cipher(algorithms.AES(SESSION_KEY), modes.CFB(SESSION_IV))
    return cipher.decryptor().update(data)

# ================= FILE ENCRYPTION =================
def encrypt_file(data):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    return key, iv, cipher.encryptor().update(data)

def decrypt_file(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    return cipher.decryptor().update(data)

# ================= FRAMING =================
def send_secure(sock, data: bytes):
    encrypted = encrypt_data(data)
    sock.sendall(struct.pack("!I", len(encrypted)) + encrypted)

def recv_secure(sock):
    raw_len = sock.recv(4)
    if not raw_len:
        return None
    size = struct.unpack("!I", raw_len)[0]

    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk

    return decrypt_data(data)

# ================= SERVER =================
def is_spam(user):
    now = time.time()
    last = last_msg_time.get(user, 0)
    last_msg_time[user] = now
    return now - last < 1

def is_phishing(msg):
    return any(k in msg.lower() for k in PHISHING_KEYWORDS)

def broadcast(payload, sender=None):
    for u, c in clients.items():
        if u != sender:
            send_secure(c, payload)

def handle_client(conn):
    user = None
    try:
        raw = recv_secure(conn)
        if not raw:
            return

        cmd = raw.decode().split("|")
        if cmd[0] != "LOGIN":
            return

        user, pwd = cmd[1], cmd[2]
        if user not in USERS or USERS[user]["password"] != pwd:
            send_secure(conn, b"LOGIN_FAIL")
            return

        clients[user] = conn
        send_secure(conn, b"LOGIN_OK")
        broadcast(pickle.dumps(("TEXT", f"[SYSTEM] {user} joined")), user)

        while True:
            data = recv_secure(conn)
            if not data:
                break

            msg_type, content = pickle.loads(data)

            if msg_type == "TEXT":
                if is_spam(user):
                    send_secure(conn, pickle.dumps(("TEXT", "[SYSTEM] Spam detected")))
                    continue

                warn = " ⚠ PHISHING" if is_phishing(content) else ""
                ts = datetime.now().strftime("%H:%M:%S")
                final = f"[{ts}] {USERS[user]['avatar']} {user}: {content}{warn}"
                broadcast(pickle.dumps(("TEXT", final)), user)

            elif msg_type == "FILE":
                broadcast(pickle.dumps(("FILE", content)), user)

    finally:
        if user in clients:
            clients.pop(user)
            broadcast(pickle.dumps(("TEXT", f"[SYSTEM] {user} left")))
        conn.close()

def start_server():
    s = socket.socket()
    s.bind(("0.0.0.0", PORT))
    s.listen()
    print("🟢 Server running on port", PORT)
    while True:
        c, _ = s.accept()
        threading.Thread(target=handle_client, args=(c,), daemon=True).start()

# ================= CLIENT =================
def start_client():
    sock = socket.socket()
    win = tk.Tk()
    win.title("Secure Chat")

    server_ip = simpledialog.askstring("Server", "Enter Server IP:", parent=win)
    if not server_ip:
        win.destroy()
        return

    def receive():
        while True:
            try:
                data = recv_secure(sock)
                if not data:
                    break

                msg_type, content = pickle.loads(data)

                if msg_type == "FILE":
                    name, key, iv, enc = content
                    path = filedialog.asksaveasfilename(initialfile=name)
                    if path:
                        with open(path, "wb") as f:
                            f.write(decrypt_file(key, iv, enc))
                else:
                    chat.insert(tk.END, content + "\n")
            except:
                break

    def send_text():
        txt = entry.get()
        if txt:
            send_secure(sock, pickle.dumps(("TEXT", txt)))
            entry.delete(0, tk.END)

    def send_file():
        path = filedialog.askopenfilename()
        if path:
            with open(path, "rb") as f:
                data = f.read()
            key, iv, enc = encrypt_file(data)
            send_secure(sock, pickle.dumps(("FILE", (os.path.basename(path), key, iv, enc))))

    def login():
        try:
            sock.connect((server_ip, PORT))
            send_secure(sock, f"LOGIN|{u.get()}|{p.get()}".encode())
            if recv_secure(sock) != b"LOGIN_OK":
                messagebox.showerror("Error", "Login failed")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Server unreachable\n{e}")
            return

        frame_login.pack_forget()
        frame_chat.pack(fill="both", expand=True)
        threading.Thread(target=receive, daemon=True).start()

    frame_login = tk.Frame(win)
    frame_login.pack(pady=20)

    tk.Label(frame_login, text="Username").pack()
    u = tk.Entry(frame_login)
    u.pack()

    tk.Label(frame_login, text="Password").pack()
    p = tk.Entry(frame_login, show="*")
    p.pack()

    tk.Button(frame_login, text="Login", command=login).pack()

    frame_chat = tk.Frame(win)
    chat = ScrolledText(frame_chat)
    chat.pack(fill="both", expand=True)

    entry = tk.Entry(frame_chat)
    entry.pack(fill="x")

    tk.Button(frame_chat, text="Send", command=send_text).pack()
    tk.Button(frame_chat, text="Send File", command=send_file).pack()

    win.mainloop()

# ================= MAIN =================
if len(sys.argv) != 2:
    print("Usage: python project.py server|client")
    sys.exit()

if sys.argv[1] == "server":
    start_server()
elif sys.argv[1] == "client":
    start_client()
