# Finanpy — Sistema de Gestão de Finanças Pessoais

![Testes](https://github.com/ThiagoHMDornelas/finanpy/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Django](https://img.shields.io/badge/django-5.2-092E20)
![LangChain](https://img.shields.io/badge/LangChain-1.3-1C3C3C)
![License](https://img.shields.io/badge/license-MIT-green)

Sistema web de gestão de finanças pessoais desenvolvido com Django. Permite controlar contas, categorias e transações (entradas e saídas), acompanhar a saúde financeira em um dashboard e ainda contar com um **agente de IA** (LangChain + OpenAI) que analisa os dados do usuário e gera insights e recomendações personalizadas.

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Agente de IA](#agente-de-ia)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados](#banco-de-dados)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Principais rotas](#principais-rotas)
- [Painel administrativo](#painel-administrativo)
- [Licença](#licença)

## Visão geral

O **Finanpy** é uma aplicação web monolítica para o controle de finanças pessoais. Cada usuário gerencia suas próprias contas bancárias, categorias e transações; os saldos das contas são atualizados automaticamente conforme as movimentações, via *signals* do Django. A tela inicial (landing page) apresenta o produto, e o **dashboard** consolida saldo total, receitas e despesas do mês, além de um gráfico dos últimos seis meses.

O projeto prioriza simplicidade, usando recursos nativos do Django (Class Based Views, autenticação, ORM) e banco **SQLite**.

## Funcionalidades

- Autenticação por **e-mail** (sem username): cadastro, login e logout
- Dashboard com saldo total, receitas e despesas do mês, gráfico de 6 meses e transações recentes
- CRUD de contas bancárias (tipo, saldo, instituição e cor)
- CRUD de categorias (receita/despesa, cor e ícone) com **categorias padrão** criadas automaticamente no cadastro
- CRUD de transações com filtros por tipo, categoria, conta, período e busca
- Atualização automática do saldo das contas via *signals* (criar, editar e excluir transações)
- Perfil do usuário com edição de dados, avatar e alteração de senha
- **Agente de IA financeiro** com análise, insights e recomendações (LangChain + OpenAI)
- Isolamento de dados por usuário (cada usuário acessa apenas seus registros)
- Painel administrativo do Django

## Agente de IA

A app `ai` integra um agente construído com **LangChain** (`create_agent`) sobre o modelo **OpenAI** (`ChatOpenAI`). O agente recebe ferramentas que consultam os dados do usuário (transações, contas, categorias, gastos por categoria e comparativo de receitas vs. despesas) e devolve uma análise estruturada com visão geral, insights, recomendações e alertas. Cada análise é persistida no modelo `AIAnalysis`, com limite de geração de uma nova a cada 24 horas.

Pela interface, o botão **Gerar Análise** no dashboard dispara a geração (rota POST `/analise/gerar/`). Também é possível rodar via comando: `python manage.py run_finance_analysis --user-email <email>`.

A funcionalidade de IA é **opcional**: sem `OPENAI_API_KEY` a aplicação funciona normalmente, apenas a geração de análise fica indisponível.

## Tecnologias

- Python
- Django 5.2
- LangChain / LangGraph + OpenAI
- Pillow (avatar)
- python-dotenv (variáveis de ambiente)
- TailwindCSS (via CDN)
- SQLite
- Docker e Docker Compose
- flake8 (desenvolvimento)
- GitHub Actions (CI)

## Estrutura do projeto

```
finanpy/
├── core/                # configurações, urls raiz, landing e dashboard
├── users/               # User customizado (login por e-mail) e autenticação
├── profiles/            # perfil (avatar) e alteração de senha
├── accounts/            # contas bancárias
├── categories/          # categorias de lançamento
├── transactions/        # transações e atualização de saldo (signals)
├── ai/                  # agente de IA (LangChain + OpenAI) e análises
├── templates/           # templates globais (layouts, components, pages)
├── static/              # arquivos estáticos de origem (CSS/JS/imagens)
├── media/               # uploads de usuário (avatares) — não versionado
├── docs/                # documentação do projeto
├── .github/workflows/   # pipeline de CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
├── .env.example         # exemplo de variáveis de ambiente
├── manage.py
├── requirements.txt
├── requirements_dev.txt
└── PRD.md               # product requirement document
```

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Crie o arquivo de ambiente (veja [Variáveis de ambiente](#variáveis-de-ambiente)):

    copy .env.example .env        # Windows
    cp .env.example .env          # Linux/macOS

Aplique as migrações:

    python manage.py migrate

Crie um usuário administrador:

    python manage.py createsuperuser

Inicie o servidor:

    python manage.py runserver

A aplicação estará disponível em:

    http://127.0.0.1:8000/

## Variáveis de ambiente

Copie o `.env.example` para `.env` e ajuste os valores:

    # Django
    SECRET_KEY=troque-por-uma-chave-secreta
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Superusuário (usado com createsuperuser --noinput)
    DJANGO_SUPERUSER_EMAIL=
    DJANGO_SUPERUSER_FIRST_NAME=
    DJANGO_SUPERUSER_PASSWORD=

    # Agente de IA (opcional)
    OPENAI_API_KEY=
    OPENAI_MODEL=gpt-4o-mini
    AI_MAX_TOKENS=2000
    AI_TEMPERATURE=0.7

## Banco de dados

O projeto usa **SQLite** (`db.sqlite3`), sem necessidade de serviços externos. No Docker, o banco é persistido em um volume e o caminho é definido pela variável `SQLITE_PATH`.

## Executar com Docker

A forma recomendada de rodar a aplicação. O Docker Compose sobe o serviço já configurado (Django + SQLite), sem precisar montar o ambiente Python manualmente.

**Pré-requisitos:**

- Docker Desktop instalado e em execução (engine)
- Docker Compose (já vem com o Docker Desktop)
- Git instalado (para clonar o repositório)
- A porta `8000` livre

> **Importante:** o Docker Desktop sozinho **não** faz o setup inicial — ele é o *engine* e o painel de gerenciamento. Criar o `.env` e rodar `docker compose up --build` são feitos pelo **terminal**; o Docker Desktop é ótimo para acompanhar logs, iniciar/parar e abrir um terminal dentro do container **depois** que a stack subiu.

> **Atenção:** neste projeto o `docker-compose.yml` usa `env_file: .env`, então o arquivo `.env` é **obrigatório** — sem ele o `docker compose up` falha. Crie-o no passo 2.

### Passo a passo (via shell / PowerShell)

**1. Clone o repositório**

```powershell
git clone https://github.com/ThiagoHMDornelas/finanpy.git
cd finanpy
```

> O `git clone` cria a pasta `finanpy` dentro da pasta atual, e o `cd` entra nela. Se você **já está dentro** da pasta do projeto, **pule o `cd`**.

**2. Crie o arquivo de ambiente**

```powershell
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

> Atenção: se você **já tem** um `.env` na pasta, o comando acima vai **sobrescrevê-lo**. Nesse caso, **pule este passo** e apenas edite o `.env` existente.

A chave `OPENAI_API_KEY` é **opcional**: sem ela a aplicação funciona normalmente, apenas a geração de análise por IA fica indisponível. Veja a seção [Variáveis de ambiente](#variáveis-de-ambiente).

**3. Suba a stack.** Na primeira execução o Docker compila a imagem da aplicação — pode levar alguns minutos:

```powershell
docker compose up --build -d
```

**4. Confira os containers:**

```powershell
docker compose ps
```

Espere o `finanpy_web` como `Up`. As migrações são aplicadas automaticamente na inicialização.

| Serviço | Porta | Acesso |
|---|---|---|
| `finanpy_web` | 8000 | `http://localhost:8000` |

**5. Acesse:**

- Aplicação: `http://localhost:8000/`
- Login: `http://localhost:8000/login/`

**6. Crie o superusuário.** Antes, preencha `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_FIRST_NAME` e `DJANGO_SUPERUSER_PASSWORD` no `.env` — com esses campos vazios (como no `.env.example`), o `--noinput` falha com o erro *"Email cannot be blank"*:

```powershell
docker compose exec finanpy_web python manage.py createsuperuser --noinput
```

> Para digitar usuário e senha manualmente, remova o `--noinput`.

**7. Comandos úteis:**

```powershell
docker compose logs -f finanpy_web     # logs da aplicação
docker compose restart finanpy_web     # reinicia a aplicação
docker compose down                    # para e remove o container
docker compose down -v                 # remove também o volume (banco de dados)
```

> O banco SQLite fica no volume `sqlite_data` e **persiste** entre reinícios. O `docker compose down -v` apaga o banco.

### Usando o Docker Desktop (interface gráfica)

Depois que a stack estiver no ar (passo 3), o Docker Desktop ajuda a operar. Na aba **Containers** você verá o grupo `finanpy` com o serviço `finanpy_web`:

- **Logs**: clique no container → aba *Logs* (equivale a `docker compose logs`).
- **Start / Stop / Restart**: botões no topo do container.
- **Terminal no container**: botão *Exec* (útil para depurar dentro do container).
- **Abrir no navegador**: clique na porta publicada (`8000:8000`).
- **Limpeza**: *Delete* remove o container; em **Volumes** você apaga o banco.

O que **não** dá para fazer pela interface gráfica: criar o `.env` e rodar `docker compose up --build` em um clone novo (isso é feito pelo terminal).

### Problemas comuns

- **A aplicação não abre**
  - Veja os logs: `docker compose logs -f finanpy_web`
  - Confirme que o container está `Up`: `docker compose ps`
- **`docker compose up` falha com "env file .env not found"** → crie o `.env` (passo 2)
- **A geração de análise por IA não funciona** → sem `OPENAI_API_KEY` no `.env` a funcionalidade fica indisponível (o restante da aplicação funciona normalmente)
- **Erro de porta em uso** (`8000`) → pare o serviço que ocupa a porta ou ajuste o mapeamento no `docker-compose.yml` (ex.: `8001:8000`) e acesse em `http://localhost:8001`
- **Os dados sumiram** → você rodou `docker compose down -v` (remove o volume do banco). Use `docker compose down` para manter os dados

## Testes

A suíte cobre modelos, formulários, views, *signals* de atualização de saldo, o isolamento de dados por usuário e o agente de IA. Execute:

    python manage.py test

O **lint** do código é feito com `flake8` (configuração em `.flake8`):

    flake8

A suíte e o lint também rodam automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`), em SQLite. O resultado é exibido no badge no topo deste README.

## Principais rotas

| Rota | Descrição |
|---|---|
| `/` | Landing page (pública) |
| `/register/`, `/login/`, `/logout/` | Autenticação |
| `/dashboard/` | Dashboard (requer login) |
| `/contas/`, `/contas/nova/`, `/contas/<id>/editar/`, `/contas/<id>/excluir/` | CRUD de contas |
| `/categorias/`, `/categorias/nova/`, `/categorias/<id>/editar/`, `/categorias/<id>/excluir/` | CRUD de categorias |
| `/transacoes/`, `/transacoes/nova/`, `/transacoes/<id>/editar/`, `/transacoes/<id>/excluir/` | CRUD de transações |
| `/perfil/`, `/perfil/editar/`, `/perfil/alterar-senha/` | Perfil do usuário |
| `/analise/gerar/` | Gera uma nova análise de IA (POST) |
| `/analise/<id>/` | Detalhe de uma análise de IA |
| `/admin/` | Painel administrativo |

## Painel administrativo

Acesse `/admin/` com o superusuário criado. Todos os recursos (usuários, perfis, contas, categorias, transações e análises de IA) ficam disponíveis para gerenciamento.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
