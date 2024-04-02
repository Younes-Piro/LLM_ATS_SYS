from components.resume_parser import resume_parser
from utils.helpers import read_pdf_path, format_resume, clean_json_string

cv_path = './data/cv.pdf'

cv_context = read_pdf_path(cv_path)
response = resume_parser(cv_context)
response_json = clean_json_string(response)
resume_formated = format_resume(response_json)
print(resume_formated)