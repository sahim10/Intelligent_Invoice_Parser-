import os
import uuid
import json
from datetime import datetime
from flask import Flask, render_template, request, send_file
from src.extract_text import extract_text_from_pdf
from src.parse_fields import parse_fields
from src.validate_fields import clean_with_llm

app = Flask(__name__)
UPLOAD_FOLDER = "invoices"
OUTPUT_FOLDER = "outputs"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("invoice")

        if file and file.filename.endswith(".pdf"):
            # Save uploaded PDF with unique name
            filename = f"{uuid.uuid4().hex}.pdf"
            saved_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(saved_path)

            # Log input metadata to all_inputs.json
            upload_log = {
                "filename": filename,
                "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "original_name": file.filename
            }

            input_log_path = os.path.join(OUTPUT_FOLDER, "all_inputs.json")
            if os.path.exists(input_log_path):
                with open(input_log_path, "r") as f:
                    input_logs = json.load(f)
            else:
                input_logs = []

            input_logs.append(upload_log)
            with open(input_log_path, "w") as f:
                json.dump(input_logs, f, indent=4)

            # Extract and parse invoice
            text = extract_text_from_pdf(saved_path)
            data = parse_fields(text)

            # Clean fields using HuggingFace
            for key in data:
                if key != "line_items":
                    data[key] = clean_with_llm(key, data[key])

            # Save to all_invoices.json
            output_path = os.path.join(OUTPUT_FOLDER, "all_invoices.json")
            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    all_data = json.load(f)
            else:
                all_data = []

            all_data.append(data)
            with open(output_path, "w") as f:
                json.dump(all_data, f, indent=4)

            return render_template("index.html", data=data, json_filename="all_invoices.json")

    return render_template("index.html")

@app.route("/download/<json_filename>")
def download(json_filename):
    json_path = os.path.join(OUTPUT_FOLDER, json_filename)
    return send_file(json_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
