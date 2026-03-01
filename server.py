from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid
import tempfile

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = tempfile.gettempdir()

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'VibeFetch backend is live ⚡'})

@app.route('/info', methods=['POST'])
def get_info():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            'title':     info.get('title', 'Unknown'),
            'thumbnail': info.get('thumbnail', ''),
            'duration':  info.get('duration_string', ''),
            'uploader':  info.get('uploader', ''),
            'view_count': info.get('view_count', 0),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    try:
        data    = request.json
        url     = data.get('url')
        quality = data.get('quality', '720')
        fmt     = data.get('format', 'video')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        filename = str(uuid.uuid4())
        out_tmpl = os.path.join(DOWNLOAD_DIR, filename + '.%(ext)s')

        if fmt == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_tmpl,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'quiet': True,
            }
            ext = 'mp3'
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best[height<={quality}]',
                'outtmpl': out_tmpl,
                'merge_output_format': 'mp4',
                'postprocessor_args': [
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-b:a', '192k'
                ],
                'quiet': True,
            }
            ext = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info      = ydl.extract_info(url, download=True)
            safe_name = ydl.prepare_filename(info)

        # Find the actual output file (extension may differ)
        base = os.path.join(DOWNLOAD_DIR, filename)
        final_path = base + '.' + ext
        if not os.path.exists(final_path):
            for f in os.listdir(DOWNLOAD_DIR):
                if f.startswith(filename):
                    final_path = os.path.join(DOWNLOAD_DIR, f)
                    break

        safe_title = info.get('title', 'vibefetch').replace('/', '-').replace('\\', '-')[:50]
        download_name = f"{safe_title}.{ext}"

        return send_file(
            final_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='audio/mpeg' if ext == 'mp3' else 'video/mp4'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
