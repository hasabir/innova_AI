from flask import Flask, jsonify, request, render_template
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
import os, json, logging

app = Flask(__name__)

def extract_details(text, model="llama2"):
    """Extract details from a text using the LLM."""
    llm = OllamaLLM(model=model, temperature=0)

    system_message = SystemMessagePromptTemplate.from_template(
        """
        You are an AI bot designed to extract structured information. Parse the given text and extract:
        - Key skills
        - Experiences
        - Tools
        Output strictly in valid JSON format. Do not include any extra text or explanations.
        """
    )
    human_message = HumanMessagePromptTemplate.from_template("{input_text}")

    prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )

    result = chain.run({"input_text": text})

    # Extract valid JSON from the result
    try:
        start_idx = result.find("{")
        end_idx = result.rfind("}") + 1
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No JSON object found in LLM response.")
        
        json_str = result[start_idx:end_idx]
        extracted_data = json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        return {"error": f"Error parsing JSON: {str(e)}"}

    return extracted_data

def compare_details(resume_details, job_offer_details):
    """Compare resume details against job offer requirements."""
    missing = {"skills": [], "experiences": [], "tools": []}

    for key in missing.keys():
        if key in resume_details and key in job_offer_details:
            resume_items = set(resume_details[key])
            job_offer_items = set(job_offer_details[key])
            missing[key] = list(job_offer_items - resume_items)

    return missing

def _read_file_from_path(path):
    """Load text from a PDF file."""
    loader = PyPDFLoader(path)
    pdf_documents = loader.load()
    return pdf_documents[0].page_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def submit():
    """Process both the resume PDF and job offer text."""
    try:
        # Get the PDF file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No resume file uploaded or wrong format!"}), 400

        doc = request.files["file"]

        file_path = os.path.join('/tmp', doc.filename)
        doc.save(file_path)

        resume_text = _read_file_from_path(file_path)

        # Get the job offer text
        job_offer_text = request.form.get("job_offer_text", "")
        if not job_offer_text:
            return jsonify({"error": "Job offer text is required!"}), 400

        # Extract details from resume and job offer
        resume_details = extract_details(resume_text)
        job_offer_details = extract_details(job_offer_text)

        if "error" in resume_details:
            return jsonify({"error": f"Resume parsing error: {resume_details['error']}"}), 500
        if "error" in job_offer_details:
            return jsonify({"error": f"Job offer parsing error: {job_offer_details['error']}"}), 500

        # Compare the details
        missing_details = compare_details(resume_details, job_offer_details)

        return jsonify({
            "missing_details": missing_details,
            "resume_details": resume_details,
            "job_offer_details": job_offer_details
        }), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
