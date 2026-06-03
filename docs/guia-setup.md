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
- `TIME_ZONE = 'UTC'` — (a ajustar para `'America/Sao_Paulo'`)
- Banco de dados: SQLite (padrao)
- Apps registrados: `accounts`, `categories`, `profiles`, `transactions`, `users`

## Superuser

Um superuser ja foi criado:

- **Usuario:** dornelas
- **Senha:** [REDACTED]

> **Nota:** Ao implementar o model User customizado (`AUTH_USER_MODEL = 'users.User'`), sera necessario apagar o `db.sqlite3` e recriar o superuser.

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

## Dependencias atuais

Arquivo `requirements.txt`:

```
asgiref==3.11.1
Django==5.2.14
sqlparse==0.5.5
tzdata==2026.2
```

Novas dependencias serao adicionadas conforme necessario (ex: django-tailwind).