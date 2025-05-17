from pydantic import BaseModel
from typing import List

class Skill(BaseModel):
    skill: str
class JobPosition(BaseModel):
    title: str
    location: str
    description: str
    start_date: str
    end_date: str
    skills: List[Skill]

class Experience(BaseModel):
    job_positions: List[JobPosition]
    start_date: str
    end_date: str

class Education(BaseModel):
    school: str
    degree: str
    start_date: str
    end_date: str

class Language(BaseModel):
    language: str
    level: str


class TopVoice(BaseModel):
    name: str
    title: str
    followers: int

class Profile(BaseModel):
    name: str
    title: str
    location: str
    about: str
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    top_voices: List[TopVoice]
    languages: List[Language]