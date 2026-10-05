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
- Perfil do usuário com edição de dados e alteração de senha
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
- Pillow (ImageField)
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
├── profiles/            # perfil e alteração de senha
├── accounts/            # contas bancárias
├── categories/          # categorias de lançamento
├── transactions/        # transações e atualização de saldo (signals)
├── ai/                  # agente de IA (LangChain + OpenAI) e análises
├── templates/           # templates globais (layouts, components, pages)
├── static/              # arquivos estáticos de origem (CSS/JS/imagens)
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

Com o Docker (Desktop) e o Docker Compose instalados, é possível subir a aplicação sem configurar o ambiente Python manualmente. A porta `8000` precisa estar livre.

1. Suba o serviço (a primeira execução compila a imagem):

       docker compose up --build -d

2. Acompanhe até a aplicação ficar `Up`:

       docker compose ps

   As migrações são aplicadas automaticamente na inicialização.

Serviço:

- `finanpy_web` → aplicação Django em `http://localhost:8000/` (banco SQLite persistido em volume)

3. Acesse:

- Aplicação: `http://localhost:8000/`
- Login: `http://localhost:8000/login/`

4. Crie o superusuário (usa as variáveis `DJANGO_SUPERUSER_*` do `.env`):

       docker compose exec finanpy_web python manage.py createsuperuser --noinput

   Para digitar usuário e senha manualmente, remova o `--noinput`.

5. Para acompanhar os logs (opcional):

       docker compose logs -f finanpy_web

6. Para parar e remover o container:

       docker compose down

   Para remover também o banco de dados (volume):

       docker compose down -v

## Testes

A suíte cobre modelos, formulários, views, *signals* de atualização de saldo e o isolamento de dados por usuário. Execute:

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
