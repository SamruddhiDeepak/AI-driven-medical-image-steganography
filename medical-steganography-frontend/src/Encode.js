import React, { useState } from "react";
import axios from "axios";
import './Encode.css';

function Encode() {
  const [textFile, setTextFile] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleEncode = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    setIsLoading(true);

    // Validate input
    if (!textFile || !imageFile || !password) {
      setErrorMessage("Please provide all required inputs.");
      setIsLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append("text_file", textFile);
      formData.append("image_file", imageFile);
      formData.append("password", password);

      // Send the request to the backend
      const response = await axios.post("http://localhost:5000/backend2/encode", formData, {
        responseType: "blob", // Expect a binary response (file)
      });

      // Handle the file response and download it
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "encoded_image.png"); // Default download name
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      // Improved error handling
      const message = error.response
        ? error.response.data?.error || "An error occurred while encoding the file."
        : error.message || "Unexpected error occurred.";
      setErrorMessage(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="encode">
      <h1>Encode Text into Image</h1>
      <form onSubmit={handleEncode}>
        {/* Text File Input */}
        <div className="upload-container">
          <label htmlFor="textFile">Upload Text File:</label>
          <input
            type="file"
            id="textFile"
            accept=".txt"
            onChange={(e) => setTextFile(e.target.files[0])}
            required
          />
        </div>

        {/* Image File Input */}
        <div className="upload-container">
          <label htmlFor="imageFile">Upload Image File:</label>
          <input
            type="file"
            id="imageFile"
            accept="image/*"
            onChange={(e) => setImageFile(e.target.files[0])}
            required
          />
        </div>

        {/* Password Input */}
        <div className="upload-container">
          <label htmlFor="password">Enter Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {/* Error Message */}
        {errorMessage && <p className="error">{errorMessage}</p>}

        {/* Submit Button */}
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Encoding..." : "Encode"}
        </button>
      </form>
    </div>
  );
}

export default Encode;
