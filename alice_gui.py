import socket
import crypto_utils
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# ----- TCP Setup -----
HOST = '127.0.0.1'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# ----- GUI Setup -----
window = tk.Tk()
window.title("Alice (Receiver)")
window.geometry("500x400")

msg_display = scrolledtext.ScrolledText(window, height=15)
msg_display.pack(pady=5)


def wait_for_bob():
    msg_display.insert(tk.END, "[Alice] Listening for Bob on 127.0.0.1:65432...\n")
    window.update()

    conn, addr = server_socket.accept()
    msg_display.insert(tk.END, f"[Alice] Connection established with {addr}.\n")
    window.update()

    # Send Alice's public key to Bob
    private_key, public_key = crypto_utils.generate_rsa_keypair(bits=1024)
    public_key_pem = public_key.export_key()
    conn.sendall(public_key_pem)
    msg_display.insert(tk.END, "[Alice] Public key sent to Bob.\n")
    window.update()

    data = conn.recv(1000000)
    encrypted_aes_key, payload = data.split(b"---SPLIT---")

    # Decrypt AES Key
    aes_key = crypto_utils.rsa_decrypt(private_key, encrypted_aes_key)

    # Split payload into message / file
    payload_parts = payload.split(b"---FILE---")

    # Decrypt Message (if exists)
    if payload_parts[0].strip() and not payload_parts[0].startswith(b"---FILE---"):
        plaintext_msg = crypto_utils.aes_decrypt(aes_key, payload_parts[0]).decode()
        msg_display.insert(tk.END, f"[Alice] Message from Bob:\n{plaintext_msg}\n")
    else:
        msg_display.insert(tk.END, "[Alice] No message received from Bob.\n")

    window.update()

    # Decrypt File (if exists)
    if len(payload_parts) > 1 and payload_parts[1].strip():
        file_bytes = crypto_utils.aes_decrypt(aes_key, payload_parts[1])
        filename = f"received_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
        with open(filename, "wb") as f:
            f.write(file_bytes)
        msg_display.insert(tk.END, f"[Alice] File received and saved as {filename}\n")
    else:
        msg_display.insert(tk.END, "[Alice] No file received from Bob.\n")

    conn.close()
    server_socket.close()
    msg_display.insert(tk.END, "[Alice] Connection closed.\n")
    window.update()


wait_for_bob()

window.mainloop()
