# Encrypted TCP Chat with RSA & AES (Python)

This project demonstrates a secure TCP chat between two users (Alice and Bob) using:
- **RSA** for secure key exchange (public/private keys)
- **AES (GCM mode)** for encrypting messages and files

---

## How It Works
1. **Alice** (server) listens for Bob (client).
2. **Bob** connects, receives Alice's **public key**.
3. Bob encrypts either:
   - A **short message** OR
   - A **file**
4. Alice decrypts using her **private key** (RSA) and **AES key**.

---

## How to Run

1️⃣ Open Terminal in project folder:
```bash
# Activate virtual environment
.\venv\Scripts\activate    # Windows

2️⃣ Run Alice (Receiver):
python alice_gui.py

3️⃣ In a second terminal, run Bob (Sender):
python bob_gui.py

📦 Requirements
Install dependencies:
pip install -r requirements.txt

📁 Files
| File               | Purpose                |
| ------------------ | ---------------------- |
| `alice_gui.py`     | Alice's GUI (receiver) |
| `bob_gui.py`       | Bob's GUI (sender)     |
| `crypto_utils.py`  | Crypto functions       |
| `requirements.txt` | Dependencies           |

🔒 Security
RSA 1024-bit for exchanging AES keys.
AES-256 GCM for encrypting messages/files.
Separate handling of messages vs. files.

👨‍🏫 Author
Raul Nyabola | July 16, 2025 | Self Project