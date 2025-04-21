import pandas as pd
import wikipedia
import time
from tqdm import tqdm

# Load your dataset
df = pd.read_csv(r"D:\Nirman\Niramaya\HealthAI\backend\model_LR\disease_CSV\dis_sym_dataset_comb.csv")

# Extract unique diseases
diseases = sorted(df['label_dis'].unique())

desc_rows = []
prec_rows = []

for disease in tqdm(diseases, desc="Fetching disease info"):
    # — Get a 1–2 sentence summary
    try:
        summary = wikipedia.summary(disease, sentences=2, auto_suggest=False, redirect=True)
    except Exception:
        summary = "No summary available."

    # — Get “Prevention” section
    precautions = []
    try:
        page = wikipedia.page(disease, auto_suggest=False, redirect=True)
        for section in page.sections:
            if "prevent" in section.lower():
                text = page.section(section)
                # split into lines and strip bullets
                precautions = [line.strip("-* ") for line in text.split("\n") if line.strip()]
                break
    except Exception:
        precautions = []

    # Fallback if none found
    if not precautions:
        precautions = [
            "Maintain good hygiene",
            "Consult a healthcare professional if symptoms persist",
            "Follow government/public‑health guidelines"
        ]

    # Build row for description CSV
    desc_rows.append({
        "disease": disease,
        "description": summary
    })

    # Build row for precaution CSV (up to 4)
    pr = {"disease": disease}
    for i, p in enumerate(precautions[:4], start=1):
        pr[f"precaution_{i}"] = p
    prec_rows.append(pr)

    time.sleep(1)  # be polite to Wikipedia

# Save out two CSVs
pd.DataFrame(desc_rows).to_csv("Symptom_Description.csv", index=False)
pd.DataFrame(prec_rows).fillna("").to_csv("Symptom_Precaution.csv", index=False)

print("✅ Generated Symptom_Description.csv and Symptom_Precaution.csv")
