import google.generativeai as genai

def generate_extraction(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.0))
    
    return response.text

def generate_nonsafety_settings(prompt):
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
    ]
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.0),
        safety_settings=safety_settings)
    return response.text