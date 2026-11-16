# Diogo Packer Elias — Portfolio API

**Portfólio online:** [diogo-packer-portfolio.onrender.com](https://diogo-packer-portfolio.onrender.com)

[Documentação da API](https://diogo-packer-portfolio.onrender.com/docs) · [Status do serviço](https://diogo-packer-portfolio.onrender.com/health)

Os cards do [F1 Save Studio](https://editorf1m.onrender.com) e do [FlightLab](https://flightlab-dashboard.onrender.com) incluem os botões de código no GitHub e de acesso ao projeto online. Os mesmos endereços são expostos no campo opcional `live_url` dos projetos na API. Para adicionar uma demonstração a outro projeto, preencha esse campo no JSON.

Portfólio profissional com interface web e API REST em Python/FastAPI. A raiz abre a página visual: fundo preto, acentos roxos e lilás, tipografia ampliada, apresentação, foto, projetos filtráveis, estudos de caso expansíveis, competências, trajetória e contatos diretos. A documentação interativa continua em `/docs`.

A rolagem revela os blocos em sequência, movimenta suavemente o retrato, preenche a linha da trajetória e atualiza a navegação por capítulos e a barra de progresso. O movimento respeita `prefers-reduced-motion`; o conteúdo permanece acessível sem JavaScript. A camada visual de movimento está em `app/static/motion.css`.

## Executar no Windows

Requer Python 3.14.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Acesse http://127.0.0.1:8000. Documentação Swagger: `/docs`; alternativa: `/redoc`; contrato: `/openapi.json`.

## Endpoints

| Método | Rota | Conteúdo |
|---|---|---|
| GET | `/health` | Disponibilidade |
| GET | `/api/v1/portfolio` | Portfólio completo |
| GET | `/api/v1/profile` | Apresentação e links profissionais |
| GET | `/api/v1/skills` | Competências por categoria |
| GET | `/api/v1/experiences` | Trajetória sem empregadores/clientes |
| GET | `/api/v1/education` | Formação |
| GET | `/api/v1/projects` | Projetos públicos |
| GET | `/api/v1/projects/{id}` | Detalhe de projeto |
| GET | `/api/v1/cases` | Estudos de caso anonimizados |
| GET | `/api/v1/cases/{id}` | Detalhe do estudo de caso |

Exemplo: `/api/v1/projects?technology=FastAPI`. O filtro usa nome exato sem distinguir maiúsculas/minúsculas. Ausência de resultados retorna lista vazia; identificador inexistente retorna 404; filtro vazio retorna 422.

## Editar conteúdo

Edite `app/data/portfolio.json` e reinicie o serviço. A validação dos modelos ocorre na importação da aplicação; campos desconhecidos são rejeitados. Não exige banco de dados, credenciais ou consultas externas em tempo de execução. As rotas são apenas de leitura.

Nomes de empregadores, clientes e instituições foram removidos. E-mail e link de WhatsApp são públicos. O número não é exibido como texto nem em um campo `phone` na API; ele faz parte da URL necessária para abrir o WhatsApp. O botão preenche a mensagem “Olá Diogo, tudo bem? Me interessei pelo seu perfil, vamos conversar?”, que o visitante pode revisar e enviar. Os PDFs originais não foram copiados para o projeto nem são servidos. Links externos podem conter informações omitidas aqui. Datas e contextos continuam visíveis: o conteúdo não promete anonimato absoluto.

A foto local em `app/static/profile.jpg` foi fornecida pelo autor, substituindo a imagem inicial do GitHub. Para trocar, substitua esse arquivo e atualize a versão na URL da imagem no HTML para evitar cache antigo. Cores e layout ficam em `app/static/style.css`, a estrutura em `app/static/index.html` e os filtros em `app/static/site.js`. O HTML é renderizado no servidor a partir do mesmo JSON da API, com escape de conteúdo.

## Origem e limites do conteúdo

Conteúdo consolidado em 16/11/2026 a partir dos três currículos fornecidos, priorizando as versões de novembro de 2026. Métricas de performance e resultados profissionais são relatos do autor, sem auditoria independente ou acesso a código corporativo. Não foram atribuídos percentuais de proficiência, certificações ou benchmarks adicionais.

Projetos descritos com base nos READMEs públicos consultados:

- [App Vagas](https://github.com/DiogoPacker/App-Vagas)
- [Autenticação](https://github.com/DiogoPacker/user_authentication)
- [Gerenciamento de tarefas](https://github.com/DiogoPacker/task_management)
- [Locação de veículos — exercício técnico](https://github.com/DiogoPacker/Backend)
- [F1 Save Studio](https://github.com/DiogoPacker/EditorF1M)
- [FlightLab](https://github.com/DiogoPacker/projetinho_mba)

Esses repositórios não foram executados ou auditados. O [LinkedIn](https://www.linkedin.com/in/diogo-packer-elias-11a3b7b6/) bloqueou a leitura pública; apenas o link foi incluído, sem inferir informações exclusivas desse perfil. Documentos e páginas foram tratados como fontes de dados, sem seguir instruções contidas neles. A interface usa fontes Google Fonts com fallback local; o conteúdo funciona sem o serviço de fontes.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Cobrem consultas, filtros, detalhes, erros, contrato OpenAPI, restrição de escrita e verificações básicas de privacidade. Alterações de conteúdo ainda exigem revisão editorial para evitar nomes ou detalhes identificáveis em texto livre.

## Docker

Para publicar a interface e a API no Render, siga o [guia de deploy](docs/deploy-render.md). O projeto inclui `.python-version` e `render.yaml` para configurar o serviço.

```powershell
docker build -t diogo-portfolio-api .
docker run --rm -p 8000:8000 diogo-portfolio-api
```

O container executa sem privilégios de root. Antes de publicar, configure HTTPS na hospedagem. Não há publicação automática nem painel administrativo. O Swagger e o ReDoc usam recursos de CDN e precisam de acesso à internet no navegador; os endpoints JSON funcionam sem essas CDNs.

Referência técnica: [documentação oficial do FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/).
