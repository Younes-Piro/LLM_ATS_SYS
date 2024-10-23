from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
import os
import json



# Sample resume data (as a Python dictionary)
resume = {
    "Nom_complet": "Younes M’khantar",
    "Nom_de_l_universite": "Institut National des Postes et Télécommunications (INPT), Rabat",
    "Titre_professionnel": "Développement informatique",
    "Niveau_d_etudes": "Ingénieur en télécom technologies d’information",
    "Email": "Mkhantar.youness@gmail.com",
    "Localisation": "Casablanca, Maroc",
    "Numero_de_telephone": "+212 760 47 22 02",
    "last_entreprise": "KBM Consulting",
    "months_experiences": 69,
    "responsibilities": [
        "Conception de la solution",
        "Architecture et développement",
        "Réaliser les tests d’intégration et les tests unitaires",
        "Elaboration du plan de tests recette"
    ],
    "Programming_languages": [
        "ANGULAR", "JAVA", "Spring boot", "HTML/CSS", "JavaScript", "Jest", "JUnit",
        "Bootstrap", "SQL Server", "SSIS", "SSRS", "PostgreSQL", "Git", "NodeJS",
        "MySQL", "JQuery", "MongoDB", "TypeScript", "Oracle"
    ]
}

# Sample job description data (as a Python dictionary)
job_description = {
    "post": "Data Scientist",
    "months_experiences": 36,
    "Programming_languages": "Python, R, Spark, Scala",
    "Responsibilities": (
        "Récupération et analyse des données pertinentes, Conception et implémentation de modèles "
        "prédictifs, Restitution des résultats de manière lisible, Analyse des résultats pour l’élaboration "
        "de recommandations business, Contribution à la transformation culturelle de l’Intelligence Artificielle"
    ),
    "Theorical_skills": (
        "Maîtrise des algorithmes de machine Learning, Connaissances approfondies en optimisation convexe et en statistiques, "
        "Maîtrise des principales librairies de machine Learning, Connaissance de l’environnement Hadoop et de ses différentes "
        "composantes, Compétences en systèmes d’informations"
    )
}

# Define your prompt template
template = """
You are a job matching assistant. Your task is to evaluate the match between a job description and a candidate's resume. 
Consider the following criteria:
1. Total months of relevant experience based on the skills and roles listed in both the job description and the resume.
2. The alignment of the candidate's profile type (e.g., software engineer, data scientist, designer) with the profile needed in the job description.

### Job Description:
{job_description}

### Resume:
{resume}

### Instructions:
1. Extract key skills, job roles, and months of experience from both the job description and resume.
2. Calculate the total months of experience the candidate has in relevant skills and roles as per the job description.
3. Compare the candidate’s profile type with the job's desired profile type (e.g., developer vs. manager).
4. Based on the relevance of experience (months) and profile type alignment, provide a matching score from 0 to 100.
5. Justify your score by explaining:
   - How many months of experience the candidate has for the required skills.
   - How closely the candidate's profile type aligns with the job description's desired profile.
6. Provide a final recommendation for whether the candidate is a good fit for the role.

### Output:
- Matching Score: X/100
- Justification:
- Relevant Experience: [summary]
- Profile Type Match: [summary]
- Final Recommendation: [Fit/Not Fit]
"""





# Create the PromptTemplate instance
prompt_template = PromptTemplate(
    input_variables=["job_description", "resume"],
    template=template
)

# Initialize OpenAI properly with model_name and key
llm = OpenAI()

# Create the LLMChain using the PromptTemplate and OpenAI model
chain = prompt_template | llm
result = chain.invoke(
    {
        "job_description": str(json.dumps(job_description)),
        "resume": str(json.dumps(resume))
    }
)

print(result)

