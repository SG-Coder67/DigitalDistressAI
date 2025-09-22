# Save this as: backend/routes/analyze_url.py

from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
import sqlite3

# This is the line that was missing or broken, causing the ImportError
analyze_url_bp = Blueprint("analyze_url_bp", __name__)

DB_FILE = "threats.db"

def query_db_for_domain(domain):
    """Checks the SQLite database for a given domain."""
    conn = sqlite3.connect(DB_FILE)
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
    
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        return jsonify({"error": "Invalid URL format"}), 400
    
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
        "reasons": reasons,
        "redirect_url": "https://www.google.com" if result == "malicious" else url
    })