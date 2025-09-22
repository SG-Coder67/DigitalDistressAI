# Save this as: backend/routes/analyze_url.py

from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
import sqlite3
import os

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

# --- THIS IS THE FIX ---
# Create an absolute path to the database file to avoid confusion.
# This assumes your 'backend' folder is the current working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "threats.db")
# --------------------

def query_db_for_domain(domain):
    """Checks the SQLite database for a given domain."""
    # Add a check to ensure the database file actually exists.
    if not os.path.exists(DB_PATH):
        print(f"!!! DATABASE FILE NOT FOUND at {DB_PATH} !!!")
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT threat_type FROM threats WHERE domain = ?", (domain,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No 'url' key provided"}), 400

    url = data.get("url")
    domain = urlparse(url).netloc.lower()
    
    db_threat = query_db_for_domain(domain)
    
    if db_threat:
        result = "malicious"
        reasons = [f"Domain found in threat database as '{db_threat}'."]
    else:
        result = "safe"
        reasons = []

    return jsonify({
        "input_url": url,
        "result": result,
        "type": db_threat if db_threat else "benign",
        "reasons": reasons,
        "redirect_url": "https://www.google.com" if result == "malicious" else url
    })