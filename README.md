# 🛡️ **AI-Driven Steganography for Medical Data Protection** 🩺

### **🌟 Overview**
In a world where healthcare is rapidly digitizing, protecting sensitive patient information is more critical than ever. Our AI-powered steganography system embeds confidential medical data into medical images seamlessly and securely. By blending advanced AI techniques with robust encryption, we ensure your data stays safe—without compromising usability.

---

### **✨ Features**
**Medical Image Classification:** Ensures only medical images are processed, powered by a CNN classifier with 98.5% accuracy.  
**AI-Driven LSB Detection:** Uses deep learning to identify optimal regions for embedding data.  
**Secure Encryption & Encoding:** Combines AES encryption and LSB steganography for robust security.  
**Authentication Layer:** RSA-secured password protection ensures only authorized users access the data.  
**Decoding & Decryption:** Retrieves and decrypts hidden patient data with precision.  
**Generative AI Diagnostics:** Analyzes symptoms and provides diagnostic suggestions with an accuracy of 89%.  
**User-Friendly Interface:** A seamless, intuitive workflow for encoding, decoding, and diagnostics.  

---

### **🚀 Project Workflow**

1. **Homepage**  
   Provides an introduction to the project and its objectives. Learn how this groundbreaking solution protects your sensitive data!  

2. **Encode Page**  
   - Input a **password** of your choice.  
   - Upload a **TXT file** containing sensitive data and a **medical image** for encoding.  
   - The AI classifier ensures the image is medical. If valid, encryption and encoding are performed.  
   - The encoded image is securely stored in a directory. Non-medical images are rejected.  

3. **Decode Page**  
   - Authenticate yourself by entering the **password**.  
   - Upload the encoded image to retrieve and decode hidden data.  
   - The system decrypts and provides the extracted data.  

4. **Diagnostics Page**  
   - Upload a document containing symptoms and health conditions.  
   - Leverage **Generative AI** for automated diagnostic insights and lifestyle suggestions.  

---

### **🛠️ Technologies Used**  

#### **🔍 Image Processing & Analysis**  
- **PyTorch & ResNet-18:** Built and executed the autoencoder for detecting anomalies in images and performing binary classification.  
- **TorchVision & PIL:** Preprocessed images, provided pre-trained models like ResNet-18, and ensured compatibility with the neural network input requirements.  
- **OpenCV:** Identified connected regions in binary masks for detailed image analysis.  
- **Matplotlib & ImageDraw:** Visualized results and annotated detected regions for better interpretability.  
- **CUDA:** Accelerated computations for handling large datasets and enhancing model performance.  

#### **💻 Frontend & Backend Integration**  
- **Frontend (React.js):**  
  - User-friendly interface for uploading images and interacting with the application.  
  - Axios for making POST requests to the Flask backend.  
- **Backend (Flask):**  
  - Handled file uploads and API requests.  
  - Loaded the pre-trained model (.pth files) and performed inference on user-provided images.  

#### **🧠 AI-Driven Analysis**  
- **Neural Network Architecture:** Leveraged ResNet-18 as the base model, with a custom fully connected layer for binary classification tasks.  
- **Google Generative AI (Gemini):** Enabled advanced text analysis for generating diagnostics and lifestyle recommendations.  

#### **🔒 Security & Steganography**  
- **AES Encryption & RSA Key Management:** Secured sensitive patient data with robust encryption and key protection mechanisms.  
- **AI-Driven LSB Detection:** Applied a deep learning autoencoder to identify optimal regions for data embedding.  

--- 


### **🚧 Future Enhancements**
- Integration with Electronic Health Records (EHRs).  
- Cloud-based data storage for enhanced accessibility.  
- Real-time analytics for data breach monitoring.  

---

**Let’s make healthcare data safer together! 💙**  
