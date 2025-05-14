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
