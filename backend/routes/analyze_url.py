from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
import sqlite3
import joblib
import os

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BACKEND_DIR, "threats.db")
MODEL_PATH = os.path.join(BACKEND_DIR, "url_model.joblib")
VECTORIZER_PATH = os.path.join(BACKEND_DIR, "url_vectorizer.joblib")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def query_db_for_domain(domain):
    # ... (this function is correct and doesn't need to change)
    if not os.path.exists(DB_PATH): return None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT threat_type FROM threats WHERE domain = ?", (domain,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_threat_to_db(domain, threat_type, source):
    """Adds a newly discovered threat to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO threats (domain, threat_type, source) VALUES (?, ?, ?)", (domain, threat_type, source))
    conn.commit()
    conn.close()
    print(f"--- New threat added to DB: {domain} (Source: {source}) ---")

@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    # ... (code to get url and domain is the same)
    data = request.get_json()
    if not data or "url" not in data: return jsonify({"error": "No 'url' key provided"}), 400
    url = data.get("url")
    domain = urlparse(url).netloc.lower()
    
    db_threat = query_db_for_domain(domain)
    
    if db_threat:
        result = "malicious"
        reasons = [f"Domain is on the known threat list as '{db_threat}'."]
        threat_type = db_threat
    else:
        url_vector = vectorizer.transform([url])
        prediction = model.predict(url_vector)
        
        if prediction[0] == 1:
            result = "malicious"
            reasons = ["AI model predicted this URL is a potential threat."]
            threat_type = "phishing"
            add_threat_to_db(domain, threat_type, 'ai_classified')
        else:
            result = "safe"
            reasons = ["AI model predicted this URL is safe."]
            threat_type = "benign"

    return jsonify({
        "input_url": url,
        "result": result,
        "type": threat_type,
        "reasons": reasons,
        "redirect_url": "https://www.google.com" if result == "malicious" else url
    })