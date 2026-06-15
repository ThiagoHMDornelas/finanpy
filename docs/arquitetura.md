# Arquitetura Tecnica

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Django 5.2+ |
| Frontend | Django Template Language + TailwindCSS |
| Banco de dados | SQLite (padrao do Django) |
| Autenticacao | Django Auth customizado (login por email) |
| Servidor dev | `python manage.py runserver` |
| Fontes | Inter (Google Fonts) |
| Icones | Heroicons |

## Estrutura de diretorios

```
finanpy/
├── accounts/          # contas bancarias (app Django)
├── ai/                # agente de IA financeira (app Django)
│   ├── agents/        # agentes LangChain
│   ├── management/
│   │   └── commands/  # Django Command: run_finance_analysis
│   ├── services/      # camada de servico (analysis_service)
│   ├── models.py      # model AIAnalysis
│   └── apps.py
├── categories/        # categorias de lancamentos (app Django)
├── core/              # configuracoes globais do projeto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── docs/              # documentacao do projeto
├── profiles/          # perfis de usuarios (app Django)
├── transactions/      # transacoes - entradas e saidas (app Django)
├── users/             # usuarios - model customizado (app Django)
├── templates/         # templates globais (a criar)
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   └── partials/
├── static/            # arquivos estaticos (a criar)
│   ├── css/
│   ├── js/
│   └── img/
├── db.sqlite3
├── manage.py
├── PRD.md
└── requirements.txt
```

## Padrao de app Django

Cada app segue a estrutura padrao do Django com os seguintes arquivos:

```
app_name/
├── __init__.py
├── admin.py        # Registro de models no admin
├── apps.py         # Configuracao da app
├── forms.py        # Formularios (a criar conforme necessidade)
├── migrations/     # Migracoes do banco
├── models.py       # Definicao dos models
├── signals.py      # Signals (quando necessario)
├── urls.py         # Rotas da app (a criar)
└── views.py        # Views (Class Based Views)
```

## Banco de dados

Usa SQLite, configurado em `core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Autenticacao

- Model customizado `users.User` herdando de `AbstractUser`
- `USERNAME_FIELD = 'email'` (login por email ao inves de username)
- `AUTH_USER_MODEL = 'users.User'` em `settings.py`
- Views nativas do Django para login/logout/registro

## Templates

- Diretorio global: `templates/` (configurado em `TEMPLATES[0]['DIRS']`)
- Layouts: `templates/layouts/` (app.html para autenticados, public.html para publicos)
- Components: `templates/components/` (reutilizaveis: cards, tables, forms, modals, etc.)
- Pages: `templates/pages/` (landing, login, register, dashboard)
- Partials: `templates/partials/` (messages, etc.)
- Templates de cada app: `templates/<app_name>/` (list, form, confirm_delete)

## URLs

Rotas principais (a configurar em `core/urls.py`):

| URL | App | View |
|-----|-----|------|
| `/` | core | LandingPageView |
| `/register/` | users | RegisterView |
| `/login/` | users | LoginView |
| `/logout/` | users | LogoutView |
| `/dashboard/` | core | DashboardView |
| `/contas/` | accounts | AccountListView |
| `/contas/nova/` | accounts | AccountCreateView |
| `/contas/<id>/editar/` | accounts | AccountUpdateView |
| `/contas/<id>/excluir/` | accounts | AccountDeleteView |
| `/categorias/` | categories | CategoryListView |
| `/transacoes/` | transactions | TransactionListView |
| `/analise/<id>/` | ai | AIAnalysisDetailView |
| `/perfil/` | profiles | ProfileDetailView |

## Diagrama ER

```mermaid
erDiagram
    User ||--o|| Profile : has
    User ||--o{ Account : owns
    User ||--o{ Category : owns
    User ||--o{ Transaction : creates
    User ||--o{ AIAnalysis : generates
    Account ||--o{ Transaction : has
    Category ||--o{ Transaction : belongs_to
```

## Agente de IA

A app `ai` integra o Finanpy com LangChain 1.0 e OpenAI API para gerar analises financeiras personalizadas.

- **Agente**: `FinanceInsightAgent` usando LangChain com `ChatOpenAI(model='gpt-4o-mini')`
- **Tools**: Consultam transacoes, contas, categorias e resumo financeiro do usuario
- **Execucao**: Via Django Command `python manage.py run_finance_analysis`
- **Persistencia**: Model `AIAnalysis` com historico e `is_latest` para marcar a analise mais recente
- **Documentacao**: [docs/ai-finance-agent.md](ai-finance-agent.md)