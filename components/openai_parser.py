from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def parse_resume(input):

    class Experience(BaseModel):
        """Experience model """

        Company_name: str = Field(description="describe company name")
        Position: str = Field(description="describe position")
        start_date: datetime = Field(description="describe start date of experience")
        end_date: datetime = Field(description="describe end date of experience")
        responsibilities: List[str] = Field(description="describe list of responsibilities during the experience")


    class Candidate(BaseModel):
        """Candidate model """

        Fullname: str = Field(description="describe candidate full name")
        Email: str = Field(description="describe candidate email address")
        Phone_number: str = Field(description="describe candidate phones number")
        Location: str = Field(description="describe candidate location")
        Linkedin_url: str = Field(description="describe candidate linkedin url")
        University_name: str = Field(description="describe candidate university name")
        Education_level: str = Field(description="describe candidate education level")
        Professional_title: str = Field(description="describe candidate professional title")
        Experiences: List[Experience] = Field(description="describe list of experiences")
        

    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind_tools([Candidate])

    print(model.kwargs["tools"])

    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a CV analysis assistant and an extraction expert."), ("user", f"Analyse this post description suivante and extract the pertinant informations: {input}")]
    )

    parser = JsonOutputKeyToolsParser(key_name="Candidate", first_tool_only=True)

    chain = prompt | model | parser

    return chain