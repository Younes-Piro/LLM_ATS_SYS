from components.resume_parser import resume_parser
from utils.helpers import read_pdf_path, format_resume, clean_json_string
import os
from dotenv import load_dotenv
from components.openai_parser import parse_resume

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


cv_path = './data/cv.pdf'

cv_context = read_pdf_path(cv_path)
chain = parse_resume(cv_context)
print(chain.invoke({"input": cv_context}))