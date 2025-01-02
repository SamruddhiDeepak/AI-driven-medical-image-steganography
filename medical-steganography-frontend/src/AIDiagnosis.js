import React, { useState } from "react";
import axios from "axios";
import "./AIDiagnosis.css"; // Ensure custom styles are imported

const AIDiagnosis = () => {
  const [file, setFile] = useState(null); // State to store the selected file
  const [result, setResult] = useState(null); // State to store the diagnosis result
  const [error, setError] = useState(null); // State to store any error messages
  const [loading, setLoading] = useState(false); // State to track loading status

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null); // Clear previous errors when a new file is selected
  };

  // Handle file upload and communication with the backend
  const handleFileUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    setLoading(true); // Show loading indicator
    setError(null); // Clear previous errors

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Make a POST request to the backend
      const response = await axios.post("http://127.0.0.1:5000/backend1/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // Check if the response contains a result
      if (response.data.result) {
        setResult(response.data.result); // Set the result (formatted HTML)
        setError(null);
      } else {
        setError("No diagnosis result found.");
      }
    } catch (err) {
      setError("An error occurred while uploading the file. Please try again.");
    } finally {
      setLoading(false); // Hide loading indicator
    }
  };

  return (
    <div className="AIDiagnosis">
      <h1>Medical Diagnosis System</h1>
      <p>Upload a text file containing patient symptoms to get an AI-generated diagnosis and lifestyle suggestions.</p>

      <div className="upload-container">
        {/* File input for uploading the file */}
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleFileUpload} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* Display error messages */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Display the diagnosis result */}
      {result && (
        <div className="result-container">
          <h2>Diagnosis and Lifestyle Suggestions</h2>
          {/* Render HTML safely */}
          <div dangerouslySetInnerHTML={{ __html: result }} />
        </div>
      )}
    </div>
  );
};

export default AIDiagnosis;
