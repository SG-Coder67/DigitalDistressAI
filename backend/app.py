from flask import Flask, jsonify
from flask_cors import CORS

# Import your route blueprints
from routes.analyze_text import analyze_text_bp
from routes.analyze_url import analyze_url_bp
from routes.analyze_system import analyze_system_bp
from routes.analyze_audio import analyze_audio_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints with URL prefixes
app.register_blueprint(analyze_text_bp, url_prefix="/analyze/text")
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")
app.register_blueprint(analyze_system_bp, url_prefix="/analyze/system")
app.register_blueprint(analyze_audio_bp, url_prefix="/analyze/audio")

# Root endpoint to check if backend is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Jarvis-Guardian Backend is running!"})

# Optional: test endpoint for backend health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Run on localhost port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
