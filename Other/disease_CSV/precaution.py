import pandas as pd
import wikipedia
import time
from tqdm import tqdm

# Load dataset
df = pd.read_csv(r"D:\Nirman\Niramaya\HealthAI\backend\model_LR\disease_CSV\dis_sym_dataset_comb.csv")
diseases = sorted(df['label_dis'].unique())

# Keywords to identify relevant Wikipedia sections
precaution_keywords = ['prevent', 'management', 'treatment', 'lifestyle', 'self-care', 'home remedy']

new_precaution_rows = []

for disease in tqdm(diseases, desc="Creating new precaution list"):
    precautions = []

    try:
        # Fetch Wikipedia page with auto-suggest enabled
        page = wikipedia.page(disease, auto_suggest=True, redirect=True)

        # Check each section for relevant content
        for section in page.sections:
            if any(keyword in section.lower() for keyword in precaution_keywords):
                text = page.section(section)
                if text:
                    # Split text into lines
                    lines = text.split("\n")
                    for line in lines:
                        line = line.strip()
                        # Look for list items (bullet points)
                        if line.startswith(('* ', '- ', '• ')):
                            precaution = line[2:].strip()  # Remove bullet marker
                            if precaution:  # Ensure it’s not empty
                                precautions.append(precaution)
                        if len(precautions) >= 4:
                            break
                if len(precautions) >= 4:
                    break

    except Exception:
        precautions = []  # Reset if page fetch fails

    # Fallback if fewer than 4 precautions are found
    default_precautions = [
        "Maintain proper hygiene",
        "Consult a healthcare professional",
        "Avoid self-medication",
        "Follow recommended lifestyle practices",
        "Ensure regular health check-ups",
        "Stay hydrated and eat balanced meals"
    ]

    while len(precautions) < 4:
        for default in default_precautions:
            if default not in precautions:
                precautions.append(default)
            if len(precautions) == 4:
                break

    # Build row for CSV
    row = {"disease": disease}
    for i in range(4):
        row[f"precaution_{i+1}"] = precautions[i]
    new_precaution_rows.append(row)

    time.sleep(1)  # Respectful delay to Wikipedia

# Save to new CSV file
output_path = r"D:\Nirman\Niramaya\HealthAI\backend\model_LR\disease_CSV\Symptom_Precaution_New.csv"
pd.DataFrame(new_precaution_rows).to_csv(output_path, index=False)

print(f"✅ New precaution file saved as: {output_path}")