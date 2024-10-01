from flask import Flask, request, render_template, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json

app = Flask(__name__)

encryption_key = b'my_secret_encryption_key'

@app.route('/')
def index():
    return open('survey_form.html').read()

@app.route('/submit', methods=['POST'])
def submit_survey():
    # Retrieve survey responses
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age')

    survey_data = {
        'name': name,
        'email': email,
        'age': age
    }

    # Encrypt survey responses
    encrypted_data = encrypt_data(survey_data)

    # Redirect to the response page with encrypted data in the URL
    return redirect(url_for('show_responses', data=encrypted_data))

@app.route('/responses')
def show_responses():
    # Retrieve encrypted data from the URL query parameter
    encrypted_data = request.args.get('data', '')

    # Decrypt and display responses
    decrypted_responses = decrypt_data(encrypted_data)

    return render_template('responses.html', responses=decrypted_responses)

def encrypt_data(data):
    # Convert name to string if it's not already
    data['name'] = str(data.get('name', ''))

    json_data = json.dumps(data)

    # Initialize AES cipher
    cipher = AES.new(encryption_key, AES.MODE_CBC)

    # Pad the data to match AES block size
    padded_data = pad(json_data.encode('utf-8'), AES.block_size)

    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)

    # Base64 encode the ciphertext for safe transmission
    encrypted_data = base64.b64encode(ciphertext).decode('utf-8')

    return encrypted_data

def decrypt_data(encrypted_data):
    # Base64 decode the encrypted data
    ciphertext = base64.b64decode(encrypted_data)

    # Initialize AES cipher
    cipher = AES.new(encryption_key, AES.MODE_CBC)

    # Decrypt the data
    decrypted_data = cipher.decrypt(ciphertext)

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    try:
        # Try to decode the decrypted data as UTF-8
        decrypted_responses = json.loads(unpadded_data.decode('utf-8'))
    except UnicodeDecodeError:
        # If decoding as UTF-8 fails, handle the decrypted data as bytes
        decrypted_responses = unpadded_data

    return decrypted_responses







if __name__ == '__main__':
    app.run(debug=True)
