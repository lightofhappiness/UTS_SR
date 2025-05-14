from flask import Flask, render_template, request, jsonify
#from services import srs_engine, tts_engine  # jika ada backend handler nanti
import random 
import json
#import writing.py

app = Flask(__name__)

# ------------------------
# Halaman Utama (Beranda)
# ------------------------
# Load soal dari file JSON



@app.route("/")
def index():
    return render_template("index.html")


# ------------------------
# Latihan Membaca (Reading)
# ------------------------
@app.route('/reading')
def reading():
    with open("data/data_soal_reading.json", "r", encoding="utf-8") as f:
        soal_list = json.load(f)
    soal = random.choice(soal_list)
    return render_template("reading.html", huruf=soal["huruf"], latin=soal["latin"], gambar=soal["gambar"])

# ------------------------
# API untuk Evaluasi Latihan Membaca (Reading)
# ------------------------
@app.route("/api/reading/evaluate", methods=["POST"])
def evaluate_reading():
    data = request.json
    user_answer = data.get("user_answer")
    question_id = data.get("question_id")

    # Ambil soal dari file
    with open("data/data_soal_reading.json", "r", encoding="utf-8") as f:
        soal_list = json.load(f)

    # Temukan soal yang sesuai
    soal = next((item for item in soal_list if item["id"] == question_id), None)

    if soal:
        is_correct = soal["latin"].lower() == user_answer.lower()
        return jsonify({"is_correct": is_correct})
    else:
        return jsonify({"error": "Soal tidak ditemukan"}), 404

# ------------------------
# Latihan Menulis (Writing)
# ------------------------
@app.route('/writing')
def writing():
    with open("data/data_soal_writing.json", "r", encoding="utf-8") as f:
        data_soal = json.load(f)
    soal = random.choice(data_soal)
    kalimat = soal["kalimat"]
    correct_sentence = soal["correct_sentence"] 
    kata_acak = kalimat.split()
    random.shuffle(kata_acak)
    return render_template("writing.html", kata=kata_acak, jawaban=kalimat, correct = correct_sentence, id=soal["id"])




# ------------------------
# API untuk Evaluasi Latihan Menulis (Writing)
# ------------------------

@app.route("/api/writing/evaluate", methods=["POST"])
def evaluate_writing():
    data = request.json
    user_sentence = data.get("user_sentence", [])
    correct_sentence = data.get("correct_sentence", [])
    question_id = data.get("question_id")
    with open("data/data_soal_writing.json", "r", encoding="utf-8") as f:
        data_soal = json.load(f)
    soal = next((item for item in data_soal if item["id"] == question_id), None)

    if soal:
        correct_sentence = soal["correct_sentence"]
        is_correct = user_sentence == correct_sentence
        return jsonify({"is_correct": is_correct})
    else:
        return jsonify({"error": "Soal tidak ditemukan"}), 404




# ------------------------
# Jalankan Aplikasi
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)