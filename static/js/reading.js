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
