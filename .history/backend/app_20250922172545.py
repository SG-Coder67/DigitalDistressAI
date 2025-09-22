from flask import Flask, jsonify
from flask_cors import CORS
from routes.analyze_text import analyze_text_bp
from routes.analyze_url import analyze_url_bp
from routes.analyze_system import analyze_system_bp
from routes.analyze_audio import analyze_audio_bp

app = Flask(__name__)

# Register modular blueprints
app.register_blueprint(analyze_text_bp, url_prefix="/analyze/text")
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")
app.register_blueprint(analyze_system_bp, url_prefix="/analyze/system")
app.register_blueprint(analyze_audio_bp, url_prefix="/analyze/audio")

@app.route("/")
@app.route("/analyze/url", methods=["POST"], strict_slashes=False)
def home():
    return jsonify({"message": "🚀 Jarvis-Guardian Backend is running!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
