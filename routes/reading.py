from flask import Blueprint, request, jsonify
from services.srs_engine import evaluate_pronunciation
import os

reading_bp = Blueprint('reading', __name__)

@reading_bp.route('/evaluate', methods=['POST'])
def evaluate_reading():
    data = request.get_json()
    user_audio_path = data.get('audio_path')  # Lokasi audio dari pengguna
    correct_text = data.get('text')

    if not user_audio_path or not correct_text:
        return jsonify({'error': 'Audio atau teks tidak boleh kosong'}), 400

    # Evaluasi pelafalan
    transcribed_text, similarity_score = evaluate_pronunciation(user_audio_path, correct_text)

    # Umpan balik hasil evaluasi
    result = {
        "transcribed_text": transcribed_text,
        "similarity_score": similarity_score,
        "feedback": "Baik!" if similarity_score > 0.8 else "Cobalah lagi!"
    }

    return jsonify(result)
