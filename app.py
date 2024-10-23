from utils.helpers import read_pdf_path
import os
from dotenv import load_dotenv
from pipeline.matching_pipeline import Matching_pipeline
import warnings
import json

warnings.filterwarnings("ignore")
load_dotenv()

# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

cv_path = './data/cv_3.pdf'
job_desc_path = './data/description.pdf'

## parse resume
cv_context = read_pdf_path(cv_path)

# parse job description
job_desc = read_pdf_path(job_desc_path)

# initialize pipeline  
MP = Matching_pipeline()

# parse resume 
MP.parse_resume(cv_context)
resume_parsed = MP.data_resume

# job description parsed
MP.parse_job(job_desc)
job_parsed = MP.data_job

print(f"Resume :  {resume_parsed}")

print('--------------------------------' * 30)

print(f"Job description : {job_parsed}")

print('--------------------------------' * 30)

print('begin matching : \n'  )
print(MP.matching(resume_parsed, job_parsed))