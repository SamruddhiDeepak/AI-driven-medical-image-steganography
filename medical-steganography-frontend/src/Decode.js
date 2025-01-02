import React, { useState } from 'react';
import './Decode.css';

function Decode() {
    const [password, setPassword] = useState(''); // State for password
    const [image, setImage] = useState(null); // State for uploaded image
    const [decryptedMessage, setDecryptedMessage] = useState(''); // State for decrypted message
    const [errorMessage, setErrorMessage] = useState(''); // State for error messages
    const [loading, setLoading] = useState(false); // State for loading spinner

    // Handle the image file change
    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImage(file); // Save the selected image file
        }
    };

    // Handle the password input change
    const handlePasswordChange = (event) => {
        setPassword(event.target.value); // Save the entered password
    };

    // Handle the decoding process when the "Decode" button is clicked
    const handleDecode = async () => {
        if (password && image) {
            setLoading(true);  // Start loading
            try {
                const formData = new FormData();
                formData.append('encoded_image', image); // Add image to FormData
                formData.append('password', password); // Add password to FormData

                // Send the request to the backend (backend3)
                const response = await fetch('http://localhost:5000/backend3/decode', {
                    method: 'POST',
                    body: formData, // Send the form data
                });

                if (response.ok) {
                    const data = await response.json(); // Get the JSON response
                    if (data.decrypted_text) {
                        setDecryptedMessage(data.decrypted_text); // Set decrypted message
                        setErrorMessage(''); // Reset error message
                    } else {
                        setErrorMessage('No decrypted text found.');
                        setDecryptedMessage('');
                    }
                } else {
                    setErrorMessage('Error while decoding the image.');
                    setDecryptedMessage('');
                }
            } catch (error) {
                setErrorMessage('An error occurred: ' + error.message);
                setDecryptedMessage('');
            } finally {
                setLoading(false);  // End loading
            }
        } else {
            setErrorMessage('Please provide both an image and a password.');
            setDecryptedMessage('');
        }
    };

    return (
        <div className="decoding-page">
            <header>
                <h1>Decoding Page</h1>
            </header>
            <main>
                <div className="form-container">
                    {/* Password Input */}
                    <label htmlFor="password">Enter Password:</label>
                    <input 
                        type="password" 
                        id="password" 
                        value={password} 
                        onChange={handlePasswordChange} 
                        placeholder="Password" 
                    />

                    {/* Image Upload Input */}
                    <label htmlFor="image">Upload Image:</label>
                    <input 
                        type="file" 
                        id="image" 
                        accept="image/*"
                        onChange={handleImageChange} 
                    />

                    {/* Decode Button */}
                    <button onClick={handleDecode}>Decode</button>
                </div>

                {/* Show Loading Spinner when the decode process is ongoing */}
                {loading && (
                    <div className="loading-spinner">
                        <p>Decoding...</p>
                    </div>
                )}

                {/* Display decrypted message or error */}
                <div className="result">
                    {decryptedMessage && <p>{decryptedMessage}</p>}
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                </div>
            </main>
        </div>
    );
}

export default Decode;
