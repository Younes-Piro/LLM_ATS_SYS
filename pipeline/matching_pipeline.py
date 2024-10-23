from components.gemini_json_formater import json_formater
from components.openai_parser import parse_resumer
from components.parse_job_description import parse_job
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


    def matching(self, resume, JD):
        
        # Define your prompt template
        template = """
        You are a job matching assistant. Your task is to evaluate the match between a job description and a candidate's resume. 
        Consider the following criteria:
        1. Total months of relevant experience based on the skills and roles listed in both the job description and the resume.
        2. The alignment of the candidate's profile type (e.g., software engineer, data scientist, designer) with the profile needed in the job description.

        ### Job Description:
        {job_description}

        ### Resume:
        {resume}

        ### Instructions:
        1. Extract key skills, job roles, and months of experience from both the job description and resume.
        2. Calculate the total months of experience the candidate has in relevant skills and roles as per the job description.
        3. Compare the candidate’s profile type with the job's desired profile type (e.g., developer vs. manager).
        4. Based on the relevance of experience (months) and profile type alignment, provide a matching score from 0 to 100.
        5. Justify your score by explaining:
        - How many months of experience the candidate has for the required skills.
        - How closely the candidate's profile type aligns with the job description's desired profile.
        6. Provide a final recommendation for whether the candidate is a good fit for the role.

        ### Output:
        - Matching Score: X/100
        - Justification:
        - Relevant Experience: [summary]
        - Profile Type Match: [summary]
        - Final Recommendation: [Fit/Not Fit]
        """





        # Create the PromptTemplate instance
        prompt_template = PromptTemplate(
            input_variables=["job_description", "resume"],
            template=template
        )

        # Initialize OpenAI properly with model_name and key
        llm = OpenAI()

        # Create the LLMChain using the PromptTemplate and OpenAI model
        chain = prompt_template | llm
        result = chain.invoke(
            {
                "job_description": str(json.dumps(JD)),
                "resume": str(json.dumps(resume))
            }
        )

        # Output the result
        return result