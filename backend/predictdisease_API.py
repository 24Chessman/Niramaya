import re
import spacy
from flask import Flask, request, jsonify
from flask_cors import CORS
from symspellpy import SymSpell, Verbosity  # For spelling correction
import pkg_resources

app = Flask(__name__)
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

sym_spell = SymSpell()
sym_spell.load_dictionary(pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt"), term_index=0, count_index=1)

synonyms = {
    "tired": "fatigue",
    "exhausted": "fatigue",
    "lightheaded": "dizziness",
    "queasy": "nausea",
    "aching": "pain",
    "sore": "pain"
}

# Sample Disease Dictionary (For Testing)
disease_dict = {
    "fever cough fatigue": "Flu",
    "headache nausea dizziness": "Migraine",
    "chest pain shortness of breath": "Heart Disease",
    "rash itching redness": "Allergy",
}

def preprocess_text(text):
    """Convert user symptoms into clean tokens with enhanced NLP processing."""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters

    # Correct spelling mistakes
    words = text.split()
    corrected_words = [sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)[0].term if sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2) else word for word in words]
    corrected_text = " ".join(corrected_words)

    # Process with NLP model
    doc = nlp(corrected_text)

    # Named Entity Recognition (NER) for symptom extraction
    symptoms = []
    for token in doc:
        if not token.is_stop and token.is_alpha:
            # Replace synonyms with standard medical terms
            symptom = synonyms.get(token.lemma_, token.lemma_)
            symptoms.append(symptom)

    return " ".join(symptoms)  # Return as a clean string

def predict_disease(processed_text):
    """Predict disease based on symptoms using word matching."""
    processed_set = set(processed_text.split())

    for symptoms, disease in disease_dict.items():
        symptom_set = set(symptoms.split())
        if len(processed_set & symptom_set) > 0:  # At least one match
            return disease
    
    return "Unknown Disease"

@app.route('/predictdisease', methods=['POST'])
def predict():
    """API Endpoint: Takes symptoms, processes them, and predicts disease."""
    data = request.json
    user_input = data.get("user_input", "").strip()
    
    if not user_input:
        return jsonify({"error": "No symptoms provided"}), 400

    # Step 1: Convert Symptoms into Tokens
    processed_text = preprocess_text(user_input)

    # Step 2: Predict Disease
    prediction = predict_disease(processed_text)

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
