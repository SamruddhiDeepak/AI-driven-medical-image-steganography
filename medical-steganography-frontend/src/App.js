import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom'; 
import './App.css';
import AIDiagnosis from './AIDiagnosis'; 
import Encode from './Encode';
import Decode from './Decode';


const App = () => {
    return (
        <Router>
            <div className="App">
                {/* Navbar */}
                <div className="navbar">
                    <ul className="nav-links">
                        <li><Link to="/">Home</Link></li> 
                        <li><Link to="/encode">Encode</Link></li>
                        <li><Link to="/decode">Decode</Link></li>
                        <li><Link to="/aidiagnosis">AI Diagnosis</Link></li>
                    </ul>
                </div>

                <Routes>
                    {/* Home Route */}
                    <Route
                        path="/"
                        element={
                            <div className="hero-section">
                                <div className="hero-text">
                                    <h1>AI Steganography for Secure Medical Data Embedding</h1>
                                    <p>Where AI meets Steganography to protect what matters most. We embed the future of healthcare into every pixel—secure, invisible, unbreakable. Your medical data, safely hidden within CT scans and MRIs, powered by advanced AI precision and next-gen decoding.</p>
                                </div>
                            </div>
                        }
                    />

                    <Route path="/encode" element={<Encode />} />

                    {/* Contact Route */}
                    <Route path="/aidiagnosis" element={<AIDiagnosis />} />

                    <Route path="/decode" element={<Decode />} />

                </Routes>
            </div>
        </Router>
    );
};

export default App;