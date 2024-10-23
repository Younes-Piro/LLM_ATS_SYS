from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field  # Import direct depuis Pydantic v2
from typing import List
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def parse_job(input):

    class Skill(BaseModel):
        Programming_languages: str = Field(..., description="decrit les Programming languages disponible")
        Responsibilities: str = Field(..., description="decrit les Responsibilities disponible")
        Theorical_skills: str = Field(..., description="decrit les theorical skills disponible")


    class JD(BaseModel):
        """Modèle du job Description"""

        intitule_poste: str = Field(..., description="décrire l'intitule du poste")
        année_experience: str = Field(..., description="décrire les années d'experience dans la description") 
        Skills: List[Skill] = Field(..., description="Une liste de descriptions structurées de toutes les expériences professionnelles du candidat, à l'exclusion de son parcours académique et éducatif")
        Langages_de_programmation_technologies: List[str] = Field(...,description="décrire la liste des langages de programmation qui apparaissent dans les CV des candidats")
        

    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind_tools([JD])

    prompt = ChatPromptTemplate.from_messages(
        [("system", "Vous êtes un assistant d'analyse des job description et un expert en extraction."), ("user", f"Analysez cette description de poste et extrayez les informations pertinentes : {input}. IMPORTANT: le resultat doit suivre une format JSON valide")]
    )

    parser = JsonOutputKeyToolsParser(key_name="JD")

    chain = prompt | model | parser

    return chain