<<<<<<< HEAD
const correctPhonetic = 'ka'; // contoh: fonetik dari aksara "ᮊ"
const hasilEl = document.getElementById('hasil');
const feedbackEl = document.getElementById('feedback');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'id-ID'; // masih pakai id-ID karena tidak ada 'su-ID'
recognition.continuous = false;
recognition.interimResults = false;

function mulaiRekam() {
  hasilEl.textContent = '...ngadengekeun';
  feedbackEl.textContent = '';
  recognition.start();
}

recognition.onresult = function (event) {
  const hasil = event.results[0][0].transcript.trim().toLowerCase();
  hasilEl.textContent = hasil;

  if (normalize(hasil) === correctPhonetic) {
    feedbackEl.textContent = '✅ Leres!';
    feedbackEl.style.color = 'green';
  } else {
    feedbackEl.textContent = '❌ Henteu luyu. Coba deui.';
    feedbackEl.style.color = 'red';
  }
};

recognition.onerror = function (event) {
  feedbackEl.textContent = `🎤 Error: ${event.error}`;
  feedbackEl.style.color = 'red';
};

// Fungsi normalisasi untuk adaptasi fonetik
function normalize(input) {
  return input
    .normalize('NFD') // hilangkan aksen jika ada
    .replace(/[^a-z]/g, '') // hilangkan karakter non-huruf
    .replace(/kha/g, 'ka') // contoh jika ucapan cenderung salah
    .replace(/ha$/, 'a') // akhir 'ha' dianggap 'a'
    .trim();
}

window.mulaiRekam = mulaiRekam;
=======
let mediaRecorder;
let audioChunks = [];

function playTTS() {
  const sentence = document.getElementById('sentence').textContent;
  const utterance = new SpeechSynthesisUtterance(sentence);
  utterance.lang = 'su-ID'; // atau "id-ID" jika tidak tersedia bahasa Sunda
  speechSynthesis.speak(utterance);
}

function startRecording() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob);

        // Kirim ke backend (jika ada endpoint evaluasi audio)
        fetch('/api/reading/evaluate', {
          method: 'POST',
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            document.getElementById('feedback').innerText = 'Skor Pelafalan: ' + Math.round(data.score * 100) + '%';
          })
          .catch((err) => {
            console.error('Error evaluating speech:', err);
            document.getElementById('feedback').innerText = 'Gagal mengevaluasi pelafalan.';
          });
      };

      mediaRecorder.start();
      setTimeout(() => {
        mediaRecorder.stop();
      }, 3000); // Rekam 3 detik
    })
    .catch((err) => {
      console.error('Mic error:', err);
      alert('Gagal mengakses mikrofon.');
    });
}

function submitRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}
>>>>>>> f27c5e6accb667ea705e33dcd8a2a82ba6bd3f9c
