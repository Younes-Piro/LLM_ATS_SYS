from components.gemini_json_formater import json_formater
from utils.helpers import read_pdf_path, format_resume, extract_json
import os
from dotenv import load_dotenv
from components.openai_parser import parse_resume
import json

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

cv_path = './data/cv_3.pdf'

cv_context = read_pdf_path(cv_path)
chain = parse_resume(cv_context)
result = chain.invoke({"input": cv_context})
result_json = json_formater(result)
# Extract JSON from the string
json_string = extract_json(result_json.strip())

# Parse the extracted JSON
try:
    json_data = json.loads(json_string)
    data = format_resume(json_data[0])
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)


print(data)