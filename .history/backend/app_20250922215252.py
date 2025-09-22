from flask import Flask, jsonify
from flask_cors import CORS

# Import your route blueprints
# For now, we are just using the URL analysis one
from routes.analyze_url import analyze_url_bp
# You can add your other blueprints here as you build them
# from routes.analyze_text import analyze_text_bp
# from routes.analyze_system import analyze_system_bp

# Initialize Flask app
app = Flask(__name__)

# This is the crucial line that allows your browser extension to connect.
CORS(app)

# Register blueprints with URL prefixes
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")
# app.register_blueprint(analyze_text_bp, url_prefix="/analyze/text")
# app.register_blueprint(analyze_system_bp, url_prefix="/analyze/system")

# Root endpoint to easily check if the backend is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Jarvis-Guardian Backend is running!"})

if __name__ == "__main__":
    # Run on localhost port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)