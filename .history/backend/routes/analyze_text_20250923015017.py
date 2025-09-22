# Save this as: backend/routes/analyze_text.py

from flask import Blueprint, request, jsonify
from transformers import pipeline

analyze_text_bp = Blueprint("analyze_text_bp", __name__)

# This line loads the AI model from Hugging Face when the server starts.
print("Loading toxicity analysis model...")
toxicity_analyzer = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    truncation=True
)
print("Toxicity model loaded.")


@analyze_text_bp.route("", methods=["POST"])
def analyze_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No 'text' key provided"}), 400

    text_to_analyze = data.get("text")

    # Use the AI model to get results
    results = toxicity_analyzer(text_to_analyze)
    
    # Determine if the primary result is toxic
    is_toxic = any(item['label'] == 'toxic' and item['score'] > 0.8 for item in results)

    return jsonify({
        "input_text": text_to_analyze,
        "result": "malicious" if is_toxic else "safe", # Use 'malicious' to match your JS
        "type": "toxic_text" if is_toxic else "benign_text",
        "reasons": [f"Detected as '{res['label']}' with score {res['score']:.2f}" for res in results]
    })