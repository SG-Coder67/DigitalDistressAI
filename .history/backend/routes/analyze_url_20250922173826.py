from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

# Example blacklisted domains
blacklisted_domains = ["phishingsite.com", "spamlink.net", "malicious.com"]

# Common URL shorteners (often used in phishing)
shortened_urls = ["bit.ly", "tinyurl.com", "t.co"]

@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    """
    Analyze the given URL for malicious characteristics.
    Expects JSON: { "input": "<URL to check>" }
    """
    data = request.get_json()
    url = data.get("input", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    reasons = []
    is_malicious = False

    # Extract domain
    try:
        domain = urlparse(url).netloc.lower()
    except Exception:
        domain = ""

    # Check blacklist
    if domain in blacklisted_domains:
        is_malicious = True
        reasons.append(f"Domain is blacklisted: {domain}")

    # Check for URL shorteners
    if any(short in url for short in shortened_urls):
        is_malicious = True
        reasons.append("Shortened URL detected (common in phishing).")

    # Check for suspicious keywords in URL
    suspicious_keywords = ["free-money", "win-prize", "click-here"]
    for keyword in suspicious_keywords:
        if keyword in url.lower():
            is_malicious = True
            reasons.append(f"Suspicious keyword detected: '{keyword}'")

    return jsonify({
        "input": url,
        "result": "malicious" if is_malicious else "safe",
        "reasons": reasons
    })
