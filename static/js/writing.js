let jawaban = [];
let btnStack = []; // untuk menyimpan referensi tombol yang dipilih

function pilihKata(btn) {
  jawaban.push(btn.innerText);
  btn.disabled = true;
  document.getElementById('hasil').innerText = jawaban.join(' ');
}

function reset() {
  // Reset jawaban
  jawaban = [];

  // Aktifkan kembali tombol-tombol yang sudah dinonaktifkan
  const allBtns = document.querySelectorAll('#kata-random button');
  allBtns.forEach((btn) => (btn.disabled = false)); // Aktifkan semua tombol lagi

  updateHasil(); // Update hasil tampilan
}
function updateHasil() {
  document.getElementById('hasil').innerText = jawaban.join(' ');
}

function cekJawaban() {
  const questionId = parseInt(document.body.dataset.questionId);

  fetch('/api/writing/evaluate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_sentence: jawaban,
      question_id: questionId,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      const feedback = document.getElementById('feedback');
      if (data.is_correct) {
        feedback.textContent = '✅ Susunan kata Anda benar!';
        feedback.style.color = 'green';
      } else {
        feedback.textContent = '❌ Susunan kata Anda masih salah.';
        feedback.style.color = 'red';
      }
    });
}
