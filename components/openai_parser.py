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

def parse_resumer(input):

    class Experience(BaseModel):
        """Modèle d'expérience"""

        Nom_de_la_societe: str = Field(..., description="décrire le nom de la société")
        Poste: str = Field(..., description="décrire le poste")
        date_de_debut: datetime = Field(..., description="décrire la date de début de l'expérience")
        date_de_fin: datetime = Field(..., description="décrire la date de fin de l'expérience")
        responsabilites: List[str] = Field(..., description="décrire la liste des responsabilités pendant l'expérience")


    class Candidat(BaseModel):
        """Modèle de candidat"""

        Nom_complet: str = Field(..., description="décrire le nom complet du candidat")
        Email: str = Field(..., description="décrire l'adresse e-mail du candidat")
        Numero_de_telephone: str = Field(..., description="décrire le numéro de téléphone du candidat")
        Localisation: str = Field(..., description="décrire la localisation du candidat")
        URL_Linkedin: str = Field(..., description="décrire l'URL Linkedin du candidat")
        Nom_de_l_universite: str = Field(..., description="décrire le nom de l'université du candidat")
        Niveau_d_etudes: str = Field(..., description="décrire le niveau d'études du candidat")
        Titre_professionnel: str = Field(..., description="décrire le titre professionnel du candidat")
        Experiences: List[Experience] = Field(..., description="Une liste de descriptions structurées de toutes les expériences professionnelles du candidat, à l'exclusion de son parcours académique et éducatif")
        Langages_de_programmation_technologies: List[str] = Field(...,description="décrire la liste des langages de programmation qui apparaissent dans les CV des candidats")
        

    model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([Candidat])

    prompt = ChatPromptTemplate.from_messages(
        [("system", "Vous êtes un assistant d'analyse de CV et un expert en extraction."), ("user", f"Analysez cette description de poste et extrayez les informations pertinentes : {input}. IMPORTANT: le resultat doit suivre une format JSON valide")]
    )

    parser = JsonOutputKeyToolsParser(key_name="Candidat")

    chain = prompt | model | parser

    return chain