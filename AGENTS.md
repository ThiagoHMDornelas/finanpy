# AGENTS.md

## Project

Finanpy — personal finance management system. Django 5.2 full-stack monolith with Django Template Language + TailwindCSS. No API, no REST, no Docker, no tests (yet).

## Critical constraints

- **Single quotes** in all Python code — no double quotes unless necessary
- **Code in English**; **UI text in Brazilian Portuguese** (all labels, buttons, messages, templates)
- **Class Based Views** always — no function-based views
- **SQLite only** — no other database
- **`AUTH_USER_MODEL = 'users.User'`** must be set in `core/settings.py` before any migration
- Every model **must** have `created_at` and `updated_at` fields
- Signals go in `<app>/signals.py`, loaded via `apps.py` `ready()` method
- No over-engineering: use Django built-ins, don't add libraries unless truly needed

## Current state

- Apps `accounts`, `categories`, `profiles`, `transactions`, `users` exist via `startapp` — only boilerplate files, no models/forms/views yet
- `core/settings.py` has apps registered and `LANGUAGE_CODE='pt-br'`
- `TEMPLATES[0]['DIRS']` is empty — needs `BASE_DIR / 'templates'` added
- `TIME_ZONE` is `'UTC'` — should be `'America/Sao_Paulo'`
- `AUTH_USER_MODEL` not set yet
- `templates/` and `static/` directories don't exist yet
- No `urls.py` files in any app yet
- No `forms.py` or `signals.py` files exist yet
- Superuser exists (`dornelas` / `[REDACTED]`) but uses default User model — **must delete `db.sqlite3` and recreate after custom User model**

## Commands

```bash
# Activate venv (Windows)
.venv\Scripts\activate

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py check
```

Always activate `.venv` before any `python manage.py` command.

## Architecture

- **`core/`** — project config (`settings.py`, root `urls.py`, `wsgi.py`, `asgi.py`)
- **`users/`** — custom User model (`AbstractUser`, `USERNAME_FIELD='email'`) + auth views
- **`profiles/`** — Profile model (OneToOne→User) + auto-creation signal
- **`accounts/`** — bank accounts (Account model)
- **`categories/`** — transaction categories (Category model) + default categories signal
- **`transactions/`** — financial transactions (Transaction model) + balance update signals
- **`ai/`** — AI finance agent (AIAnalysis model, LangChain agent, analysis service)
- **`templates/`** — global templates: `layouts/`, `components/`, `pages/`, `partials/`
- **`static/`** — CSS/JS/images

Each app will get `forms.py`, `urls.py`, `signals.py` added as needed.

## URL patterns (planned)

| Path | App |
|------|-----|
| `/` | core (landing) |
| `/register/`, `/login/`, `/logout/` | users |
| `/dashboard/` | core |
| `/contas/...` | accounts |
| `/categorias/...` | categories |
| `/transacoes/...` | transactions |
| `/analise/<id>/` | ai |
| `/perfil/...` | profiles |

## Design system

Dark theme with violet/indigo accents. TailwindCSS via CDN. Font: Inter. All specs in `docs/design-system.md`.

## Key references

- `PRD.md` — full product requirements, sprint task list, user stories
- `docs/` — architecture, code conventions, models, design system, setup guide