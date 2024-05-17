from components.gemini_generate import generate_nonsafety_settings

def json_formater(result):
    
    prompt_template = """I'm working on a project that involves parsing JSON responses. Sometimes, the JSON produced by my code contains errors or issues. I'd like assistance in fixing any issues that may arise. \
    Below is an example of JSON data that I've encountered:\
    INPUT: {input_json} \
    Could you please review this JSON and solve any errors or issues that you find?\
    IMPORT: RETURN ONLY THE JSON"""

    prompt_final = prompt_template.format(input_json=result)

    response = generate_nonsafety_settings(prompt_final)

    return response