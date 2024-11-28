from langchain_community.document_loaders import PyPDFLoader
import os, sys, json
from flask import Flask, jsonify, request, render_template
from parse_resume import parse_resume

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
        response = parse_resume(data)
        
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
def _read_file_from_path(path):
    loader = PyPDFLoader(path)
    pdf_documents = loader.load()

    document_text = pdf_documents[0].page_content
    return document_text


if __name__ == "__main__":
    app.run(port=8000, debug=True)
