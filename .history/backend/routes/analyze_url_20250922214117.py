# In backend/routes/analyze_url.py

from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

# ... (your lists of blacklisted domains, etc., are here) ...

@analyze_url_bp.route("", methods=["POST"]) # The route we fixed before
def analyze_url():
    # --- THIS IS THE NEW DEBUGGING CODE ---
    print("--- Received a new request for URL analysis ---")
    try:
        data = request.get_json()
        print(f"Request JSON data received: {data}") # <<< DEBUG PRINT #1
    except Exception as e:
        print(f"Error getting JSON from request: {e}")
        return jsonify({"error": "Could not parse JSON body"}), 400
    # ----------------------------------------

    if not data or "url" not in data:
        print("!!! Validation failed: 'data' is missing or 'url' key not in data.") # <<< DEBUG PRINT #2
        return jsonify({"error": "No URL provided in JSON body"}), 400

    url = data.get("url")
    
    # ... (the rest of your analysis logic is here) ...
    # ... (it should be fine, no need to change it) ...
    
    reasons = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Example check
    if domain in ["malicious.com"]:
        reasons.append("Domain is on a known blacklist.")

    is_malicious = len(reasons) > 0
    result = "malicious" if is_malicious else "safe"
    redirect_url = "https://www.google.com"

    return jsonify({
        "input_url": url,
        "result": result,
        "reasons": reasons,
        "redirect_url": redirect_url if is_malicious else url
    })