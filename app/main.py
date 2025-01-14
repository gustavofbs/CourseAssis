from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import os
from dotenv import load_dotenv
from app.patterns.template_method import WebUserDataCollector
from app.patterns.factory_method import SQLiteStorageFactory
from app.patterns.recommendation_strategy import RecommendationStrategy

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
