from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
from pdfminer.layout import LAParams
from datetime import datetime
import json
from dateutil import parser

# function to read the pdf
def read_pdf_path(cv_path):
    # load cv file
    i_f = open(cv_path,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)
 
    txt = retData.getvalue()
    return txt

def fix_json(json_str):
    try:
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError as e:
        error_position = e.pos
        # Check if the error position is within the string length

        if error_position < len(json_str):
            # Remove the character at the error position
            json_str = json_str[: (error_position-2)] + json_str[error_position:]
            return json_str
        else:
            return json_str

def extract_json(input_string):
    # Find the start and end indices of the JSON string
    start_index = input_string.find("```json") + len("```json")
    end_index = input_string.find("\n```", start_index)

    # Extract the JSON string
    json_string = input_string[start_index:end_index]

    return json_string

# convert experiences duration to specific format
def convert_to_standard_format(date_str):
    # Try to parse the date using dateutil.parser
    try:
        parsed_date = parser.parse(date_str)
    except ValueError:
        return None

    # Format the parsed date into 'YYYY-MM' format
    formatted_date = datetime.strftime(parsed_date, "%Y-%m")
    return formatted_date

def extract_experience_duration(experiences):
    # Initialize a set to store unique date pairs
    unique_dates = set()

    # Iterate through each experience in the provided list
    for exp in experiences:
        if not any(keyword in exp["Poste"].lower() for keyword in ["internship", "intern", "stage", "pfe", "stagiaire"]):
            # Use the convert_to_standard_format function for start_date
            start_date_str = convert_to_standard_format(exp['date_de_debut'])

            # Use the end_date from the experience if it contains any string, otherwise use datetime.now()
            end_date_str = convert_to_standard_format(exp['date_de_fin']) if exp['date_de_fin'] else None
            end_date_str = end_date_str or datetime.now().strftime("%Y-%m")
            
            # Create a tuple representing the unique date pair
            date_pair = (start_date_str, end_date_str)

            # Add the date pair to the set, ensuring uniqueness
            unique_dates.add(date_pair)

    # Calculate the total duration in months
    total_duration = sum(months_difference(start_date, end_date) for start_date, end_date in unique_dates)

    # Ensure that the total duration is non-negative, otherwise return 0
    if total_duration > 0:
        return total_duration
    else:
        return 0

def months_difference(start_date_str, end_date_str):
    # Parse the date strings into datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m")
    end_date = datetime.strptime(end_date_str, "%Y-%m")

    # Calculate the difference in months
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month


# extract all responsibilites from different experiences
def all_responsibilies(experiences):
    all_resp = []
    for exp in experiences:
        if not any(keyword in exp["Poste"].lower() for keyword in ["internship", "intern", "stage", "pfe", "stagiaire"]):
            if isinstance(exp['responsabilites'], list):
                all_resp.extend(exp['responsabilites'])
            else:
                all_resp.extend([exp['responsabilites']])
    return all_resp   

def format_resume(cv_parsed):
  data = {}

  #basic information

  basic_infos = set(cv_parsed.keys()) - set('Experiences Langages_de_programmation_technologies'.split())

  for basic in basic_infos:
    data[f'{basic}'] = cv_parsed[f'{basic}']

  # numero mois d'experience
  data['months_experiences'] = extract_experience_duration(cv_parsed['Experiences'])

  # responsibilites
  data['responsibilities'] = all_responsibilies(cv_parsed['Experiences'])

  #Skills 
  # Check the type of the value under 'skills'
  if isinstance(cv_parsed['Langages_de_programmation_technologies'], list):
    # If it's a list, return the values directly under 'skills'
    values = cv_parsed['Langages_de_programmation_technologies']
  else:
    # If it's a dictionary, assume one key and return its values
    values = list(cv_parsed['Langages_de_programmation_technologies'].values())[0]

  data['Programming_languages'] = values

  return data

def experience_needed(experience_str):
    experience_str = str(experience_str)
    if ' ' in experience_str.strip():
        return experience_str.split()[0]
    else:
        return experience_str

def format_job(job_parsed):
    data = {}

    data['post'] = job_parsed['information_post']['intitule_poste']

    data['months_experiences']   = int(experience_needed(job_parsed['information_post']['année_experience'])) * 12

    for skill in job_parsed['Skills'].keys():
        data[f'{skill}'] = job_parsed['Skills'][f'{skill}']
    return data

def clean_json_string(raw_json_string):
    # Remove backticks from the JSON string
    cleaned_json_string = raw_json_string.replace('`', '')

    # Find the index where 'json' occurs
    start_index = cleaned_json_string.find('{')

    # Extract the JSON part
    json_string = cleaned_json_string[start_index:]

    try:
        # Attempt to load the cleaned JSON string
        json_data = json.loads(json_string)
        
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None