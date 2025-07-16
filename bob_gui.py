import socket
import crypto_utils
import tkinter as tk
from tkinter import filedialog, scrolledtext

# ----- TCP Setup -----
HOST = '127.0.0.1'
PORT = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# ----- GUI Setup -----
window = tk.Tk()
window.title("Bob (Sender)")
window.geometry("500x400")

msg_display = scrolledtext.ScrolledText(window, height=12)
msg_display.pack(pady=5)

entry = tk.Entry(window, width=50)
entry.pack(pady=5)


def send_message():
    public_key_pem = client_socket.recv(4096)
    public_key = crypto_utils.RSA.import_key(public_key_pem)
    aes_key = crypto_utils.generate_aes_key()

    plaintext = entry.get().strip()
    if not plaintext:
        msg_display.insert(tk.END, "[Bob] No message to send.\n")
        return
    encrypted_msg = crypto_utils.aes_encrypt(aes_key, plaintext.encode())
    payload = encrypted_msg + b"---FILE---"  # No file attached
    encrypted_aes_key = crypto_utils.rsa_encrypt(public_key, aes_key)
    full_data = encrypted_aes_key + b"---SPLIT---" + payload
    client_socket.sendall(full_data)

    msg_display.insert(tk.END, "[Bob] Message sent to Alice.\n")
    entry.delete(0, tk.END)


def send_file():
    public_key_pem = client_socket.recv(4096)
    public_key = crypto_utils.RSA.import_key(public_key_pem)
    aes_key = crypto_utils.generate_aes_key()

    file_path = filedialog.askopenfilename()
    if not file_path:
        msg_display.insert(tk.END, "[Bob] No file selected.\n")
        return

    with open(file_path, "rb") as f:
        file_bytes = f.read()
    encrypted_file = crypto_utils.aes_encrypt(aes_key, file_bytes)

    payload = b"---FILE---" + encrypted_file  # No message attached
    encrypted_aes_key = crypto_utils.rsa_encrypt(public_key, aes_key)
    full_data = encrypted_aes_key + b"---SPLIT---" + payload
    client_socket.sendall(full_data)

    msg_display.insert(tk.END, f"[Bob] File sent: {file_path}\n")


send_msg_button = tk.Button(window, text="Send Message", command=send_message)
send_msg_button.pack(pady=5)

send_file_button = tk.Button(window, text="Send File", command=send_file)
send_file_button.pack(pady=5)

window.mainloop()
client_socket.close()
