from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

blacklisted_domains = ["phishingsite.com", "spamlink.net", "malicious.com"]
shortened_urls = ["bit.ly", "tinyurl.com", "t.co"]
suspicious_keywords = ["free-money", "win-prize", "click-here"]

@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    data = request.get_json()
    url = data.get("input", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    reasons = []
    is_malicious = False

    domain = urlparse(url).netloc.lower()
    if domain in blacklisted_domains:
        is_malicious = True
        reasons.append(f"Domain is blacklisted: {domain}")

    if any(short in url for short in shortened_urls):
        is_malicious = True
        reasons.append("Shortened URL detected (common in phishing).")

    for keyword in suspicious_keywords:
        if keyword in url.lower():
            is_malicious = True
            reasons.append(f"Suspicious keyword detected: '{keyword}'")

    return jsonify({
        "input": url,
        "result": "malicious" if is_malicious else "safe",
        "reasons": reasons
    })
