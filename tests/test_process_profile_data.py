import pytest
import sys
import os
# Add the parent directory to sys.path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents import analyse_prospect_agent


# Sample test data - LinkedIn profile
@pytest.fixture
def sample_profile_data():
    return {
        "name": "Nicole Murillo Fonseca",
        "about": "",
        "title": "Systems and Computing Engineering | Universidad de Los Andes",
        "skills": ["Extract, Transform, Load (ETL)", "Microsoft Power BI"],
        "location": "Bogotá, Distrito Capital, Colombia",
        "education": [
            {
                "degree": "Grado en Ingeniería de Sistemas y Computación",
                "school": "Universidad de los Andes - Colombia",
                "end_date": "2025",
                "start_date": "2020"
            }
        ],
        "languages": [
            {
                "level": "Competencia bilingüe o nativa",
                "language": "English"
            },
            {
                "level": "Competencia básica",
                "language": "French"
            }
        ],
        "experience": [
            {
                "end_date": "dic. 2023",
                "start_date": "ago. 2023",
                "job_positions": [
                    {
                        "title": "Undergraduate Teaching Assistant",
                        "skills": [],
                        "end_date": "dic. 2023",
                        "location": "",
                        "start_date": "ago. 2023",
                        "description": "- Undergraduate Teaching Assistant of Introduction to Programming"
                    }
                ]
            },
            {
                "end_date": "jun. 2023",
                "start_date": "ene. 2023",
                "job_positions": [
                    {
                        "title": "Undergraduate Teaching Assistant",
                        "skills": [],
                        "end_date": "jun. 2023",
                        "location": "",
                        "start_date": "ene. 2023",
                        "description": "- Undergraduate Teaching Assistant of IT in Organizations"
                    }
                ]
            },
            {
                "end_date": "dic. 2022",
                "start_date": "ago. 2022",
                "job_positions": [
                    {
                        "title": "Undergraduate Teaching Assistant",
                        "skills": [],
                        "end_date": "dic. 2022",
                        "location": "",
                        "start_date": "ago. 2022",
                        "description": "- Undergraduate Teaching Assistant of Introduction to Programming"
                    }
                ]
            }
        ],
        "top_voices": []
    }


def test_process_profile_data_returns_dict(sample_profile_data):
    """Test that the function returns a dictionary."""
    result = analyse_prospect_agent(sample_profile_data)
    assert isinstance(result, str)
