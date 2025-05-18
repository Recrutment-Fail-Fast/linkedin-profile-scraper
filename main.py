from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from dotenv import load_dotenv
from initial_actions import initial_actions
from prompts import task, override_system_message, extend_planner_system_message
from models.models import Profile
from browser import browser
import asyncio

from utils.prospects import store_scraped_profile

load_dotenv()


controller = Controller(output_model=Profile)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.0)



data = {"name": "Manuel Porras", "title": "Ingeniero de Sistemas. Maestr\u00eda en Ingenier\u00eda de la Informaci\u00f3n. Instructor.", "location": "Colombia", "about": "Soy Ingeniero de Sistemas egresado de la Universidad de los Andes y actualmente estudiante de la Maestr\u00eda en Ingenier\u00eda de la Informaci\u00f3n. Tengo una gran pasi\u00f3n por aprender constantemente, especialmente en el \u00e1rea de programaci\u00f3n. Adem\u00e1s, me interesan profundamente los temas relacionados con Machine Learning e Inteligencia Artificial. Disfruto trabajar en equipo para desarrollar grandes proyectos y alcanzar objetivos desafiantes.Soy Ingeniero de Sistemas egresado de la Universidad de los Andes y actualmente estudiante de la Maestr\u00eda en Ingenier\u00eda de la Informaci\u00f3n. Tengo una gran pasi\u00f3n por aprender constantemente, especialmente en el \u00e1rea de programaci\u00f3n. Adem\u00e1s, me interesan profundamente los temas relacionados con Machine Learning e Inteligencia Artificial. Disfruto trabajar en equipo para desarrollar grandes proyectos y alcanzar objetivos desafiantes.", "skills": ["Microsoft Power BI", "Python (Programming Language)"], "experience": [{"job_positions": [{"title": "Instructor", "location": "Bogota, D.C., Capital District, Colombia", "description": "", "start_date": "2025-01", "end_date": "present", "skills": []}], "start_date": "2025-01", "end_date": "present"}, {"job_positions": [{"title": "Graduate Research Assistant", "location": "Bogota, D.C., Capital District, Colombia", "description": "- * **Microsoft Power BI**", "start_date": "2023-02", "end_date": "2025-01", "skills": []}], "start_date": "2023-02", "end_date": "2025-01"}, {"job_positions": [{"title": "Monitor de investigaci\u00f3n en proyecto de Mapa abierto para analisis de datos solares", "location": "Unknown", "description": "", "start_date": "2022-01", "end_date": "2022-06", "skills": []}], "start_date": "2022-01", "end_date": "2022-06"}, {"job_positions": [{"title": "Monitor en la materia de Dise\u00f1o y programaci\u00f3n orientada a objetos. (DPOO)", "location": "Bogota, D.C., Capital District, Colombia", "description": "", "start_date": "2022-01", "end_date": "2022-06", "skills": []}], "start_date": "2022-01", "end_date": "2022-06"}, {"job_positions": [{"title": "Monitor de investigaci\u00f3n en proyecto de Mapa abierto para analisis de datos solares", "location": "Unknown", "description": "", "start_date": "2022-01", "end_date": "2022-06", "skills": []}], "start_date": "2022-01", "end_date": "2022-06"}, {"job_positions": [{"title": "Monitor en la materia de Dise\u00f1o y programaci\u00f3n orientada a objetos. (DPOO)", "location": "Bogota, D.C., Capital District, Colombia", "description": "", "start_date": "2021-01", "end_date": "2021-06", "skills": []}], "start_date": "2021-01", "end_date": "2021-06"}, {"job_positions": [{"title": "Monitor en la materia de Introducci\u00f3n a la Ingenier\u00eda de Sistemas", "location": "Bogota,D.C., Capital District, Colombia", "description": "", "start_date": "2020-08", "end_date": "2020-12", "skills": []}], "start_date": "2020-08", "end_date": "2020-12"}], "education": [{"school": "Universidad de los Andes - Colombia", "degree": "Engineer's degree, Computer Science", "start_date": "2019", "end_date": "2023"}], "top_voices": [{"name": "Freddy Vega", "title": "CEO and Founder at Platzi: Latin America's School of Technology", "followers": 273475}, {"name": "Andrew Ng", "title": "Founder of DeepLearning.AI; Managing General Partner of AI Fund; Exec Chairman of Landing AI", "followers": 2061703}], "languages": []}


async def main():
    agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
		controller=controller,
		initial_actions=initial_actions,
		override_system_message=override_system_message,
		extend_planner_system_message=extend_planner_system_message
    )
    result = await agent.run()
    await browser.close()
    store_scraped_profile(result)
asyncio.run(main())