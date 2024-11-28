import spacy
from spacy.matcher import Matcher
import pandas as pd

nlp = spacy.load("en_core_web_md")

job_ad_text = """
We are seeking a passionate Software Engineer to join our team at TechCorp. 
Location: New York, NY
Responsibilities include designing, developing, and maintaining web applications.
Required Skills: Proficiency in Python, JavaScript, React, and Docker.
Experience: 3+ years in software development.
"""

doc = nlp(job_ad_text)

parsed_result = {
    "Job Title": None,
    "Company Name": None,
    "Location": None,
    "Required Skills": None,
    "Experience": None,
    "Job Description": None,
}

for ent in doc.ents:
    print(ent.text, ent.label_)    
# if ent.label_ == "ORG":  
#         parsed_result["Company Name"] = ent.text
#     elif ent.label_ == "GPE":  
#         parsed_result["Location"] = ent.text
        
# print(parsed_result)

# # Use spaCy's matcher for job title (custom pattern)
# matcher = Matcher(nlp.vocab)
# job_title_pattern = [{"LOWER": "software"}, {"LOWER": "engineer"}]
# matcher.add("JobTitle", [job_title_pattern])
# matches = matcher(doc)
# if matches:
#     for match_id, start, end in matches:
#         parsed_result["Job Title"] = doc[start:end].text

# # Extract required skills and experience with simple keyword matching
# for sent in doc.sents:
#     if "Required Skills" in sent.text:
#         parsed_result["Required Skills"] = sent.text.split(":")[1].strip()
#     elif "Experience" in sent.text:
#         parsed_result["Experience"] = sent.text.split(":")[1].strip()
#     elif "Responsibilities" in sent.text:
#         parsed_result["Job Description"] = sent.text.split("include")[1].strip()

# # Convert to DataFrame
# df = pd.DataFrame([parsed_result])
# print(df)
