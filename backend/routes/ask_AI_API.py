from flask import Blueprint, jsonify, request
from flask_cors import CORS
from transformers import pipeline, BioGptTokenizer, BioGptForCausalLM
import google.generativeai as genai

# Create a Blueprint for disease predictor routes
AI_bp = Blueprint('disease', __name__)
CORS(AI_bp)

# Load BioGPT Model and Tokenizer
model_name = "microsoft/biogpt"
tokenizer = BioGptTokenizer.from_pretrained(model_name)
model = BioGptForCausalLM.from_pretrained(model_name)

# Set up the text generation pipeline for BioGPT
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_medical_response(prompt, max_length=1000):
    """Generates a long medical response using BioGPT pipeline, matching Colab."""
    input_text = prompt
    responses = generator(
        input_text,
        max_length=max_length,
        num_return_sequences=10,
        do_sample=True
    )
    full_response = " ".join([resp["generated_text"] for resp in responses])
    return full_response

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCxcCXwbFRdEz6f92mXlVd1dBw7fqCQWew"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def generate_gemini_response(prompt):
    """Generates a response using the Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')  # Use the appropriate Gemini model
        response = model.generate_content(prompt)
        return response.text  # Returns the generated text
    except Exception as e:
        return str(e)

@AI_bp.route("/askbiogpt", methods=["POST"])
def ask_biogpt():
    """Handles user medical questions and generates answers using BioGPT."""
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "The 'question' field is required."}), 400

    try:
        answer = generate_medical_response(question)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@AI_bp.route("/askgemini", methods=["POST"])
def ask_gemini():
    """Handles user medical questions and generates answers using Gemini API."""
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "The 'question' field is required."}), 400

    try:
        answer = generate_gemini_response(question)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
