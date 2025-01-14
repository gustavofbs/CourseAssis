from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import StrOutputParser
from typing import List, Dict
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class RecommendationStrategy:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Prompt template para recomendações personalizadas
        self.recommendation_template = """
        Como um especialista em educação, crie recomendações personalizadas de cursos para um estudante com o seguinte perfil:
        
        Nome: {name}
        Interesses: {interests}
        Nível de Experiência: {experience_level}
        
        Por favor, forneça recomendações específicas e relevantes que ajudarão este estudante a atingir seus objetivos educacionais.
        Foque em cursos que combinem com seu nível de experiência e interesses.
        
        Formato da resposta:
        - Nome do Curso
        - Breve descrição
        - Por que este curso é relevante para o perfil
        """
        
    def generate_recommendations(self, user_data: Dict) -> Dict:
        # Criando a chain com operadores de pipe
        chain = (
            PromptTemplate.from_template(self.recommendation_template)
            | self.llm
            | StrOutputParser()
        )
        
        # Executando a chain
        recommendations = chain.invoke({
            "name": user_data["name"],
            "interests": ", ".join(user_data["interests"]),
            "experience_level": user_data["experience_level"]
        })
        
        # Buscando informações complementares da API do Coursera
        coursera_recommendations = self._get_coursera_courses(user_data["interests"])
        
        # Formatando as recomendações para salvar no banco
        return {
            "content": recommendations + "\n\nCursos do Coursera:\n" + 
                      "\n".join([f"- {course['name']}: {course['link']}" 
                                for course in coursera_recommendations]),
            "type": "course_recommendation",
            "ai_recommendations": recommendations,
            "coursera_courses": coursera_recommendations
        }
    
    def _get_coursera_courses(self, interests: List[str]) -> List[Dict]:
        coursera_courses = []
        
        try:
            # Exemplo de chamada à API do Coursera
            # Note: Esta é uma API pública limitada, em produção você precisaria de credenciais
            for interest in interests:
                response = requests.get(
                    f"https://api.coursera.org/api/courses.v1?q=search&query={interest}&limit=3"
                )
                if response.status_code == 200:
                    courses = response.json().get("elements", [])
                    coursera_courses.extend([{
                        "name": course.get("name"),
                        "slug": course.get("slug"),
                        "description": course.get("description"),
                        "link": f"https://www.coursera.org/learn/{course.get('slug')}"
                    } for course in courses])
        except Exception as e:
            print(f"Erro ao buscar cursos do Coursera: {str(e)}")
        
        return coursera_courses

    def answer_course_question(self, question: str, course_context: Dict) -> str:
        question_template = """
        Como um especialista em educação, responda à seguinte pergunta sobre um curso:

        Contexto do Curso:
        Nome: {course_name}
        Descrição: {course_description}

        Pergunta do usuário: {question}

        Por favor, forneça uma resposta detalhada e útil baseada nas informações disponíveis sobre o curso.
        """
        
        chain = (
            PromptTemplate.from_template(question_template)
            | self.llm
            | StrOutputParser()
        )
        
        response = chain.invoke({
            "course_name": course_context.get("name", ""),
            "course_description": course_context.get("description", ""),
            "question": question
        })
        
        return response
