from pydantic import BaseModel
from typing import List



class JobPosition(BaseModel):
    title: str
    location: str
    description: str
    start_date: str
    end_date: str
    skills: List[str]

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
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    top_voices: List[TopVoice]
    languages: List[Language]

profile_example = """
{
  "name": "Jane Doe",
  "title": "Senior Data Scientist at OpenAI",
  "location": "San Francisco, CA, United States",
  "about": "Experienced Data Scientist with a demonstrated history of working in AI and machine learning. Passionate about solving real-world problems using data.",
  "skills": [
    "Machine Learning",
    "Python",
    "Data Analysis",
    "Deep Learning"
  ],
  "experience": [
    {
      "job_positions": [
        {
          "title": "Senior Data Scientist",
          "location": "San Francisco, CA",
          "description": "Leading AI model development and deployment for natural language processing tasks.",
          "start_date": "2021-06",
          "end_date": "Present",
          "skills": [
            "Natural Language Processing",
            "Python",
            "TensorFlow"
          ]
        },
        {
          "title": "Data Scientist",
          "location": "New York, NY",
          "description": "Developed predictive models and automated analytics pipelines.",
          "start_date": "2018-01",
          "end_date": "2021-05",
          "skills": [
            "Predictive Modeling",
            "SQL",
            "Scikit-Learn"
          ]
        }
      ],
      "start_date": "2018-01",
      "end_date": "Present"
    }
  ],
  "education": [
    {
      "school": "Stanford University",
      "degree": "Master of Science in Computer Science",
      "start_date": "2015-09",
      "end_date": "2017-06"
    },
    {
      "school": "University of California, Berkeley",
      "degree": "Bachelor of Science in Statistics",
      "start_date": "2011-09",
      "end_date": "2015-05"
    }
  ],
  "top_voices": [
    {
      "name": "Andrew Ng",
      "title": "Founder at DeepLearning.AI",
      "followers": 2100000
    },
    {
      "name": "Cassie Kozyrkov",
      "title": "Chief Decision Scientist at Google",
      "followers": 1200000
    }
  ],
  "languages": [
    {
      "language": "English",
      "level": "Native"
    },
    {
      "language": "Spanish",
      "level": "Professional Working Proficiency"
    }
  ]
}


"""