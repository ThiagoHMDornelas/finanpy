# Apps do Django

O projeto Finanpy e dividido em apps Django, cada um isolando uma responsabilidade de dominio.

## users

**Responsabilidade:** Model customizado de usuario com autenticacao por email.

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `User` customizado (AbstractUser, USERNAME_FIELD='email') |
| `forms.py` | `UserRegisterForm`, `UserLoginForm` |
| `views.py` | `RegisterView`, `LoginView`, `LogoutView` |
| `urls.py` | Rotas: `/register/`, `/login/`, `/logout/` |
| `admin.py` | Registro do model User no admin |

**Model User:**

- Herda de `AbstractUser`
- `USERNAME_FIELD = 'email'`
- `username` com `blank=True, null=True`
- Campos: `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `created_at`, `updated_at`
- `UserManager` customizado com `create_user` e `create_superuser` por email

---

## profiles

**Responsabilidade:** Perfil do usuario (dados complementares ao User).

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `Profile` (OneToOne com User) |
| `forms.py` | `ProfileUpdateForm`, `PasswordChangeForm` |
| `views.py` | `ProfileDetailView`, `ProfileUpdateView`, `PasswordChangeView` |
| `urls.py` | Rotas: `/perfil/`, `/perfil/editar/`, `/perfil/alterar-senha/` |
| `signals.py` | Signal `post_save` para criar Profile ao criar User |

**Model Profile:**

- `user` (OneToOneField -> User)
- `avatar` (ImageField, opcional)
- `created_at`, `updated_at`

---

## accounts

**Responsabilidade:** Contas bancarias do usuario.

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `Account` |
| `forms.py` | `AccountForm` |
| `views.py` | `AccountListView`, `AccountCreateView`, `AccountUpdateView`, `AccountDeleteView` |
| `urls.py` | Rotas CRUD: `/contas/`, `/contas/nova/`, `/contas/<id>/editar/`, `/contas/<id>/excluir/` |
| `admin.py` | Registro do model Account |

**Model Account:**

- `user` (FK -> User)
- `name` (CharField)
- `account_type` (CharField com choices: corrente, poupanca, carteira, investimento)
- `balance` (DecimalField)
- `institution` (CharField, opcional)
- `color` (CharField, default='#7c3aed')
- `is_active` (BooleanField, default=True)
- `created_at`, `updated_at`

---

## categories

**Responsabilidade:** Categorias de lancamentos/transacoes (receita ou despesa).

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `Category` |
| `forms.py` | `CategoryForm` |
| `views.py` | `CategoryListView`, `CategoryCreateView`, `CategoryUpdateView`, `CategoryDeleteView` |
| `urls.py` | Rotas CRUD |
| `signals.py` | Signal para criar categorias padrao ao registrar novo usuario |
| `admin.py` | Registro do model Category |

**Model Category:**

- `user` (FK -> User)
- `name` (CharField)
- `category_type` (CharField com choices: receita, despesa)
- `color` (CharField, default='#7c3aed')
- `icon` (CharField, opcional)
- `created_at`, `updated_at`

**Categorias padrao (criadas via signal):**

Despesas: Alimentacao, Transporte, Moradia, Lazer, Saude, Educacao, Outros
Receitas: Salario, Freelance, Investimentos, Outros

---

## transactions

**Responsabilidade:** Transacoes financeiras (entradas e saidas).

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `Transaction` |
| `forms.py` | `TransactionForm` |
| `views.py` | `TransactionListView`, `TransactionCreateView`, `TransactionUpdateView`, `TransactionDeleteView` |
| `urls.py` | Rotas CRUD |
| `signals.py` | Signals para atualizar saldo da conta ao criar/editar/excluir transacao |
| `admin.py` | Registro do model Transaction |

**Model Transaction:**

- `user` (FK -> User)
- `account` (FK -> Account)
- `category` (FK -> Category)
- `description` (CharField)
- `amount` (DecimalField)
- `transaction_type` (CharField com choices: entrada, saida)
- `date` (DateField)
- `created_at`, `updated_at`

---

## ai

**Responsabilidade:** Agente de IA financeira — analises personalizadas com LangChain 1.0 e OpenAI.

| Arquivo | Funcao |
|---------|--------|
| `models.py` | Model `AIAnalysis` (analises geradas pelo agente) |
| `agents/finance_insight_agent.py` | Agente LangChain com tools e prompt do sistema |
| `services/analysis_service.py` | Camada de servico: orquestra analise e persistencia |
| `management/commands/run_finance_analysis.py` | Django Command para executar analises |
| `admin.py` | Registro do model AIAnalysis no admin |
| `apps.py` | Configuracao da app |

**Funcionamento:**

1. O Django Command `run_finance_analysis` e executado manualmente
2. O `AnalysisService` itera sobre usuarios ativos
3. Para cada usuario, o `FinanceInsightAgent` consulta transacoes, contas e categorias via tools
4. O agente envia os dados ao LLM (gpt-4o-mini) e recebe uma analise personalizada
5. O resultado e salvo no model `AIAnalysis`
6. A analise mais recente (`is_latest=True`) e exibida no dashboard

**Dependencias:** `langchain`, `langchain-openai`, `python-dotenv`

**URL:** `/analise/<id>/` — detalhe da analise

---

## core

**Responsabilidade:** Configuracoes globais do projeto (settings, urls, wsgi, asgi).

| Arquivo | Funcao |
|---------|--------|
| `settings.py` | Configuracoes do Django |
| `urls.py` | Rotas principais e inclusao de URLs dos apps |
| `wsgi.py` | Configuracao WSGI |
| `asgi.py` | Configuracao ASGI |

**Views do core:**

- `DashboardView` (TemplateView) - dashboard principal
- `LandingPageView` (TemplateView) - landing page publica