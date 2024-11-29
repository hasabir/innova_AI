from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import json

def extract_details(document_text):
    llm = OllamaLLM(model="llama2", temperature=0)

    system_message = SystemMessagePromptTemplate.from_template(
        """
        You are an AI bot designed to extract structured information. Parse the given text and extract:
        - Key skills
        - Experiences
        - Tools
        Output strictly in valid JSON format. Do not include any extra text or explanations.
        """
    )
    human_message = HumanMessagePromptTemplate.from_template("{resume_text}")

    prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )

    result = chain.run({"resume_text": document_text})

    print("Raw LLM Result:", result)

    try:
        start_idx = result.find("{")
        end_idx = result.rfind("}") + 1
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No JSON object found in LLM response.")
        
        json_str = result[start_idx:end_idx]
        result = json.loads(json_str)  # Parse the JSON
        
    except (json.JSONDecodeError, ValueError) as e:
        return {"error": f"Error parsing JSON: {str(e)}"}

    return result




# def parse_resume(document_text):
    
#     llm = OllamaLLM(model="llama2", temperature=0)

#     system_message = SystemMessagePromptTemplate.from_template(
#         """
#         You are an AI bot designed to parse resumes. Extract the following details:
#         1. full name
#         2. email id
#         3. github portfolio
#         4. linkedin id
#         5. employment details
#         6. technical skills
#         7. soft skills
#         Output strictly in valid JSON format. Do not include any extra text or explanations.
#         """
#     )
#     human_message = HumanMessagePromptTemplate.from_template("{resume_text}")

#     prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])

#     chain = LLMChain(
#         llm=llm,
#         prompt=prompt_template,
#         output_parser=StrOutputParser()
#     )

#     result = chain.run({"resume_text": document_text})

#     print("Raw LLM Result:", result)
#     if result.strip():
#         try:
#             cleaned_result = "\n".join(result.split("\n")[1:]).strip()
#             result = json.loads(cleaned_result)
#             # print("Parsed JSON Result:", parsed_result)
#         except json.JSONDecodeError as e:
#             return {"error": "Error parsing JSON: " + str(e)}
#     else:
#         return {"error": "No result received from the LLM."}

    return result
  
