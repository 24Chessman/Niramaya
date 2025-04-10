from flask import Blueprint, jsonify, request
from flask_cors import CORS
from transformers import pipeline, BioGptTokenizer, BioGptForCausalLM
import google.generativeai as genai
import joblib
import os
import pandas as pd

# Create a Blueprint for disease predictor routes
AI_bp = Blueprint('health_AI', __name__)
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
    
# LR

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model_LR', 'disease_prediction_model.pkl')
MLB_PATH = os.path.join(BASE_DIR, 'model_LR', 'symptom_mlb.pkl')

model = joblib.load(MODEL_PATH)
mlb = joblib.load(MLB_PATH)
all_symptoms = mlb.classes_

# Prediction function
def predict_disease(user_input):
    user_symptoms = user_input.strip().lower().split()
    processed_input = ['_'.join(symptom.split()) for symptom in user_symptoms]
    input_data = [1 if symptom in processed_input else 0 for symptom in all_symptoms]
    prediction = model.predict([input_data])
    return prediction[0]

# LRv1
@AI_bp.route('/asklrv1', methods=['POST'])
def predict_lrv1():
    data = request.get_json()
    user_input = data.get('symptoms', '')
    if not user_input:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    # Diesease Prediction
    predicted_disease = predict_disease(user_input)

    # Description
    description_row = desc_df[desc_df['disease'].str.lower() == predicted_disease.lower()]
    description = description_row['description'].values[0] if not description_row.empty else 'No description found.'
    return jsonify({'predicted_disease': predicted_disease, "Description" : description})


# LRv2

DESC_PATH = os.path.join(BASE_DIR, 'model_LR', 'Symptom_Description.csv')
PRECAUTION_PATH = os.path.join(BASE_DIR, 'model_LR', 'Symptom_Precaution.csv')

desc_df = pd.read_csv(DESC_PATH)
prec_df = pd.read_csv(PRECAUTION_PATH)

# Clean column names just in case
desc_df.columns = desc_df.columns.str.lower().str.strip()
prec_df.columns = prec_df.columns.str.lower().str.strip()

@AI_bp.route('/asklrv2', methods=['POST'])
def predict_lrv2():
    data = request.get_json()
    user_input = data.get('symptoms', '')

    # Predict disease
    predicted_disease = predict_disease(user_input)

    # Get description
    description_row = desc_df[desc_df['disease'].str.lower() == predicted_disease.lower()]
    description = description_row['description'].values[0] if not description_row.empty else 'No description found.'

    # Get precautions
    precaution_row = prec_df[prec_df['disease'].str.lower() == predicted_disease.lower()]
    precautions = []
    if not precaution_row.empty:
        row = precaution_row.iloc[0]
        precautions = [v for k, v in row.items() if k.startswith('precaution') and pd.notna(v)]

    # Return the results
    return jsonify({
        'predicted_disease': predicted_disease,
        'description': description,
        'precautions': precautions
    })
