from flask import Flask
from flask_cors import CORS
from routes.analyze_text import analyze_text_bp
from routes.analyze_url import analyze_url_bp
from routes.analyze_system import analyze_system_bp
from routes.analyze_audio import analyze_audio_bp

app = Flask(__name__)
CORS(app)  # enable CORS for testing

# Register blueprints
app.register_blueprint(analyze_text_bp, url_prefix="/analyze/text")
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")
app.register_blueprint(analyze_system_bp, url_prefix="/analyze/system")
app.register_blueprint(analyze_audio_bp, url_prefix="/analyze/audio")

# Root check only
@app.route("/")
def home():
    return {"message": "🚀 Jarvis-Guardian Backend is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
