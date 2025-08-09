# 🔒 Secure File Sharing with AES Encryption

## Overview
A simple Flask web app that lets users upload files, encrypts them using AES before saving, and decrypts them for download.

## Features
- Secure AES encryption for files at rest
- Basic web UI for uploading & downloading
- Simple key-based encryption (for demo purposes)
## 🛠 Tech Stack
- Languages: Python, HTML, CSS, JS (optional frontend)
- Dev Library: Flask
- Encryption Library: pycryptodome or cryptography
- Tools: Git, GitHub, VS Code
- # Secure File Sharing (Flask + AES)

## Quick Start
1. `pip install -r requirements.txt`
2. `python app.py`
3. Open `http://127.0.0.1:5000`

## Notes
- Uploaded files are stored as `<filename>.enc` in uploads/.
- AES key stored in `key.key`. Keep it safe — if lost, encrypted files cannot be recovered.
- This is a demo. For production use secure key management, HTTPS, auth, and rate-limiting.



