from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
import sqlite3

analyze_url_bp = Blueprint("analyze_url_bp", __name__)
DB_FILE = "threats.db" # The database file we created

def query_db_for_domain(domain):
    """Checks the SQLite database for a given domain."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT threat_type FROM threats WHERE domain = ?", (domain,))
    result = cursor.fetchone() # Get the first result
    conn.close()
    return result[0] if result else None

@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No 'url' key provided"}), 400

    url = data.get("url")
    reasons = []
    result = "safe"
    threat_type = "benign"
    
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        return jsonify({"error": "Invalid URL format"}), 400

    # Query the database for the domain
    db_threat = query_db_for_domain(domain)
    
    if db_threat:
        result = "malicious"
        threat_type = db_threat
        reasons.append(f"Domain found in threat database as '{threat_type}'.")

    redirect_url = "https://www.google.com" # A safe page to redirect to

    return jsonify({
        "input_url": url,
        "result": result,
        "type": threat_type,
        "reasons": reasons,
        "redirect_url": redirect_url if result == "malicious" else url
    })