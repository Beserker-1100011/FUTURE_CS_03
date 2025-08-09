# app.py
from flask import Flask, request, render_template, redirect, url_for, send_file, abort
from werkzeug.utils import secure_filename
from crypto_utils import encrypt_bytes, decrypt_bytes
import os
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit (adjust if needed)

@app.route("/", methods=["GET", "POST"])
def index():
    msg = None
    if request.method == "POST":
        if "file" not in request.files:
            msg = "No file part"
            return render_template("index.html", msg=msg)
        file = request.files["file"]
        if file.filename == "":
            msg = "No selected file"
            return render_template("index.html", msg=msg)
        filename = secure_filename(file.filename)
        # Read raw bytes
        data = file.read()
        enc = encrypt_bytes(data)
        enc_path = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".enc")
        with open(enc_path, "wb") as f:
            f.write(enc)
        msg = f"File uploaded and encrypted as: {filename}.enc"
        return render_template("index.html", msg=msg)
    return render_template("index.html", msg=msg)

# Use path converter to allow spaces and dots in filename
@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    filename = secure_filename(filename)  # prevents traversal
    enc_path = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".enc")
    if not os.path.exists(enc_path):
        return render_template("index.html", msg="File not found: " + filename)
    # Read encrypted bytes and decrypt in memory
    with open(enc_path, "rb") as f:
        enc_bytes = f.read()
    try:
        dec_bytes = decrypt_bytes(enc_bytes)
    except Exception as e:
        # Decryption error (MAC failed, corrupted file, wrong key)
        return render_template("index.html", msg="Decryption failed: " + str(e))
    # Return decrypted file as attachment from memory
    bio = BytesIO()
    bio.write(dec_bytes)
    bio.seek(0)
    # download_name requires Flask >= 2.0; if older, use attachment_filename
    return send_file(bio, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
