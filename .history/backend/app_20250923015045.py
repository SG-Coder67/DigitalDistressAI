# In backend/app.py

from flask import Flask, jsonify
from flask_cors import CORS

# Import BOTH of your route blueprints
from routes.analyze_url import analyze_url_bp
from routes.analyze_text import analyze_text_bp # <-- 1. ADD THIS IMPORT

app = Flask(__name__)
CORS(app)

# Register BOTH blueprints
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")
app.register_blueprint(analyze_text_bp, url_prefix="/analyze/text") # <-- 2. ADD THIS LINE

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Jarvis-Guardian Backend is running!"})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)