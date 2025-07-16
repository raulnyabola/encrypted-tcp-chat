# alice.py

import socket
import crypto_utils

# Generate RSA keypair
private_key, public_key = crypto_utils.generate_rsa_keypair(bits=1024)
public_key_pem = public_key.export_key()

# Set up TCP Server
HOST = '127.0.0.1'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[Alice] Listening on {HOST}:{PORT}... Waiting for Bob.")
conn, addr = server_socket.accept()
print(f"[Alice] Connected with {addr}.")

# Send Alice's public key to Bob
conn.sendall(public_key_pem)
print("[Alice] Public key sent.")

# Receive encrypted AES key + AES ciphertext
data = conn.recv(4096)
encrypted_aes_key, aes_ciphertext = data.split(b"---SPLIT---")
print("[Alice] Received encrypted AES key and AES ciphertext.")

# Decrypt AES key with RSA private key
aes_key = crypto_utils.rsa_decrypt(private_key, encrypted_aes_key)

# Decrypt message with AES key
plaintext = crypto_utils.aes_decrypt(aes_key, aes_ciphertext)
print("[Alice] Final decrypted message from Bob:", plaintext.decode())

conn.close()
server_socket.close()
