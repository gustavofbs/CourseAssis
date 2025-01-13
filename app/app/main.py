from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
from app.patterns.template_method import WebUserDataCollector

app = FastAPI()

# Configurando arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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
    
    collector = WebUserDataCollector()
    collector.user_data["name"] = name
    collector.user_data["interests"] = interests_list
    collector.user_data["experience_level"] = experience_level
    
    # Aqui você pode adicionar lógica para salvar os dados
    return {"message": "Dados recebidos com sucesso!", "data": collector.get_user_data()}
