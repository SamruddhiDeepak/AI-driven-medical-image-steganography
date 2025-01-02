from flask import Blueprint, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Initialize Blueprint for backend1
backend1 = Blueprint('backend1', __name__)
CORS(backend1)

# Initialize Gemini API
GENAI_API_KEY = "AIzaSyDw00wmS7RyVjMSgkNIwK6ct6Iyx92DQq4"
genai.configure(api_key=GENAI_API_KEY)

def format_output(response_text):
    # Initialize sections
    diagnosis_section = []
    suggestions_section = []

    # Split the response into lines
    lines = response_text.split("\n")
    current_section = None

    # Iterate over the lines and classify them
    for line in lines:
        if "Diagnosis:" in line:
            current_section = "diagnosis"
        elif "Lifestyle Suggestions:" in line:
            current_section = "suggestions"
        elif line.strip():  # Ignore empty lines
            if current_section == "diagnosis":
                diagnosis_section.append(f"<li>{line.strip()}</li>")
            elif current_section == "suggestions":
                suggestions_section.append(f"<li>{line.strip()}</li>")

    # Handle missing sections
    if not diagnosis_section:
        diagnosis_section.append("<li>No diagnosis information provided.</li>")
    if not suggestions_section:
        suggestions_section.append("<li>No lifestyle suggestions provided.</li>")

    # Create formatted output with HTML list structure
    formatted_output = "<h3>Diagnosis:</h3><ul>" + "".join(diagnosis_section) + "</ul>"
    formatted_output += "<h3>Lifestyle Suggestions:</h3><ul>" + "".join(suggestions_section) + "</ul>"

    return formatted_output

def analyze_document(patient_text):
    # Prepare the prompt for the AI model
    prompt = (
        "You’re a knowledgeable health and wellness consultant with extensive experience in analyzing health-related text documents. "
        "Your expertise lies in diagnosing health issues based on provided information and suggesting appropriate lifestyle changes and best practices tailored to individual needs.\n"
        "Your task is to analyze the information extracted from a text document and provide a diagnosis along with recommended lifestyle changes and good practices. Here are the details from the text document that I’d like you to consider:\n"
        f"{patient_text}\n"
        "Provide a very short diagnosis and list lifestyle changes or good practices to follow in short, concise bullet points.\n"
        "Output should include:\n"
        "1. Diagnosis: Short summary of potential conditions.\n"
        "2. Lifestyle Suggestions: Practical recommendations.\n"
        "print diagnosis in one paragraph and lifestyle suggestions in one more and write everything pointwise in short. "
        "donot print stars and hash symbol"
    )

    try:
        # Call the generative AI model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Print raw response for debugging
        print("Raw Response from Gemini API:")
        print(response.text)

        # Clean and structure the response
        response_lines = response.text.strip().split("\n")
        cleaned_response = "\n".join(
            line.replace("#", "").replace("*", "").strip()
            for line in response_lines
            if "disclaimer" not in line.lower() and "educational purposes" not in line.lower()
        )

        print("Cleaned Response:")
        print(cleaned_response)

        # Format the response into structured output
        formatted_output = format_output(cleaned_response)
        return formatted_output  # Ensure this is returned as a string

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"Error: {str(e)}"}

@backend1.route('/analyze', methods=['POST'])
def analyze():
    # Ensure that a file is part of the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the content of the uploaded file
        patient_text = file.read().decode("utf-8")
        # Process the document and get formatted output
        results = analyze_document(patient_text)
        # Return the result as a JSON response
        return jsonify({"result": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
