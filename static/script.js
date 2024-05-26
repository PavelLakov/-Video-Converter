document.addEventListener('DOMContentLoaded', () => {
    const videoInput = document.getElementById('videoInput');
    const compressionSlider = document.getElementById('compressionSlider');
    const compressionValue = document.getElementById('compressionValue');
    const compressButton = document.getElementById('compressButton');
    const outputMessage = document.getElementById('outputMessage');

    compressionSlider.addEventListener('input', () => {
        compressionValue.textContent = `${compressionSlider.value}%`;
    });

    compressButton.addEventListener('click', () => {
        const file = videoInput.files[0];
        const compressionLevel = compressionSlider.value;

        if (file) {
            const formData = new FormData();
            formData.append('video', file);
            formData.append('compression', compressionLevel);

            fetch('/compress', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `compressed_${compressionLevel}_${file.name}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                outputMessage.textContent = `Video compressed to ${compressionLevel}% of its original size successfully!`;
            })
            .catch(error => {
                console.error('Error:', error);
                outputMessage.textContent = 'An error occurred during compression.';
            });
        } else {
            alert('Please select a video file first.');
        }
    });
});
