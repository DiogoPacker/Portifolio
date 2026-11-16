import json
import re

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize('path', [
    '/health', '/docs', '/redoc', '/openapi.json', '/api/v1/portfolio',
    '/api/v1/profile', '/api/v1/skills', '/api/v1/experiences',
    '/api/v1/education', '/api/v1/cases', '/api/v1/projects',
])
def test_public_endpoints(path):
    assert client.get(path).status_code == 200


def test_entrypoint_serves_portfolio_interface():
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/html')
    assert 'Diogo Packer' in response.text
    assert '[[PROJECTS]]' not in response.text
    assert response.text.count('class="project-card"') == 6
    for path in ['/static/style.css', '/static/site.js', '/static/profile.jpg']:
        assert client.get(path).status_code == 200


def test_project_filter_and_details():
    projects = client.get('/api/v1/projects?technology=fAsTaPi').json()
    assert {project['id'] for project in projects} == {'app-vagas', 'f1-save-studio', 'flightlab'}
    assert all('FastAPI' in p['technologies'] for p in projects)
    assert client.get('/api/v1/projects?technology=unknown').json() == []
    assert client.get('/api/v1/projects?technology=').status_code == 422


@pytest.mark.parametrize('collection', ['projects', 'cases'])
def test_detail_and_not_found(collection):
    items = client.get(f'/api/v1/{collection}').json()
    for item in items:
        assert client.get(f'/api/v1/{collection}/{item["id"]}').json() == item
    assert client.get(f'/api/v1/{collection}/does-not-exist').status_code == 404


def test_public_data_only_has_authorized_contacts_and_no_employer_fields():
    data = client.get('/api/v1/portfolio').json()
    serialized = json.dumps(data, ensure_ascii=False)
    assert set(re.findall(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', serialized)) == {'diogopacker@hotmail.com'}
    assert 'phone' not in data['profile']
    from urllib.parse import parse_qs, urlparse
    link = urlparse(data['profile']['whatsapp'])
    assert link.netloc == 'wa.me'
    assert parse_qs(link.query)['text'] == ['Olá Diogo, tudo bem? Me interessei pelo seu perfil, vamos conversar?']
    for experience in data['experiences']:
        assert set(experience) == {
            'id', 'role', 'start', 'end', 'context', 'contributions', 'technologies'
        }
    assert all('evidence' in case for case in data['cases'])


def test_interface_contacts_and_safe_rendering():
    from app.main import portfolio
    from app.website import render_portfolio
    copy = portfolio.model_copy(deep=True)
    copy.profile.name = '<script>alert(1)</script>'
    html = render_portfolio(copy)
    assert '<script>alert(1)</script>' not in html
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in html
    assert 'mailto:diogopacker@hotmail.com' in html
    assert 'https://wa.me/5511943351707' in html
    assert '+55 (11) 94335-1707' not in html
    assert '[[PHONE]]' not in html
    from html.parser import HTMLParser
    from urllib.parse import parse_qs, urlparse

    class Links(HTMLParser):
        hrefs = []

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                self.hrefs.append(dict(attrs).get('href', ''))

    parser = Links()
    parser.feed(html)
    whatsapp = next(url for url in parser.hrefs if url.startswith('https://wa.me/'))
    assert parse_qs(urlparse(whatsapp).query)['text'] == ['Olá Diogo, tudo bem? Me interessei pelo seu perfil, vamos conversar?']


def test_no_write_or_source_file_access():
    assert client.post('/api/v1/profile', json={'name': 'changed'}).status_code == 405
    assert client.get('/app/data/portfolio.json').status_code == 404
    assert client.get('/requirements.txt').status_code == 404


def test_schema_documents_typed_responses():
    schema = client.get('/openapi.json').json()
    response = schema['paths']['/api/v1/portfolio']['get']['responses']['200']
    assert response['content']['application/json']['schema']['$ref'].endswith('/Portfolio')


def test_live_project_links_in_api_and_interface():
    html = client.get('/').text
    expected = {
        'f1-save-studio': 'https://editorf1m.onrender.com/',
        'flightlab': 'https://flightlab-dashboard.onrender.com/',
    }
    for project_id, url in expected.items():
        project = client.get(f'/api/v1/projects/{project_id}').json()
        assert project['live_url'] == url
        assert f'href="{url}"' in html
        assert f'href="{project["repository"]}"' in html
    assert html.count('class="live-link"') == 2
    assert client.get('/api/v1/projects/app-vagas').json()['live_url'] is None
