from google.cloud import speech
import io

def evaluate_pronunciation(user_audio_path, correct_text):
    """
    Menggunakan Google Cloud Speech-to-Text untuk menganalisis pelafalan pengguna
    dan membandingkannya dengan teks yang benar.
    """

    # Inisialisasi client Google Cloud Speech
    client = speech.SpeechClient()

    # Membaca file audio
    with io.open(user_audio_path, "rb") as audio_file:
        content = audio_file.read()

    # Menyiapkan permintaan untuk Speech-to-Text
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="su-ID",  # Bisa pakai bahasa Indonesia, jika pelafalan Sunda sulit
    )

    response = client.recognize(config=config, audio=audio)

    # Ambil hasil transkripsi
    transcribed_text = response.results[0].alternatives[0].transcript

    # Membandingkan teks transkripsi dengan teks yang benar
    similarity_score = compare_texts(transcribed_text, correct_text)
    
    return transcribed_text, similarity_score

def compare_texts(transcribed_text, correct_text):
    """
    Fungsi sederhana untuk menghitung seberapa mirip dua teks (misal, menggunakan Levenshtein Distance).
    """
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer
    
    # Menggunakan cosine similarity (ini bisa ditingkatkan lagi)
    vectorizer = CountVectorizer().fit_transform([transcribed_text, correct_text])
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    
    return similarity_matrix[0][0]
