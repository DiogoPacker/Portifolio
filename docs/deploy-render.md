# Publicar no Render

Versão publicada: **https://diogo-packer-portfolio.onrender.com**.

Este projeto publica a interface e a API no mesmo Web Service. Não exige banco, disco persistente nem chaves de API.

## 1. Enviar o commit para o GitHub

Crie um repositório chamado `Portifolio` em https://github.com/new, na conta `DiogoPacker`. Deixe sem README, licença ou `.gitignore`, pois o projeto local já contém o primeiro commit. Pode ser privado, desde que você conceda ao Render acesso a ele.

No PowerShell, dentro de `D:\Documentos\Projetos\Portifolio`, execute:

```powershell
$portfolioGit = 'C:\Program Files\Git\cmd\git.exe'
& $portfolioGit remote add origin https://github.com/DiogoPacker/Portifolio.git
& $portfolioGit push -u origin main
```

Se escolher outro nome de repositório, ajuste a URL. Conclua a autenticação do GitHub se solicitada. Se `origin` já existir, confira `& $portfolioGit remote -v` antes de alterar qualquer configuração.

## 2. Criar o serviço

No https://dashboard.render.com, escolha **New → Web Service**. Conecte o GitHub e selecione o repositório enviado no passo anterior.

Preencha:

| Campo | Valor |
|---|---|
| Name | `diogo-packer-portfolio` ou outro nome disponível |
| Language / Runtime | **Python 3** |
| Branch | `main` |
| Region | Uma região disponível de sua preferência |
| Root Directory | Deixar vazio |
| Build Command | `python -m pip install -r requirements.txt` |
| Start Command | `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | **Free**, para começar |
| Health Check Path, em Advanced | `/health` |

Escolha explicitamente **Python 3**: a pasta também tem Dockerfile, mas este guia usa o runtime nativo. O arquivo `.python-version` seleciona Python 3.14. Não precisa preencher variáveis de ambiente; o Render fornece `PORT`.

Clique em **Deploy Web Service** e acompanhe os logs até o serviço ficar **Live**. O painel fornecerá o endereço HTTPS terminado em `.onrender.com`; o nome exato depende da disponibilidade.

Alternativa: use **New → Blueprint**, selecione o repositório e deixe o Render ler o `render.yaml` incluído. Essa opção já declara o runtime, os comandos, o plano Free e o health check. Use apenas um dos fluxos para evitar criar dois serviços.

## 3. Conferir a publicação

Abra o endereço fornecido pelo Render:

- `/`: interface completa, foto, projetos e contatos.
- `/health`: deve retornar `status: ok`.
- `/docs`: documentação interativa da API.
- `/api/v1/portfolio`: conteúdo do portfólio em JSON.

Confira também os filtros de projetos, a navegação por seções e os links de contato no celular.

## 4. Atualizar depois

Após editar e conferir as mudanças localmente:

```powershell
$portfolioGit = 'C:\Program Files\Git\cmd\git.exe'
& $portfolioGit add app README.md
& $portfolioGit commit -m 'Atualiza portfolio'
& $portfolioGit push
```

Adicione explicitamente outros arquivos alterados quando necessário. Com deploy automático habilitado no Render, novos pushes na branch conectada iniciam a atualização. Caso contrário, use **Manual Deploy → Deploy latest commit** no painel.

## Problemas comuns

- **Nenhuma porta detectada:** use exatamente o Start Command acima, com `--host 0.0.0.0 --port $PORT`. Esse comando é do servidor Linux no Render; não substitua `$PORT` pelo comando PowerShell local.
- **Erro ao importar `app`:** deixe Root Directory vazio e confirme que a pasta `app` está no GitHub.
- **Runtime Docker selecionado:** altere para Python 3 para usar os comandos deste guia.
- **Primeiro acesso demorado:** serviços Free entram em repouso após 15 minutos sem tráfego; a próxima abertura pode levar cerca de um minuto. Um plano pago remove esse repouso.
- **Foto ou cores antigas:** confirme que o último commit está publicado e atualize com `Ctrl + F5`.

Fontes oficiais consultadas em 16/11/2026: [FastAPI no Render](https://render.com/docs/deploy-fastapi), [versão do Python](https://render.com/docs/python-version), [Blueprints](https://render.com/docs/blueprint-spec) e [limites do plano Free](https://render.com/docs/free).
