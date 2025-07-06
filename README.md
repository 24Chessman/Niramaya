# 🩺 Niramaya – AI-Powered Health Symptom Checker

**Niramaya** is an AI-based health assistant that analyzes symptoms provided by users and predicts possible diseases using machine learning.  
It is designed for families, allowing multiple members under one account (like Netflix profiles).

This project was developed as part of an academic initiative to apply machine learning and Flask-based web development in a real-world healthcare context.

---

## 🚀 Features

- 🔍 Enter symptoms and get probable diseases predicted by an ML model (Naïve Bayes)
- 👥 Add multiple family members under a single login
- 🧠 Trained on the **AIIMS Clinical Symptom-Disease Dataset**
- 🖥️ Simple UI built with Flask, HTML, CSS, JacaScript
- 🗃️ Stores history of patient inputs and predictions

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| Language | Python |
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask |
| ML | scikit-learn, pandas, NumPy |
| Storage | PostgreSQL |
| Tools | Google Colab, VS Code, GitHub |

---

## 📦 How to Run Locally

> ⚠️ You need Python installed on your system.

```bash
# 1. Clone the repository
git clone https://github.com/24Chessman/Niramaya.git
cd Niramaya

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
