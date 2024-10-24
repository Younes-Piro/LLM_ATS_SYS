from components.gemini_json_formater import json_formater
from components.openai_parser import parse_resumer
from components.parse_job_description import parse_job
from utils.helpers import extract_json, format_resume, format_job
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI



def matching(resume, JD):

    # Define your prompt template
    template = """
    You are an IT job matching assistant. Your task is to evaluate the match between a job description and a candidate's resume in the IT field. 
    Consider the following criteria:
    1. Total months of relevant experience based on the skills and roles listed in both the job description and the resume.
    2. The alignment of the candidate's profile type with the profile needed in the job description, for higher score the candidate should have the same profile type as needed in the job description as example software engineer will have low score for data scientist in the job description

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
    - Justification:
    {{
        'Matching Score': X/100,
        'Relevant Experience': [summary],
        'Profile Type Match': [summary],
        'Final Recommendation': [Fit/Not Fit] 
    }}

    IMPORTANT : The output needs to follow a json format
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