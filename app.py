from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
os.makedirs('./downloads', exist_ok=True)

@app.route('/')
def home():
    return 'ytbackend is running!'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': './downloads/%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return jsonify({'message': 'Download successful', 'file': filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
