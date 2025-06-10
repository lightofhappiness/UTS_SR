from flask import Blueprint, request, jsonify
from services.word_arrangement_checker import check_word_arrangement

writing_bp = Blueprint('writing', __name__)

@writing_bp.route('/start', methods=['POST'])
def start_word_arrangement():
    data = request.get_json()
    target_sentence = data.get('target_sentence')  # Kalimat yang benar
    words = data.get('words')  # Kata-kata yang teracak

    if not target_sentence or not words:
        return jsonify({'error': 'Kalimat atau kata tidak boleh kosong'}), 400

    # Kirim kata-kata teracak untuk latihan menyusun kata
    return jsonify({'words': words, 'target_sentence': target_sentence})

@writing_bp.route('/evaluate', methods=['POST'])
def evaluate_word_arrangement():
    """
    Evaluasi susunan kata yang dimasukkan pengguna dan bandingkan dengan kalimat yang benar.
    """
    data = request.get_json()
    user_input = data.get('user_input')  # Susunan kata dari pengguna
    correct_sentence = data.get('target_sentence')

    if not user_input or not correct_sentence:
        return jsonify({'error': 'Input atau kalimat yang benar tidak boleh kosong'}), 400

    # Periksa apakah susunan kata yang dimasukkan pengguna benar
    is_correct, feedback = check_word_arrangement(user_input, correct_sentence)

    result = {
        "is_correct": is_correct,
        "feedback": feedback
    }

    

    return jsonify(result)
