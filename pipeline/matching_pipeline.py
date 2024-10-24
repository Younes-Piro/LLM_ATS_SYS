from components.gemini_json_formater import json_formater
from components.openai_parser import parse_resumer
from components.parse_job_description import parse_job
from components.matching import matching
from utils.helpers import extract_json, format_resume, format_job
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI

class Matching_pipeline:
    def __init__(self):
        self.data_resume = None
        self.data_job = None

    def parse_resume(self, cv_context):
        chain = parse_resumer(cv_context)
        result = chain.invoke({"input": cv_context})
        result_json = json_formater(result)
        # Extract JSON from the string
        json_string = extract_json(result_json.strip())
        # Parse the extracted JSON
        try:
            json_data = json.loads(json_string)
            self.data_resume = format_resume(json_data[0])
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            self.data_resume
            
    def parse_job(self, job_context):
        chain = parse_job(job_context)
        result = chain.invoke({"input": job_context})
        result_json = json_formater(result)
        # Extract JSON from the string
        json_string = extract_json(result_json.strip())
        # Parse the extracted JSON
        try:
            json_data = json.loads(json_string)
            print("ana hna ")
            self.data_job = format_job(json_data[0])
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            self.data_job


    def matching_profiles(self, resume, JD):
       
        result = matching(resume, JD)

        return result