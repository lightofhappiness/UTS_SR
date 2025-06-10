from flask import Blueprint, request, jsonify, send_file
from services.tts_engine import generate_tts
import os

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/generate', methods=['POST'])
def tts_generate():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Teks tidak boleh kosong'}), 400

    audio_path = generate_tts(text)

    if audio_path and os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mp3')
    else:
        return jsonify({'error': 'Gagal menghasilkan audio'}), 500
