from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'  # Update with the correct path to ffmpeg
FFPROBE_PATH = 'C:/ffmpeg/bin/ffprobe.exe'  # Update with the correct path to ffprobe

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'video' not in request.files:
        return "No video file part", 400
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Get the compression level from the form
        compression_level = int(request.form['compression'])
        
        # Calculate the target size in bytes
        original_size = os.path.getsize(filepath)
        target_size = original_size * (compression_level / 100.0)
        
        # Estimate the duration of the video using ffprobe
        probe = subprocess.run([
            FFPROBE_PATH, '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', filepath
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
        
        # Calculate the target bitrate (in bits per second)
        target_bitrate = (target_size * 8) / duration
        
        # Convert the target bitrate to kilobits per second (kbps)
        target_bitrate_kbps = target_bitrate / 1000
        
        # Define the output file path
        compressed_filename = f"compressed_{compression_level}_{filename}"
        compressed_filepath = os.path.join(COMPRESSED_FOLDER, compressed_filename)
        
        # Compress the video using ffmpeg with the calculated target bitrate
        subprocess.run([
            FFMPEG_PATH, '-i', filepath, '-b:v', f'{target_bitrate_kbps}k', '-y', compressed_filepath
        ], check=True)
        
        return send_file(compressed_filepath, as_attachment=True, download_name=compressed_filename)

if __name__ == '__main__':
    app.run(debug=True)
