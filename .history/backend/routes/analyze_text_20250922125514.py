from flask import Blueprint, request, jsonify
from utils.models import ToxicityModel

analyze_text_bp = Blueprint("analyze_text", __name__)

# Initialize AI model (HuggingFace)
toxicity_model = ToxicityModel()

@analyze_text_bp.route("/", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Run AI model
    is_malicious, reasons = toxicity_model.predict(text)

    return jsonify({
        "input": text,
        "result": "malicious" if is_malicious else "safe",
        "reasons": reasons
    })
