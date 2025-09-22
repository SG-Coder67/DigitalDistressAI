from flask import Blueprint, request, jsonify

analyze_text_bp = Blueprint("analyze_text_bp", __name__)

malicious_words = ["buy now", "click here", "free money", "win prize"]

@analyze_text_bp.route("", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("input", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    reasons = []
    is_malicious = False

    for word in malicious_words:
        if word in text.lower():
            is_malicious = True
            reasons.append(f"Suspicious keyword detected: '{word}'")

    return jsonify({
        "input": text,
        "result": "malicious" if is_malicious else "safe",
        "reasons": reasons
    })
