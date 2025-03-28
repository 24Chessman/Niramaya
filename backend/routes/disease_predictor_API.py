from flask import Blueprint, jsonify, request
from flask_cors import CORS
from transformers import pipeline, BioGptTokenizer, BioGptForCausalLM

# Create a Blueprint for disease predictor routes
disease_bp = Blueprint('disease', __name__)
CORS(disease_bp)

# Load BioGPT Model and Tokenizer
model_name = "microsoft/biogpt"
tokenizer = BioGptTokenizer.from_pretrained(model_name)
model = BioGptForCausalLM.from_pretrained(model_name)

# Set up the text generation pipeline
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

@disease_bp.route("/askbiogpt", methods=["POST"])
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