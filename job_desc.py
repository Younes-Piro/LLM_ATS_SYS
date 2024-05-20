from utils.helpers import read_pdf_path
from components.parse_job_description import parse_job

description_path = './data/description.pdf'

job_descr_context = read_pdf_path(description_path)

job_parsed = parse_job(job_descr_context)

print(job_parsed)