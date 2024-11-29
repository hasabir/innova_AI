from langchain_community.document_loaders import PyPDFLoader
import os, sys, json
from flask import Flask, jsonify, request, render_template
from extract_details import extract_details, compare_details
from flask_cors import CORS
import tempfile

sys.path.insert(0, os.path.abspath(os.getcwd()))

import logging



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def submit():
    
    
    try:
        logging.debug(f"Request files: {request.files}")
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file uploaded or wrong format!"}), 400

        doc = request.files["file"]
        
        job_offer_text = request.form.get("job_offer_text")
        if not job_offer_text:
            return jsonify({"error": "Job offer text is missing!"}), 400


        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            doc.save(temp_file.name)
            file_path = temp_file.name

        data = _read_file_from_path(file_path)
        resume_details = extract_details(data)
        job_offer_details = extract_details(job_offer_text)
        
        if "error" in resume_details:
            return jsonify({"error": f"Resume parsing error: {resume_details['error']}"}), 500
        if "error" in job_offer_details:
            return jsonify({"error": f"Job offer parsing error: {job_offer_details['error']}"}), 500


        response = compare_details(resume_details, job_offer_details)
        return jsonify({"response": response}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
 
def _read_file_from_path(path):
    try:
        loader = PyPDFLoader(path)
        pdf_documents = loader.load()
        print(pdf_documents)
        if not pdf_documents:
            raise ValueError("No text found in the PDF.")
        return pdf_documents[0].page_content
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")



# def _compare_details(resume_details, job_offer_details):
#     missing = {"skills": [], "experiences": [], "tools": []}
#     for key in missing.keys():
#         resume_items = set(resume_details.get(key, []))
#         job_offer_items = set(job_offer_details.get(key, []))
#         missing[key] = list(job_offer_items - resume_items)
#     return missing









if __name__ == "__main__":

    app.run(port=8000, debug=True)
    CORS(app)



# eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnaXRodWJ8OTYyODQxODEiLCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyIsImlzcyI6ImFwaV9rZXlfaXNzdWVyIiwiYXVkIjpbImh0dHBzOi8vbmViaXVzLWluZmVyZW5jZS5ldS5hdXRoMC5jb20vYXBpL3YyLyJdLCJleHAiOjE4OTA1NzQ3ODcsInV1aWQiOiI0NmE5MGIwNy1kZDAwLTRhNjItOTUxZi01NDliMGNlZjFhZGIiLCJuYW1lIjoiaWEiLCJleHBpcmVzX2F0IjoiMjAyOS0xMS0yOFQxNTozOTo0NyswMDAwIn0.M3vwUJ9bieDbGl1-u64tuURSQCmKp0KnKC9vmXtPcrw