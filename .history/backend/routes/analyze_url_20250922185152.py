from flask import Flask, jsonify
from analyze_url import analyze_url_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from frontend

# Register blueprint
app.register_blueprint(analyze_url_bp, url_prefix="/analyze/url")

@app.route("/")
def home():
    return jsonify({"message": "Web Protector backend is running!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
