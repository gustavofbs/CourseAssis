from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import os
from dotenv import load_dotenv
from app.patterns.user_data_template import WebUserDataCollector
from app.patterns.data_storage_factory import SQLiteStorageFactory
from app.patterns.recommendation_strategy import RecommendationStrategy
from app.patterns.study_plan_template import CourseraStudyPlanGenerator
from fastapi.exceptions import HTTPException

load_dotenv()

app = FastAPI()

# Configurando arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Configurando o storage
db_path = os.path.join(os.path.dirname(__file__), "data.db")
storage_factory = SQLiteStorageFactory(db_path)
storage = storage_factory.create_storage()
recommendation_strategy = RecommendationStrategy()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit_form(
    request: Request,
    name: str = Form(...),
    interests: str = Form(...),
    experience_level: str = Form(...)
):
    # Converter a string JSON de interesses em lista
    interests_list = json.loads(interests)
    
    # Usar o Template Method para coletar dados
    collector = WebUserDataCollector()
    collector.user_data["name"] = name
    collector.user_data["interests"] = interests_list
    collector.user_data["experience_level"] = experience_level
    
    # Usar o Factory Method para salvar os dados
    user_id = storage.save_user(collector.get_user_data())
    
    # Gerar recomendações personalizadas
    recommendations = recommendation_strategy.generate_recommendations(collector.get_user_data())
    
    # Salvar as recomendações
    storage.save_recommendation(user_id, recommendations)
    
    return {
        "message": "Dados recebidos com sucesso!",
        "data": collector.get_user_data(),
        "user_id": user_id,
        "recommendations": recommendations
    }

@app.post("/ask_question")
async def ask_question(
    request: Request,
    question: str = Form(...),
    course_name: str = Form(...),
    course_description: str = Form(...)
):
    course_context = {
        "name": course_name,
        "description": course_description
    }
    
    response = recommendation_strategy.answer_course_question(question, course_context)
    
    return {
        "answer": response
    }

@app.post("/generate_study_plan")
async def generate_study_plan(
    course_name: str = Form(...),
    course_description: str = Form(...),
    weekly_hours: int = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    fundamentals_percent: int = Form(...),
    development_percent: int = Form(...),
    project_percent: int = Form(...)
):
    try:
        # Criar o gerador de plano de estudos
        study_plan_generator = CourseraStudyPlanGenerator()
        
        # Preparar os dados do curso
        course_data = {
            "name": course_name,
            "description": course_description,
            "total_hours": 40  # Estimativa inicial
        }
        
        # Preparar as preferências do usuário
        user_preferences = {
            "weekly_hours": int(weekly_hours),
            "start_date": start_date,
            "end_date": end_date,
            "fundamentals_percent": int(fundamentals_percent),
            "development_percent": int(development_percent),
            "project_percent": int(project_percent)
        }
        
        # Gerar o plano de estudos
        study_plan = study_plan_generator.create_study_plan(course_data, user_preferences)
        
        return JSONResponse(content=study_plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
