import openai

def parse_job(description_de_poste, openai_api_key, max_tokens=1000):

    openai.api_key = openai_api_key

    # Définissez la conversation avec la description de poste comme variable
    conversation = [
        {"role": "system", "content": "Vous êtes un analyseur de descriptions de poste."},
        {"role": "user", "content": f"Analysez la description de poste suivante et extrayez les informations pertinentes :\n\n{description_de_poste}"},
        {"role": "assistant", "content": "Informations extraites en JSON avec exactement la structure suivante : {information_post : {intitule_poste, année_experience}, Skills : {Programming_languages, responsibilities, theorical_skills}}" }

    ]

    # Effectuez l'appel à l'API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=max_tokens
    )

    # Extrayez la réponse de l'assistant
    assistant_reply = response['choices'][0]['message']['content']

    #return the result
    return assistant_reply