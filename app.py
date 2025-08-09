from flask import Flask, request, render_template, send_file
import os
from crypto_utils import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DECRYPT_FOLDER = "decrypted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    enc_path = filepath + ".enc"
    encrypt_file(filepath, enc_path)
    os.remove(filepath)  # remove unencrypted file
    return f"File encrypted and saved as {os.path.basename(enc_path)}"

@app.route('/download/<filename>')
def download(filename):
    enc_path = os.path.join(UPLOAD_FOLDER, filename + ".enc")
    dec_path = os.path.join(DECRYPT_FOLDER, filename)
    decrypt_file(enc_path, dec_path)
    return send_file(dec_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
