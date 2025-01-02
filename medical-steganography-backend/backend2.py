from flask import Blueprint, request, send_file, jsonify
from cryptography.fernet import Fernet
import base64
import os
from PIL import Image
import numpy as np
from flask_cors import CORS
import torch
import torch.nn as nn
from torchvision import models, transforms
import uuid

backend2 = Blueprint('backend2', __name__)
CORS(backend2, origins="http://localhost:3000")

# Function to load the medical image classifier model
def load_model(model_path='medical_classifier.pth'):
    model = models.resnet18(weights=None)  # Initialize model without pre-trained weights
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_features, 1),
        nn.Sigmoid()
    )
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Set the model to evaluation mode
    return model

# Function to preprocess the image for classification
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert('RGB')  # Ensure image is RGB
    return transform(image).unsqueeze(0)  # Add batch dimension

# Function to classify the image
def is_medical_image(image_path, model, threshold=0.5):
    image_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(image_tensor)
        probability = output.item()
        return probability <= threshold  # True if classified as medical

# Function to encrypt the text file using password
def encrypt_text_file(text, password):
    try:
        key = base64.urlsafe_b64encode(password.encode('utf-8').ljust(32, b'\0'))
        fernet = Fernet(key)
        encrypted_text = fernet.encrypt(text.encode('utf-8'))
        return encrypted_text
    except Exception as e:
        raise ValueError(f"Error encrypting text: {str(e)}")

# Function to encode the encrypted data into an image
def encode_into_image(encrypted_data, image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')  # Ensure image is in RGB format

        binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)
        pixels = np.array(img)
        data_index = 0

        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                if data_index < len(binary_data):
                    pixel = pixels[i, j]
                    r, g, b = pixel
                    r = r & 0xFE | int(binary_data[data_index])
                    data_index += 1
                    if data_index < len(binary_data):
                        g = g & 0xFE | int(binary_data[data_index])
                        data_index += 1
                    if data_index < len(binary_data):
                        b = b & 0xFE | int(binary_data[data_index])
                        data_index += 1
                    pixels[i, j] = [r, g, b]

        encoded_image_path = f'encoded_image_{uuid.uuid4().hex}.png'
        encoded_image = Image.fromarray(pixels)
        os.makedirs('uploads', exist_ok=True)
        encoded_image.save(os.path.join('uploads', encoded_image_path))
        return os.path.join('uploads', encoded_image_path)

    except Exception as e:
        raise ValueError(f"Error encoding the image: {str(e)}")

@backend2.route('/encode', methods=['POST'])
def encode_file():
    try:
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)

        text_file = request.files['text_file']
        password = request.form['password']
        image_file = request.files['image_file']

        # Save the uploaded image temporarily
        temp_image_path = os.path.join(upload_folder, f'temp_{uuid.uuid4().hex}.png')
        image_file.save(temp_image_path)

        # Load the classifier model
        model = load_model()

        # Check if the image is classified as medical
        if not is_medical_image(temp_image_path, model):
            os.remove(temp_image_path)  # Clean up the temporary file
            return jsonify({"error": "The uploaded image is classified as non-medical. Please upload a valid medical image."}), 400

        # Read text from the text file
        text = text_file.read().decode('utf-8')

        # Encrypt the text using the password
        encrypted_text = encrypt_text_file(text, password)

        # Encode the encrypted text into the image
        encoded_image_path = encode_into_image(encrypted_text, temp_image_path)

        # Remove the temporary image file
        os.remove(temp_image_path)

        return send_file(encoded_image_path, as_attachment=True, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
