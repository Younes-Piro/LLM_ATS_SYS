from components.resume_parser import resume_parser
from utils.helpers import read_pdf_path, format_resume, extract_json
import os
from dotenv import load_dotenv
from components.openai_parser import parse_resume
import json
from components.gemini_generate import generate_nonsafety_settings


load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

cv_path = './data/cv_2.pdf'

cv_context = read_pdf_path(cv_path)
chain = parse_resume(cv_context)
result = chain.invoke({"input": cv_context})

template = f"I'm working on a project that involves parsing JSON responses. Sometimes, the JSON produced by my code contains errors or issues. I'd like assistance in fixing any issues that may arise. \
    Below is an example of JSON data that I've encountered:\
    INPUT: {result} \
    Could you please review this JSON and solve any errors or issues that you find?\
    IMPORT: RETURN ONLY THE JSON"

response = generate_nonsafety_settings(template)


# Extract JSON from the string
json_string = extract_json(response.strip())

# Parse the extracted JSON
try:
    json_data = json.loads(json_string)
    data = format_resume(json_data[0])
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)


print(data)