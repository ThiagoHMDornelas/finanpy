# Guia de Setup

## Prerequisitos

- Python 3.10+
- pip

## Instalacao

```bash
# Clonar o repositorio
git clone <repo-url>
cd finanpy

# Criar e ativar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuracao

O arquivo `core/settings.py` contem a configuracao atual do projeto:

- `LANGUAGE_CODE = 'pt-br'` — internacionalizacao para pt-BR
- `TIME_ZONE = 'America/Sao_Paulo'` — fuso horario do projeto
- Banco de dados: SQLite (padrao)
- Apps registrados: `accounts`, `categories`, `profiles`, `transactions`, `users`

## Superuser

Crie um superusuario para acessar o painel administrativo:

```bash
python manage.py createsuperuser
```

> **Nota:** o projeto usa um model User customizado (`AUTH_USER_MODEL = 'users.User'`), definido antes da primeira migracao.

## Comandos principais

```bash
# Ativar o ambiente virtual (Windows)
.venv\Scripts\activate

# Executar migracoes
python manage.py migrate

# Criar novas migracoes
python manage.py makemigrations

# Criar superuser
python manage.py createsuperuser

# Rodar servidor de desenvolvimento
python manage.py runserver

# Acessar admin
# http://127.0.0.1:8000/admin/

# Verificar problemas
python manage.py check
```

## Dependencias

As dependencias do projeto estao em `requirements.txt` (Django, LangChain/LangGraph, OpenAI, Pillow, python-dotenv, entre outras). Para desenvolvimento (lint):

```bash
pip install -r requirements_dev.txt
```