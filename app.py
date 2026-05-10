from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os
from main import download_audio

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

INDEX_HTML = '''
<!doctype html>
<title>Extract YouTube Audio</title>
<h1>Extract YouTube Audio (mp3)</h1>
<form method=post>
  <label for=url>Video URL</label>
  <input id=url name=url size=80 placeholder="https://www.youtube.com/watch?v=...">
  <input type=submit value=Download>
</form>
{% if error %}
  <p style="color:red">{{ error }}</p>
{% endif %}
{% if file_url %}
  <p>Download ready: <a href="{{ file_url }}">{{ file_name }}</a></p>
{% endif %}
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    file_url = None
    file_name = None
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            error = 'Vui lòng nhập URL.'
        else:
            result = download_audio(url, output_dir=DOWNLOAD_DIR)
            if result:
                file_name = os.path.basename(result)
                file_url = url_for('download_file', filename=file_name)
            else:
                error = 'Có lỗi khi tải file. Kiểm tra console để biết chi tiết.'
    return render_template_string(INDEX_HTML, error=error, file_url=file_url, file_name=file_name)


@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=True)
