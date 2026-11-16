"""Server-rendered portfolio using the same validated content as the API."""
from html import escape
from pathlib import Path

from app.models import Portfolio


def tags(items: list[str]) -> str:
    return ''.join(f'<span class="tag">{escape(item)}</span>' for item in items)


def period(value: str | None) -> str:
    if value is None:
        return 'atual'
    year, month = value.split('-')
    months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    return f'{months[int(month) - 1]}/{year}'


def render_portfolio(data: Portfolio) -> str:
    template = (Path(__file__).parent / 'static' / 'index.html').read_text(encoding='utf-8')
    icons = {'app-vagas': '↗', 'user-authentication': '⌘', 'task-management': '☷',
             'car-rental': '⇄', 'f1-save-studio': '⚑', 'flightlab': '✈'}
    projects = []
    for index, project in enumerate(data.projects):
        category = 'dados' if project.id == 'flightlab' else 'aplicacoes' if project.id in {'app-vagas', 'f1-save-studio'} else 'apis'
        projects.append(f'''
        <article class="project-card" data-category="{category}">
          <div class="project-top"><span class="project-icon" aria-hidden="true">{icons.get(project.id, '↗')}</span><span class="mono">0{index + 1} / {escape(project.kind)}</span></div>
          <h3>{escape(project.title)}</h3><p>{escape(project.description)}</p>
          <div class="tags">{tags(project.technologies)}</div>
          <a class="repo-link" href="{escape(str(project.repository))}" target="_blank" rel="noopener noreferrer">Explorar no GitHub <span aria-hidden="true">↗</span></a>
        </article>''')
    cases = []
    for index, case in enumerate(data.cases):
        cases.append(f'''
        <details class="case" {'open' if index == 0 else ''}>
          <summary><span class="case-number mono">0{index + 1}</span><span><span class="eyebrow">{escape(case.context)}</span><strong>{escape(case.title)}</strong></span><span class="expand" aria-hidden="true">+</span></summary>
          <div class="case-body"><div><h4>O desafio</h4><p>{escape(case.challenge)}</p><h4>A solução</h4><p>{escape(case.solution)}</p><div class="tags">{tags(case.technologies)}</div></div><div class="outcome"><span class="eyebrow">O resultado</span><p>{escape(case.outcome)}</p><small>{escape(case.evidence)}</small></div></div>
        </details>''')
    experiences = []
    for experience in data.experiences:
        experiences.append(f'''
        <article class="experience"><div class="experience-date mono">{period(experience.start)} — {period(experience.end)}</div><div><h3>{escape(experience.role)}</h3><p>{escape(experience.context)}</p><ul>{''.join(f'<li>{escape(item)}</li>' for item in experience.contributions)}</ul><div class="tags">{tags(experience.technologies)}</div></div></article>''')
    skills = ''.join(f'<article class="skill-group"><span class="mono skill-index">0{i + 1}</span><h3>{escape(group.category)}</h3><p>{" · ".join(escape(t) for t in group.technologies)}</p></article>' for i, group in enumerate(data.skills))
    education = ''.join(f'<article class="education"><span class="mono">{e.start_year} — {e.end_year}</span><h3>{escape(e.title)}</h3></article>' for e in data.education)
    values = {
        'NAME': escape(data.profile.name), 'SUMMARY': escape(data.profile.summary),
        'LOCATION': escape(data.profile.location), 'GITHUB': escape(str(data.profile.links.github)),
        'LINKEDIN': escape(str(data.profile.links.linkedin)), 'EMAIL': escape(data.profile.email),
        'WHATSAPP': escape(str(data.profile.whatsapp)),
        'PROJECTS': ''.join(projects), 'CASES': ''.join(cases),
        'EXPERIENCES': ''.join(experiences), 'SKILLS': skills, 'EDUCATION': education,
        'PROJECT_COUNT': str(len(data.projects)),
    }
    # One pass: content containing placeholder-like text cannot become template code.
    import re
    return re.sub(r'\[\[([A-Z_]+)\]\]', lambda match: values[match[1]], template)
