from flask import Blueprint, jsonify
import psutil

analyze_system_bp = Blueprint("analyze_system", __name__)

@analyze_system_bp.route("/", methods=["GET"])
def analyze_system():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    is_distress = False
    reasons = []

    if cpu > 80:
        is_distress = True
        reasons.append(f"High CPU usage: {cpu}%")
    if memory > 80:
        is_distress = True
        reasons.append(f"High Memory usage: {memory}%")

    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "result": "distress" if is_distress else "normal",
        "reasons": reasons
    })
