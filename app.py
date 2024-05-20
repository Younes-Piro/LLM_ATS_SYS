from utils.helpers import read_pdf_path
import os
from dotenv import load_dotenv
from pipeline.matching_pipeline import Matching_pipeline

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

cv_path = './data/cv_3.pdf'

## parse resume
cv_context = read_pdf_path(cv_path)

# initialize pipeline and parse resume
MP = Matching_pipeline()
MP.parse_resume(cv_context)
resume_parsed = MP.data_resume
print(resume_parsed)