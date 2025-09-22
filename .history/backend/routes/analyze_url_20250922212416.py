from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

# --- Data for analysis ---
blacklisted_domains = ["phishingsite.com", "spamlink.net", "malicious.com"]
shortened_domains = ["bit.ly", "tinyurl.com", "t.co"]
suspicious_keywords = ["free-money", "win-prize", "click-here", "verify-account"]

@analyze_url_bp.route("/", methods=["POST"])
def analyze_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data.get("url")
    reasons = []
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
    except Exception:
        return jsonify({"error": "Invalid URL format"}), 400

    # --- Analysis Logic ---
    
    # 1. Check if the domain is blacklisted
    if domain in blacklisted_domains:
        reasons.append(f"Domain is on a known blacklist: {domain}")

    # 2. Check if the domain is a known URL shortener
    if domain in shortened_domains:
        reasons.append("URL uses a shortener, which can hide the true destination.")

    # 3. Check for suspicious keywords in the entire URL
    for keyword in suspicious_keywords:
        if keyword in url.lower():
            reasons.append(f"Suspicious keyword found: '{keyword}'")

    # --- Final Decision ---
    is_malicious = len(reasons) > 0
    result = "malicious" if is_malicious else "safe"
    
    # For the demo, we can just redirect to a safe "blocked" page or Google
    redirect_url = "https://www.google.com" 

    return jsonify({
        "input_url": url,
        "result": result,
        "reasons": reasons,
        "redirect_url": redirect_url if is_malicious else url
    })