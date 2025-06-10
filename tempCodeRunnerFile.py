@app.route("/api/writing/evaluate", methods=["POST"])
def evaluate_writing():
    # Menerima data dari frontend yang berisi kalimat susunan pengguna
    data = request.json
    user_sentence = data.get("user_sentence", [])
    
    # Kalimat yang benar untuk latihan menulis
    correct_sentence = ["abdi", "badé", "ka", "kacamatan"]
    
    # Cek apakah susunan kata pengguna sudah benar
    is_correct = (user_sentence == correct_sentence)
    
    # Kirimkan hasil evaluasi ke frontend
    return jsonify({"is_correct": is_correct})

