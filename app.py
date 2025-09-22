from flask import Flask, render_template, request, jsonify, send_file
import os, uuid
import pandas as pd
from extractor import extract_kemenku_strong

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada file diupload"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "Nama file kosong"}), 400

    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    excel_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.xlsx")

    file.save(pdf_path)

    return jsonify({"status": "success", "message": "File berhasil diupload!", "file_id": file_id})

@app.route("/extract/<file_id>", methods=["POST"])
def extract_data(file_id):
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    excel_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.xlsx")

    if not os.path.exists(pdf_path):
        return jsonify({"status": "error", "message": "File PDF tidak ditemukan."}), 404

    try:
        df = extract_kemenku_strong(pdf_path, excel_path)

        stats = {
            "totalRows": len(df),
            "totalSchools": int(df["Sekolah"].nunique()),
            "totalMajors": int(df["Jurusan"].nunique()),
            "totalPages": df["No"].nunique() if "No" in df.columns else len(df)
        }

        preview = df.head(10).to_dict(orient="records")

        return jsonify({
            "status": "success",
            "file_id": file_id,
            "stats": stats,
            "preview": preview
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/download/<file_id>")
def download(file_id):
    excel_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.xlsx")
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    return jsonify({"status": "error", "message": "File tidak ditemukan"}), 404

if __name__ == "__main__":
    app.run(debug=True)
