from flask import Blueprint, request, jsonify
from urllib.parse import urlparse

analyze_url_bp = Blueprint("analyze_url_bp", __name__)

# Example rules
blacklisted_domains = [
    # General malicious
    "phishingsite.com",
    "spamlink.net",
    "malicious.com",
    "totally-safe-site.biz",
    "click-here-for-virus.info",
    # Fake brand login pages
    "login-apple-support.com",
    "facebook-secure-login.net",
    "amazn-rewards.com",
    "microsft-support.org",
    "wellsfargo-online-security.com",
    "chase-verification-center.com",
    
    # Urgent action required
    "secure-login-update.com",
    "verify-your-bank.com",
    "account-suspension-notice.net",
    "paypal-support.info",
    "your-package-has-been-detained.com",
    "tax-refund-claim.org"
]
shortened_urls = ["bit.ly", "tinyurl.com", "t.co"]
suspicious_keywords = ["free-money", "win-prize", "click-here"]

# Mapping malicious type to redirect
safe_redirects = {
    "phishing": "https://www.google.com",
    "spam": "https://www.wikipedia.org",
    "malware": "https://www.mozilla.org"
}

@analyze_url_bp.route("/", methods=["POST"])
@analyze_url_bp.route("", methods=["POST"])
def analyze_url():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    reasons = []
    site_type = "safe"

    domain = urlparse(url).netloc.lower()

    # Check blacklist
    if domain in blacklisted_domains:
        site_type = "phishing"
        reasons.append(f"Domain is blacklisted: {domain}")

    # Check shortened URLs
    if any(short in url for short in shortened_urls):
        site_type = "spam"
        reasons.append("Shortened URL detected (common in phishing)")

    # Check suspicious keywords
    for keyword in suspicious_keywords:
        if keyword in url.lower():
            site_type = "malware"
            reasons.append(f"Suspicious keyword detected: '{keyword}'")

    # Decide redirect
    redirect_url = safe_redirects.get(site_type, url)

    return jsonify({
        "input": url,
        "result": "malicious" if site_type != "safe" else "safe",
        "type": site_type,
        "reasons": reasons,
        "redirect_url": redirect_url
    })
