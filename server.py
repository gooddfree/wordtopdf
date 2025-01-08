
from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CONVERT_FOLDER = 'converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_file():
    file = request.files.get('file')
    output_format = request.form.get('format')

    if not file or not output_format:
        return "Missing file or format", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(CONVERT_FOLDER, f"output.{output_format}")

    file.save(input_path)

    # Using LibreOffice for conversion
    command = [
        "libreoffice",
        "--headless",
        "--convert-to", output_format,
        "--outdir", CONVERT_FOLDER,
        input_path
    ]

    try:
        subprocess.run(command, check=True)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
    finally:
        # Clean up
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True)
