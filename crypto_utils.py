from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 32-byte AES key (use env variable in real projects)
KEY = b"this_is_a_32_byte_secret_key_for_demo!!"

def encrypt_file(input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(output_path, "wb") as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

def decrypt_file(input_path, output_path):
    with open(input_path, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(output_path, "wb") as f:
        f.write(data)
