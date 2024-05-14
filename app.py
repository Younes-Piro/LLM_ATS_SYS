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
result = chain.invoke({"input": cv_context})

# Specify the file path
file_path = "output_piro.txt"

# Open the file in write mode ('w')
with open(file_path, 'w') as file:
    file.write(str(result))

print("Result has been saved to", file_path)