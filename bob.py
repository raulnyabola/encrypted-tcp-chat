# bob.py

import socket
from Crypto.PublicKey import RSA
import crypto_utils

# Connect to Alice
HOST = '127.0.0.1'
PORT = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[Bob] Connected to Alice.")

# Receive Alice's public RSA key
public_key_pem = client_socket.recv(2048)
alice_public_key = RSA.import_key(public_key_pem)
print("[Bob] Received Alice's public key.")

# Generate AES key and encrypt the message with it
aes_key = crypto_utils.generate_aes_key()
plaintext = b"This is a longer message from Bob, secured with AES."

aes_ciphertext = crypto_utils.aes_encrypt(aes_key, plaintext)

# Encrypt AES key with Alice's RSA public key
encrypted_aes_key = crypto_utils.rsa_encrypt(alice_public_key, aes_key)

# Send the encrypted AES key first, then AES ciphertext
client_socket.sendall(encrypted_aes_key + b"---SPLIT---" + aes_ciphertext)
print("[Bob] Encrypted AES key and AES-encrypted message sent to Alice.")

client_socket.close()
