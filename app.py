from langchain_community.document_loaders import PyPDFLoader
import os, sys, json
from flask import Flask, jsonify, request, render_template
from extract_details import extract_details

sys.path.insert(0, os.path.abspath(os.getcwd()))

import logging

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/load_resume", methods=["POST"])
def load_resume():
    try:
        logging.debug(f"Request files: {request.files}")
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file uploaded or wrong format!"}), 400

        doc = request.files["file"]

        file_path = os.path.join('/tmp', doc.filename)
        doc.save(file_path)

        data = _read_file_from_path(file_path)
        resume_details = extract_details(data)
        job_offer_details = extract_details(request.form.get("job_offer_text"))
        
        if "error" in resume_details:
            return jsonify({"error": f"Resume parsing error: {resume_details['error']}"}), 500
        if "error" in job_offer_details:
            return jsonify({"error": f"Job offer parsing error: {job_offer_details['error']}"}), 500


        response = _compare_details(resume_details, job_offer_details)
        return jsonify({"response": response}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
 
def _read_file_from_path(path):
    loader = PyPDFLoader(path)
    pdf_documents = loader.load()

    document_text = pdf_documents[0].page_content
    return document_text


def _compare_details(resume_details, job_offer_details):
    """Compare resume details against job offer requirements."""
    missing = {"skills": [], "experiences": [], "tools": []}

    for key in missing.keys():
        if key in resume_details and key in job_offer_details:
            resume_items = set(resume_details[key])
            job_offer_items = set(job_offer_details[key])
            missing[key] = list(job_offer_items - resume_items)

    return missing


if __name__ == "__main__":
    app.run(port=8000, debug=True)
