# crypto_utils.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY_FILE = "key.key"

def ensure_key():
    """Create a 16-byte AES key (AES-128) if not exists, and return it."""
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(get_random_bytes(16))
    with open(KEY_FILE, "rb") as f:
        return f.read()

KEY = ensure_key()

def encrypt_bytes(plain_bytes: bytes) -> bytes:
    """
    Encrypt bytes using AES-EAX.
    Returns bytes organized as: nonce (16) + tag (16) + ciphertext.
    """
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plain_bytes)
    return cipher.nonce + tag + ciphertext

def decrypt_bytes(enc_bytes: bytes) -> bytes:
    """
    Decrypt bytes that were created by encrypt_bytes.
    Expects nonce (16) + tag (16) + ciphertext.
    """
    if len(enc_bytes) < 32:
        raise ValueError("Encrypted payload too short")
    nonce = enc_bytes[:16]
    tag = enc_bytes[16:32]
    ciphertext = enc_bytes[32:]
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
