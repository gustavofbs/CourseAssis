from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List
import json

class StudyPlanGenerator(ABC):
    def __init__(self):
        self.study_plan = {
            "course_name": "",
            "description": "",
            "total_hours": 0,
            "weekly_hours": 0,
            "start_date": None,
            "end_date": None,
            "fundamentals_percent": 0,
            "development_percent": 0,
            "project_percent": 0,
            "modules": [],
            "schedule": [],
            "weekly_breakdown": []
        }

    def create_study_plan(self, course_data: Dict, user_preferences: Dict) -> Dict:
        """Template method que define o algoritmo para criar um plano de estudos"""
        self._validate_input(course_data, user_preferences)
        self.collect_course_info(course_data)
        self.calculate_timeline(user_preferences)
        self.generate_modules()
        self.create_schedule()
        return self.study_plan

    def _validate_input(self, course_data: Dict, user_preferences: Dict) -> None:
        """Validates input data"""
        if not course_data.get("course_name"):
            raise ValueError("Course name cannot be empty")
        if not course_data.get("description"):
            raise ValueError("Course description cannot be empty")
            
        required_preferences = ["weekly_hours", "start_date", "end_date", 
                              "fundamentals_percent", "development_percent", "project_percent"]
        for field in required_preferences:
            if field not in user_preferences:
                raise ValueError(f"Missing required field: {field}")
                
        total_percent = (user_preferences.get("fundamentals_percent", 0) + 
                        user_preferences.get("development_percent", 0) + 
                        user_preferences.get("project_percent", 0))
        if total_percent != 100:
            raise ValueError("Percentages must sum to 100")

    @abstractmethod
    def collect_course_info(self, course_data: Dict) -> None:
        """Coleta informações básicas do curso"""
        pass

    @abstractmethod
    def calculate_timeline(self, user_preferences: Dict) -> None:
        """Calcula o cronograma baseado nas preferências do usuário"""
        pass

    @abstractmethod
    def generate_modules(self) -> None:
        """Gera os módulos do curso"""
        pass

    @abstractmethod
    def create_schedule(self) -> None:
        """Cria o cronograma detalhado"""
        pass

    def format_date_br(self, date_str: str) -> str:
        """Converte data do formato ISO para o formato brasileiro"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")


class CourseraStudyPlanGenerator(StudyPlanGenerator):
    def collect_course_info(self, course_data: Dict) -> None:
        self.study_plan["course_name"] = course_data.get("course_name", "")
        self.study_plan["description"] = course_data.get("description", "")
        # Estimativa padrão de horas totais se não fornecido
        self.study_plan["total_hours"] = course_data.get("total_hours", 40)

    def calculate_timeline(self, user_preferences: Dict) -> None:
        weekly_hours = int(user_preferences.get("weekly_hours", 10))
        self.study_plan["weekly_hours"] = weekly_hours
        
        # Converter datas de string para datetime
        start_date = datetime.strptime(user_preferences.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(user_preferences.get("end_date"), "%Y-%m-%d")
        
        # Calcular o número total de semanas disponíveis
        total_weeks = (end_date - start_date).days / 7
        
        # Calcular o total de horas disponíveis no período
        total_available_hours = total_weeks * weekly_hours
        
        # Ajustar o total de horas do curso para caber no período especificado
        self.study_plan["total_hours"] = min(self.study_plan.get("total_hours", 40), total_available_hours)
        
        # Salvar datas no formato brasileiro
        self.study_plan["start_date"] = start_date.strftime("%d/%m/%Y")
        self.study_plan["end_date"] = end_date.strftime("%d/%m/%Y")
        
        # Guardar as datas para uso no create_schedule
        self.start_date = start_date
        self.end_date = end_date
        
        # Guardar as porcentagens para uso no generate_modules
        self.study_plan["fundamentals_percent"] = int(user_preferences.get("fundamentals_percent", 30))
        self.study_plan["development_percent"] = int(user_preferences.get("development_percent", 40))
        self.study_plan["project_percent"] = int(user_preferences.get("project_percent", 30))

    def generate_modules(self) -> None:
        # Usar as porcentagens definidas pelo usuário para distribuir o tempo
        fundamentals_percent = self.study_plan["fundamentals_percent"] / 100
        development_percent = self.study_plan["development_percent"] / 100
        project_percent = self.study_plan["project_percent"] / 100
        
        total_hours = self.study_plan["total_hours"]
        
        self.study_plan["modules"] = [
            {
                "name": "Fundamentos",
                "duration_hours": total_hours * fundamentals_percent,
                "topics": ["Conceitos básicos", "Introdução à área", "Ferramentas essenciais"]
            },
            {
                "name": "Desenvolvimento",
                "duration_hours": total_hours * development_percent,
                "topics": ["Práticas avançadas", "Projetos práticos", "Estudos de caso"]
            },
            {
                "name": "Projeto Final",
                "duration_hours": total_hours * project_percent,
                "topics": ["Aplicação prática", "Desenvolvimento do projeto", "Apresentação"]
            }
        ]

    def get_resources_by_topic(self, topic_name: str) -> List[str]:
        """Retorna recursos específicos baseados no tipo de tópico"""
        resources_map = {
            "Conceitos básicos": [
                "Vídeoaulas introdutórias",
                "Guia de estudo",
                "Quiz de conceitos"
            ],
            "Introdução à área": [
                "Artigos de referência",
                "Vídeos explicativos",
                "Mapa conceitual"
            ],
            "Ferramentas essenciais": [
                "Tutoriais práticos",
                "Documentação oficial",
                "Exercícios guiados"
            ],
            "Práticas avançadas": [
                "Workshops online",
                "Estudos de caso",
                "Exercícios avançados"
            ],
            "Projetos práticos": [
                "Templates de projeto",
                "Código de exemplo",
                "Revisão por pares"
            ],
            "Estudos de caso": [
                "Análise de casos reais",
                "Discussões em grupo",
                "Relatórios técnicos"
            ],
            "Aplicação prática": [
                "Mentoria individual",
                "Feedback personalizado",
                "Documentação do projeto"
            ],
            "Desenvolvimento do projeto": [
                "Repositório de código",
                "Code review",
                "Testes automatizados"
            ],
            "Apresentação": [
                "Template de apresentação",
                "Guia de boas práticas",
                "Sessão de feedback"
            ]
        }
        return resources_map.get(topic_name, ["Vídeos", "Exercícios", "Leituras complementares"])

    def create_schedule(self) -> None:
        current_date = self.start_date
        weekly_hours = self.study_plan["weekly_hours"]
        schedule = []
        weekly_breakdown = []

        for module in self.study_plan["modules"]:
            # Calcular a porcentagem deste módulo
            if module["name"] == "Fundamentos":
                percent = self.study_plan["fundamentals_percent"] / 100
            elif module["name"] == "Desenvolvimento":
                percent = self.study_plan["development_percent"] / 100
            else:  # Projeto Final
                percent = self.study_plan["project_percent"] / 100
            
            # Calcular horas semanais para este módulo específico
            module_weekly_hours = weekly_hours * percent
            
            # Calcular quantas semanas este módulo vai durar
            module_weeks = module["duration_hours"] / module_weekly_hours
            module_end_date = current_date + timedelta(weeks=module_weeks)
            
            module_schedule = {
                "module_name": module["name"],
                "start_date": current_date.strftime("%d/%m/%Y"),
                "end_date": module_end_date.strftime("%d/%m/%Y"),
                "weekly_activities": []
            }

            # Distribuir as horas semanais igualmente entre os tópicos
            hours_per_topic = module_weekly_hours / len(module["topics"])
            
            for topic in module["topics"]:
                activity = {
                    "topic": topic,
                    "hours": round(hours_per_topic, 1),
                    "resources": self.get_resources_by_topic(topic)
                }
                module_schedule["weekly_activities"].append(activity)
                
                # Adicionar à weekly_breakdown
                week_number = len(weekly_breakdown) + 1
                weekly_breakdown.append({
                    "week": week_number,
                    "module": module["name"],
                    "topic": topic,
                    "hours": round(hours_per_topic, 1),
                    "start_date": current_date.strftime("%d/%m/%Y"),
                    "end_date": (current_date + timedelta(days=7)).strftime("%d/%m/%Y")
                })
                current_date += timedelta(days=7)

            schedule.append(module_schedule)

        self.study_plan["schedule"] = schedule
        self.study_plan["weekly_breakdown"] = weekly_breakdown
