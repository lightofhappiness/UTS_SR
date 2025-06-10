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
    return render_template("reading.html",
                           huruf=soal["huruf"],
                           latin=soal["latin"],
                           id=soal["id"])


# ------------------------
# API untuk Evaluasi Latihan Membaca (Reading)
# ------------------------
@app.route("/api/reading/evaluate", methods=["POST"])
def evaluate_reading():
    data = request.json
    user_answer = data.get("user_answer").lower()
    question_id = data.get("question_id")

    with open("data/data_soal_reading.json", "r", encoding="utf-8") as f:
        soal_list = json.load(f)

    soal = next((item for item in soal_list if item["id"] == question_id), None)

    if soal:
        is_correct = soal["latin"].lower() == user_answer
        return jsonify({"is_correct": is_correct})
    else:
        return jsonify({"error": "Soal tidak ditemukan"}), 404

# ------------------------
# Latihan Menulis (Writing)
# ------------------------
@app.route('/writing')
def writing():
    # Baca file soal
    with open("data/data_soal_writing.json", "r", encoding="utf-8") as f:
        data_soal = json.load(f)

    # Baca kata untuk distraktor
    with open("data/data_kata_random.json", "r", encoding="utf-8") as f:
        data_kata = json.load(f)  # pastikan isinya list kata ["lalajo", "ka pasar", ...]

    soal = random.choice(data_soal)
    kalimat = soal["kalimat"]
    correct_sentence = soal["correct_sentence"]  # sudah berupa list kata

    # Buat kata acak dari jawaban benar
    kata_acak = correct_sentence.copy()

    # Tambahkan distraktor, hindari duplikat dengan correct_sentence
    distraktor = []
    correct_lower = set(k.lower() for k in correct_sentence)

    while len(distraktor) < 3:
        kata = random.choice(data_kata)
        if kata.lower() not in correct_lower and kata not in distraktor:
            distraktor.append(kata)

    # Gabungkan kata benar + distraktor, lalu acak
    semua_kata = kata_acak + distraktor
    random.shuffle(semua_kata)

    return render_template( "writing.html", 
        id=soal['id'],  # pastikan ada id,
        jawaban= kalimat,
        correct= correct_sentence,
        kata= semua_kata
    ) 





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


@app.route('/')
def home():
    return render_template('home.html')


# ------------------------
# Jalankan Aplikasi
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)