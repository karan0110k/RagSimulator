from flask import Blueprint, request, jsonify
from services.rag_pipeline import run_rag

chat_bp = Blueprint("chat", __name__)

chat_history = []

@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query missing"}), 400

    answer, model_used, confidence = run_rag(query)

    chat_entry = {
        "question": query,
        "answer": answer,
        "model": model_used,
        "confidence": confidence
    }

    chat_history.append(chat_entry)

    return jsonify(chat_entry)


@chat_bp.route("/history", methods=["GET"])
def history():
    return jsonify(chat_history)