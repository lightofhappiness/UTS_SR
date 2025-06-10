from gtts import gTTS
import os
import uuid

def generate_tts(text):
    try:
        tts = gTTS(text=text, lang='su')  # 'su' = Bahasa Sunda (jika didukung)
        filename = f"tts_{uuid.uuid4()}.mp3"
        filepath = os.path.join("tmp", filename)

        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None
