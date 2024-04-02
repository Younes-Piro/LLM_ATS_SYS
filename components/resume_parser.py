from components.gemini_generate import generate_nonsafety_settings

def resume_parser(cv_content):
    
    ## build prompt to answer every question based on the context
    prompt_template = """
        You are a CV analysis assistant and an extraction expert.
        Please analyze the following CV and extract the relevant information:

        {cv_content}

        The extracted information should be in JSON format with the following structure:

        {{
            "basic_information": {{
                "full_name": "",
                "email": "",
                "phone_number": "",
                "location": "",
                "linkedin_url": "",
                "university_name": "",
                "education_level": "",
                "professional_title": ""
            }},
            "professional_experiences": [
                {{
                    "position": "",
                    "company": "",
                    "duration": {{"start_date": "mm-YYYY", "end_date": "mm-YYYY"}},
                    "responsibilities": ""
                }}
            ],
            "skills": {{
                "programming_languages_technologies": ""
            }}
        }}

    NOTE : Please ensure all dates are in the format: mm-YYYY.
    """

    prompt_final = prompt_template.format(context=cv_content)

    response = generate_nonsafety_settings(prompt_final)

    return response