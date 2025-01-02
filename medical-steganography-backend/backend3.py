from flask import Blueprint, request, jsonify
from cryptography.fernet import Fernet
import base64
import os
from PIL import Image
import numpy as np
from flask_cors import CORS

backend3 = Blueprint('backend3', __name__)
CORS(backend3, origins="http://localhost:3000")

# Function to decrypt the text file using password
def decrypt_text_file(encrypted_text, password):
    try:
        key = base64.urlsafe_b64encode(password.encode('utf-8').ljust(32, b'\0'))
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text).decode('utf-8')
        return decrypted_text
    except Exception as e:
        raise ValueError(f"Error decrypting text: {str(e)}")

# Function to extract encrypted data from an image
def extract_from_image(image_path):
    try:
        print(f"Opening image file: {image_path}")  # Logging image file path
        img = Image.open(image_path)
        img = img.convert('RGB')  # Ensure the image is in RGB format
        pixels = np.array(img)
        print(f"Image dimensions: {pixels.shape}")  # Log image dimensions

        binary_data = ''
        
        # Extract binary data from the LSB (Least Significant Bit) of RGB components
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                pixel = pixels[i, j]
                r, g, b = pixel
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

        print(f"Extracted binary data length: {len(binary_data)}")  # Log binary data length

        # Convert the binary data into bytes
        byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        encrypted_data = bytearray(int(b, 2) for b in byte_data)
        
        # Ensure the data is in the correct format (bytes) for decryption
        if len(encrypted_data) == 0:
            raise Exception("No data extracted from the image.")

        return bytes(encrypted_data)  # Ensure it's in bytes format
        
    except Exception as e:
        print(f"Error extracting data from image: {e}")  # Detailed logging for image extraction error
        raise Exception(f"Error extracting data from image: {e}")

# API route to decode the file
@backend3.route('/decode', methods=['POST'])
def decode_file():
    try:
        # Get files and password from the request
        image_file = request.files.get('encoded_image')
        password = request.form.get('password')

        if not image_file or not password:
            return jsonify({"error": "Missing image or password."}), 400

        # Save the encoded image temporarily
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        encoded_image_path = os.path.join(upload_folder, image_file.filename)
        image_file.save(encoded_image_path)

        # Extract encrypted data from the image
        encrypted_text = extract_from_image(encoded_image_path)

        # Decrypt the data using the provided password
        decrypted_text = decrypt_text_file(encrypted_text, password)

        # Return the decrypted text as a response
        return jsonify({'decrypted_text': decrypted_text})

    except Exception as e:
        print(f"Error while decoding: {e}")
        return jsonify({"error": str(e)}), 500

