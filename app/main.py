import json
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.models import CaseStudy, Education, Experience, Portfolio, Profile, Project, SkillGroup
from app.website import render_portfolio

DATA_PATH = Path(__file__).parent / 'data' / 'portfolio.json'
portfolio = Portfolio.model_validate(json.loads(DATA_PATH.read_text(encoding='utf-8')))

app = FastAPI(
    title='Diogo Packer Elias | Portfolio API',
    version='1.1.0',
    description=(
        'Engenharia backend, APIs e sistemas distribuídos. '
        'Explore o perfil, os projetos públicos e os estudos de caso. '
        'Experiências apresentadas sem nomes de empregadores ou clientes. '
        'Resultados profissionais são relatos do autor nos currículos.'
    ),
    contact={'name': portfolio.profile.name, 'url': str(portfolio.profile.links.github)},
    openapi_tags=[
        {'name': 'Portfólio', 'description': 'Perfil profissional e trajetória.'},
        {'name': 'Projetos', 'description': 'Código público e experiências práticas.'},
        {'name': 'Operação', 'description': 'Disponibilidade do serviço.'},
    ],
    swagger_ui_parameters={'displayRequestDuration': True, 'defaultModelsExpandDepth': -1},
)


app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def home():
    return render_portfolio(portfolio)


@app.get('/health', tags=['Operação'])
def health() -> dict[str, str]:
    return {'status': 'ok', 'version': app.version}


@app.get('/api/v1/portfolio', response_model=Portfolio, tags=['Portfólio'])
def get_portfolio():
    """Todo o conteúdo público em uma resposta."""
    return portfolio


@app.get('/api/v1/profile', response_model=Profile, tags=['Portfólio'])
def get_profile():
    return portfolio.profile


@app.get('/api/v1/skills', response_model=list[SkillGroup], tags=['Portfólio'])
def get_skills():
    return portfolio.skills


@app.get('/api/v1/experiences', response_model=list[Experience], tags=['Portfólio'])
def get_experiences():
    """Trajetória em ordem cronológica inversa, com contextos anonimizados."""
    return portfolio.experiences


@app.get('/api/v1/education', response_model=list[Education], tags=['Portfólio'])
def get_education():
    return portfolio.education


@app.get('/api/v1/projects', response_model=list[Project], tags=['Projetos'])
def get_projects(
    technology: Annotated[str | None, Query(min_length=1, max_length=80)] = None,
):
    """Filtre pela tecnologia exata, sem diferenciar maiúsculas e minúsculas."""
    if technology is None:
        return portfolio.projects
    return [p for p in portfolio.projects if technology.strip().casefold() in
            {t.casefold() for t in p.technologies}]


@app.get('/api/v1/projects/{project_id}', response_model=Project, tags=['Projetos'])
def get_project(project_id: str):
    for project in portfolio.projects:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail='Projeto não encontrado')


@app.get('/api/v1/cases', response_model=list[CaseStudy], tags=['Projetos'])
def get_cases():
    return portfolio.cases


@app.get('/api/v1/cases/{case_id}', response_model=CaseStudy, tags=['Projetos'])
def get_case(case_id: str):
    for case in portfolio.cases:
        if case.id == case_id:
            return case
    raise HTTPException(status_code=404, detail='Estudo de caso não encontrado')
