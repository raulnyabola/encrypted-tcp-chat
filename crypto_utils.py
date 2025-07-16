from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


# ---------------- RSA SECTION -------------------
def generate_rsa_keypair(bits=1024):
    key = RSA.generate(bits)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key


def rsa_encrypt(public_key, data):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(data)


def rsa_decrypt(private_key, ciphertext):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(ciphertext)


# ---------------- AES SECTION -------------------
def generate_aes_key():
    return get_random_bytes(32)  # AES-256


def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext  # [16 bytes IV] + [16 bytes TAG] + [rest]


def aes_decrypt(key, data):
    nonce = data[:16]     # First 16 bytes = nonce (IV)
    tag = data[16:32]     # Next 16 bytes = authentication tag
    ciphertext = data[32:]  # Rest = ciphertext
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
