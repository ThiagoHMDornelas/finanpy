## Lista de tarefas

> **Estado atual do projeto:**
> - Projeto Django já criado na pasta correta (`finanpy/`)
> - Ambiente virtual `.venv` já configurado
> - `startapp` já executado para: `accounts`, `categories`, `transactions`, `profiles`, `users` (apenas arquivos iniciais padrão)
> - Superuser já criado: user `dornelas` / senha `[REDACTED]` (usando model User padrão do Django — será necessário recriar após implementar o model customizado)
> - `core/settings.py` já configurado com apps registrados, `LANGUAGE_CODE='pt-br'` e banco SQLite
> - `requirements.txt` já existe com Django 5.2.14

### Sprint 1 — Setup do projeto e autenticação

#### T1.1 — Configuração inicial do projeto ✅
- [X] 1.1.1 — Criar estrutura de diretórios dos apps (`accounts`, `categories`, `transactions`, `profiles`, `users`) — **já realizado via `startapp`**
- [X] 1.1.2 — Criar diretório `templates/` com subpastas `components/`, `pages/`, `partials/`, `layouts/`
- [X] 1.1.3 — Criar diretório `static/` com subpastas `css/`, `js/`, `img/`
- [X] 1.1.4 — Configurar `settings.py`: apps registrados, `LANGUAGE_CODE='pt-br'` — **já realizado**
- [X] 1.1.5 — Atualizar `settings.py`: adicionar `TEMPLATES[0]['DIRS']` apontando para diretório de templates global, `STATICFILES_DIRS`, `TIME_ZONE='America/Sao_Paulo'`, `AUTH_USER_MODEL = 'users.User'`, `LOGIN_URL`, `LOGIN_REDIRECT_URL = 'dashboard'`, `LOGOUT_REDIRECT_URL = 'landing'`
- [X] 1.1.6 — Atualizar `requirements.txt` adicionando dependências necessárias (Pillow para ImageField)
- [X] 1.1.7 — Configurar TailwindCSS via CDN no template base (`templates/base.html`)
- [X] 1.1.8: Criar arquivo `.env` na raiz do projeto
- [X] 1.1.9: Mover SECRET_KEY para arquivo `.env`
- [X] 1.1.10 — **Atenção:** `db.sqlite3` apagado. Banco será recriado após implementar model User customizado (T1.2)

#### T1.2 — Model User customizado ✅
- [X] 1.2.1 — Criar model `User` em `users/models.py` herdando de `AbstractUser`, substituindo `username` por `email` como campo principal (`USERNAME_FIELD = 'email'`), tornando `username` não obrigatório (`blank=True, null=True`)
- [X] 1.2.2 — Adicionar campos `created_at` e `updated_at` com `auto_now_add` e `auto_now`
- [X] 1.2.3 — Adicionar `REQUIRED_FIELDS = ['first_name']` no model User
- [X] 1.2.4 — Criar `UserManager` customizado que usa email para `create_user` e `create_superuser`
- [X] 1.2.5 — Registrar model `User` no `users/admin.py` com configuração adequada
- [X] 1.2.6 — Apagar `db.sqlite3` existente, executar `makemigrations` e `migrate` (necessário pois o superuser atual usa o model padrão)
- [X] 1.2.7 — Recriar superuser com o novo model: `python manage.py createsuperuser` (email: dornelas, senha: [REDACTED])

#### T1.3 — Model Profile e Signal ✅
- [X] 1.3.1 — Criar model `Profile` em `profiles/models.py` com campos: `user` (OneToOne com User), `avatar` (ImageField opcional), `created_at`, `updated_at`
- [X] 1.3.2 — Criar `profiles/signals.py` com signal `post_save` para criar Profile automaticamente ao criar User
- [X] 1.3.3 — Configurar `apps.py` do profiles para carregar signals (método `ready()`)
- [X] 1.3.4 — Registrar model `Profile` no admin
- [X] 1.3.5 — Executar migração (`makemigrations profiles` e `migrate`)

#### T1.4 — Templates base e design system ✅
- [X] 1.4.1 — Criar `templates/base.html` com estrutura HTML5, TailwindCSS CDN, Google Fonts (Inter), meta tags, blocos `{% block title %}`, `{% block content %}`, `{% block extra_css %}`, `{% block extra_js %}`
- [X] 1.4.2 — Criar `templates/components/navbar.html` com logo, links de navegação, dropdown de usuário (para páginas públicas)
- [X] 1.4.3 — Criar `templates/components/sidebar.html` com links de navegação do app (Dashboard, Contas, Categorias, Transações, Perfil), logo e botão de logout
- [X] 1.4.4 — Criar `templates/components/card.html` como template component reutilizável
- [X] 1.4.5 — Criar `templates/components/table.html` como template component reutilizável
- [X] 1.4.6 — Criar `templates/components/form.html` como template component reusável com renderização de campos e erros
- [X] 1.4.7 — Criar `templates/components/pagination.html` como template component reutilizável
- [X] 1.4.8 — Criar `templates/components/alert.html` para mensagens de sucesso/erro/aviso
- [X] 1.4.9 — Criar `templates/components/modal.html` como template component reutilizável
- [X] 1.4.10 — Criar `templates/partials/messages.html` para renderizar mensagens do Django messages framework
- [X] 1.4.11 — Criar `templates/layouts/app.html` que herda de base.html e inclui sidebar + área de conteúdo (layout autenticado)
- [X] 1.4.12 — Criar `templates/layouts/public.html` que herda de base.html e inclui navbar (layout público)

#### T1.5 — Landing page ✅
- [X] 1.5.1 — Criar view `LandingPageView` (TemplateView) em `core/views.py`
- [X] 1.5.2 — Criar `templates/pages/landing.html` com hero section, features, CTA de cadastro e login
- [X] 1.5.3 — Configurar `core/urls.py` com URL `/` apontando para a landing page
- [X] 1.5.4 — Aplicar design system: gradiente no hero, cards de features, tema escuro

#### T1.6 — Autenticação: cadastro, login, logout ✅
- [X] 1.6.1 — Criar `users/forms.py` com `UserRegisterForm` (nome, email, senha, confirmação de senha)
- [X] 1.6.2 — Criar `users/forms.py` com `UserLoginForm` (email, senha, lembrar-me)
- [X] 1.6.3 — Criar `users/views.py` com `RegisterView` (CreateView ou View customizada) para cadastro
- [X] 1.6.4 — Criar `users/views.py` com `LoginView` customizada que usa email
- [X] 1.6.5 — Criar `users/views.py` com `LogoutView`
- [X] 1.6.6 — Criar `templates/pages/register.html` com formulário de cadastro estilizado
- [X] 1.6.7 — Criar `templates/pages/login.html` com formulário de login estilizado
- [X] 1.6.8 — Criar `users/urls.py` com rotas de autenticação (`/register/`, `/login/`, `/logout/`)
- [X] 1.6.9 — Configurar `core/urls.py` incluindo urls de todos os apps
- [X] 1.6.10 — Adicionar decorator `@login_required` ou `LoginRequiredMixin` nas views protegidas

---

### Sprint 2 — Dashboard e Contas bancárias ✅

#### T2.1 — Dashboard base ✅
- [X] 2.1.1 — Criar `dashboard/` ou usar `core/views.py` para a view do dashboard (`DashboardView`)
- [X] 2.1.2 — Criar `templates/pages/dashboard.html` herdando de `layouts/app.html`
- [X] 2.1.3 — Implementar cards de métricas: saldo total, receitas do mês, despesas do mês, saldo do mês
- [X] 2.1.4 — Implementar listagem das 5 transações mais recentes (inicialmente vazio, sem dados)
- [X] 2.1.5 — Implementar listagem de contas com saldos (inicialmente vazio)
- [X] 2.1.6 — Configurar URL `/dashboard/` com nome `dashboard`
- [X] 2.1.7 — Adicionar dados de contexto no dashboard (querysets vazios inicialmente, depois populados)

#### T2.2 — Model Account ✅
- [X] 2.2.1 — Criar model `Account` em `accounts/models.py` com campos: `user` (FK para User), `name` (CharField), `account_type` (CharField com choices: corrente, poupança, carteira, investimento), `balance` (DecimalField), `institution` (CharField, opcional), `color` (CharField, default='#7c3aed'), `is_active` (BooleanField, default=True), `created_at`, `updated_at`
- [X] 2.2.2 — Adicionar `__str__` retornando nome da conta
- [X] 2.2.3 — Adicionar `class Meta` com `ordering = ['-created_at']`
- [X] 2.2.4 — Registrar model `Account` no admin
- [X] 2.2.5 — Executar migração

#### T2.3 — CRUD de Contas ✅
- [X] 2.3.1 — Criar `accounts/forms.py` com `AccountForm` (name, account_type, balance, institution, color)
- [X] 2.3.2 — Criar `AccountListView` (ListView) filtrando por `request.user`
- [X] 2.3.3 — Criar `AccountCreateView` (CreateView) com `form_class` e `success_url`
- [X] 2.3.4 — Criar `AccountUpdateView` (UpdateView) com verificação de proprietário
- [X] 2.3.5 — Criar `AccountDeleteView` (DeleteView) com verificação de proprietário
- [X] 2.3.6 — Criar `templates/accounts/account_list.html` com listagem em cards/grid
- [X] 2.3.7 — Criar `templates/accounts/account_form.html` com formulário estilizado (reutilizar component form.html)
- [X] 2.3.8 — Criar `templates/accounts/account_confirm_delete.html` com modal de confirmação
- [X] 2.3.9 — Configurar `accounts/urls.py` com rotas CRUD (`/contas/`, `/contas/nova/`, `/contas/<id>/editar/`, `/contas/<id>/excluir/`)
- [X] 2.3.10 — Incluir URLs de accounts em `core/urls.py`
- [X] 2.3.11 — Adicionar link "Contas" na sidebar

---

### Sprint 3 — Categorias ✅

#### T3.1 — Model Category ✅
- [X] 3.1.1 — Criar model `Category` em `categories/models.py` com campos: `user` (FK para User), `name` (CharField), `category_type` (CharField com choices: receita, despesa), `color` (CharField, default='#7c3aed'), `icon` (CharField, opcional), `created_at`, `updated_at`
- [X] 3.1.2 — Adicionar `__str__` retornando nome da categoria
- [X] 3.1.3 — Adicionar `class Meta` com `ordering = ['category_type', 'name']` e `unique_together = ('user', 'name')`
- [X] 3.1.4 — Registrar model `Category` no admin
- [X] 3.1.5 — Executar migração

#### T3.2 — Categorias padrão (signal) ✅
- [X] 3.2.1 — Criar `categories/signals.py` com signal `post_save` para criar categorias padrão quando um novo User for criado (ex: Alimentação, Transporte, Salário, Moradia, Lazer, Saúde, Educação, Outros — para despesas; Salário, Freelance, Investimentos, Outros — para receitas)
- [X] 3.2.2 — Configurar `apps.py` do categories para carregar signals
- [X] 3.2.3 — Testar criação de categorias padrão ao registrar novo usuário

#### T3.3 — CRUD de Categorias ✅
- [X] 3.3.1 — Criar `categories/forms.py` com `CategoryForm` (name, category_type, color)
- [X] 3.3.2 — Criar `CategoryListView` (ListView) filtrando por `request.user`
- [X] 3.3.3 — Criar `CategoryCreateView` (CreateView)
- [X] 3.3.4 — Criar `CategoryUpdateView` (UpdateView) com verificação de proprietário
- [X] 3.3.5 — Criar `CategoryDeleteView` (DeleteView) com verificação de proprietário
- [X] 3.3.6 — Criar `templates/categories/category_list.html` com abas de receita/despesa
- [X] 3.3.7 — Criar `templates/categories/category_form.html`
- [X] 3.3.8 — Criar `templates/categories/category_confirm_delete.html`
- [X] 3.3.9 — Configurar `categories/urls.py` com rotas CRUD
- [X] 3.3.10 — Incluir URLs de categories em `core/urls.py`
- [X] 3.3.11 — Adicionar link "Categorias" na sidebar

---

### Sprint 4 — Transações ✅

#### T4.1 — Model Transaction ✅
- [X] 4.1.1 — Criar model `Transaction` em `transactions/models.py` com campos: `user` (FK para User), `account` (FK para Account), `category` (FK para Category), `description` (CharField), `amount` (DecimalField), `transaction_type` (CharField com choices: entrada, saida), `date` (DateField), `created_at`, `updated_at`
- [X] 4.1.2 — Adicionar `__str__` retornando descrição e valor
- [X] 4.1.3 — Adicionar `class Meta` com `ordering = ['-date', '-created_at']`
- [X] 4.1.4 — Registrar model `Transaction` no admin
- [X] 4.1.5 — Executar migração

#### T4.2 — CRUD de Transações ✅
- [X] 4.2.1 — Criar `transactions/forms.py` com `TransactionForm` (description, amount, transaction_type, date, category, account). Filtrar categorias por tipo da transação e por usuário; filtrar contas por usuário
- [X] 4.2.2 — Criar `TransactionListView` (ListView) filtrando por `request.user` com filtros GET (período, tipo, categoria, conta) e busca por descrição
- [X] 4.2.3 — Criar `TransactionCreateView` (CreateView)
- [X] 4.2.4 — Criar `TransactionUpdateView` (UpdateView) com verificação de proprietário
- [X] 4.2.5 — Criar `TransactionDeleteView` (DeleteView) com verificação de proprietário
- [X] 4.2.6 — Criar `templates/transactions/transaction_list.html` com filtros, busca e tabela paginada
- [X] 4.2.7 — Criar `templates/transactions/transaction_form.html`
- [X] 4.2.8 — Criar `templates/transactions/transaction_confirm_delete.html`
- [X] 4.2.9 — Configurar `transactions/urls.py` com rotas CRUD
- [X] 4.2.10 — Incluir URLs de transactions em `core/urls.py`
- [X] 4.2.11 — Adicionar link "Transações" na sidebar

#### T4.3 — Atualização de saldo ao criar/editar/excluir transação ✅
- [X] 4.3.1 — Criar `transactions/signals.py` com signal `post_save` para atualizar saldo da conta ao criar/editar transação
- [X] 4.3.2 — Criar signal `post_delete` para reverter saldo da conta ao excluir transação
- [X] 4.3.3 — Ao editar, calcular diferença entre valor antigo e novo para ajustar saldo
- [X] 4.3.4 — Configurar `apps.py` do transactions para carregar signals

---

### Sprint 5 — Dashboard com dados reais e Perfil ✅

#### T5.1 — Dashboard com dados reais ✅
- [X] 5.1.1 — Atualizar `DashboardView` com queryset de transações do usuário logado
- [X] 5.1.2 — Implementar cálculo de saldo total (soma dos saldos de todas as contas do usuário)
- [X] 5.1.3 — Implementar cálculo de receitas do mês atual
- [X] 5.1.4 — Implementar cálculo de despesas do mês atual
- [X] 5.1.5 — Implementar cálculo de saldo do mês (receitas - despesas)
- [X] 5.1.6 — Implementar listagem das 5 transações mais recentes
- [X] 5.1.7 — Implementar listagem de contas com saldos
- [X] 5.1.8 — Implementar gráfico simples de receitas vs despesas por mês (usando Chart.js via CDN ou barras HTML/CSS)
- [X] 5.1.9 — Refinar visual do dashboard com cards de gradiente e ícones

#### T5.2 — Perfil do usuário ✅
- [X] 5.2.1 — Criar `profiles/forms.py` com `ProfileUpdateForm` (first_name, last_name, email)
- [X] 5.2.2 — Criar `profiles/forms.py` com `PasswordChangeForm` customizada
- [X] 5.2.3 — Criar `ProfileDetailView` (DetailView) para exibir perfil
- [X] 5.2.4 — Criar `ProfileUpdateView` (UpdateView) para editar perfil
- [X] 5.2.5 — Criar `PasswordChangeView` customizada
- [X] 5.2.6 — Criar `templates/profiles/profile_detail.html`
- [X] 5.2.7 — Criar `templates/profiles/profile_form.html`
- [X] 5.2.8 — Criar `templates/profiles/password_change.html`
- [X] 5.2.9 — Configurar `profiles/urls.py` com rotas (`/perfil/`, `/perfil/editar/`, `/perfil/alterar-senha/`)
- [X] 5.2.10 — Incluir URLs de profiles em `core/urls.py`
- [X] 5.2.11 — Adicionar link "Perfil" na sidebar (no dropdown do usuário)

---

### Sprint 6 — Polimento e finalização ✅

#### T6.1 — Polimento visual e UX ✅
- [X] 6.1.1 — Revisar consistência visual de todas as páginas
- [X] 6.1.2 — Adicionar mensagens de feedback (success, error, warning) em todas as operações CRUD usando Django messages framework
- [X] 6.1.3 — Implementar paginação consistente em todas as listagens (ListView com `paginate_by`)
- [X] 6.1.4 — Adicionar estados vazios (empty states) quando não houver dados (ex: "Nenhuma transação registrada. Clique em Nova Transação para começar.")
- [X] 6.1.5 — Adicionar confirmação visual de exclusão com modal em todas as telas de delete (usar component modal.html)
- [X] 6.1.6 — Garantir que todos os formulários exibam erros de validação corretamente
- [X] 6.1.7 — Garantir responsividade mobile em todas as páginas
- [X] 6.1.8 — Adicionar loading states ou feedback visual em formulários submetidos

#### T6.2 — Segurança e proteção de dados ✅
- [X] 6.2.1 — Garantir que todas as views protegidas usam `@login_required` ou `LoginRequiredMixin`
- [X] 6.2.2 — Garantir que todas as queries filtram por `request.user` (isolation)
- [X] 6.2.3 — Garantir que usuários não podem acessar/editar/excluir dados de outros usuários
- [X] 6.2.4 — Revisar CSRF em todos os formulários POST
- [X] 6.2.5 — Adicionar `LOGIN_REQUIRED` em settings para views protegidas

#### T6.3 — Revisão de código e organização ✅
- [X] 6.3.1 — Revisar todos os models para garantir `created_at` e `updated_at`
- [X] 6.3.2 — Revisar que todo código está em inglês
- [X] 6.3.3 — Revisar que toda interface está em português brasileiro
- [X] 6.3.4 — Revisar que o código usa aspas simples (PEP8)
- [X] 6.3.5 — Revisar que todas as CBVs seguem padrão consistente
- [X] 6.3.6 — Limpar imports não utilizados
- [X] 6.3.7 — Verificar relacionamentos no banco (on_delete, related_name)
- [X] 6.3.8 — Revisar `__str__` em todos os models

#### T6.4 — Documentação e configuração final ✅
- [X] 6.4.1 — Atualizar `requirements.txt` com todas as dependências
- [X] 6.4.2 — Atualizar ou criar arquivo `.env.example` com variáveis de ambiente necessárias
- [X] 6.4.3 — Garantir que `manage.py` e migrações estão em dia
- [X] 6.4.4 — Executar `python manage.py check` e corrigir avisos
- [X] 6.4.5 — Executar `python manage.py runserver` e testar todos os fluxos manualmente

---

### Sprint 7 — Testes ✅

#### T7.1 — Testes unitários ✅
- [X] 7.1.1 — Testes do model User (criação, email como campo de login)
- [X] 7.1.2 — Testes do model Account (CRUD, filtros por usuário)
- [X] 7.1.3 — Testes do model Category (CRUD, categorias padrão)
- [X] 7.1.4 — Testes do model Transaction (CRUD, cálculos)
- [X] 7.1.5 — Testes do model Profile (criação automática)

#### T7.2 — Testes de integração e views ✅
- [X] 7.2.1 — Testes de cadastro de usuário (fluxo completo)
- [X] 7.2.2 — Testes de login/logout (fluxo completo)
- [X] 7.2.3 — Testes de CRUD de contas (autenticado)
- [X] 7.2.4 — Testes de CRUD de categorias (autenticado)
- [X] 7.2.5 — Testes de CRUD de transações (autenticado)
- [X] 7.2.6 — Testes de proteção de rotas (não autenticado)

---

### Sprint 8 — Agente de IA Financeiro (LangChain 1.0)

#### T8.1 — Configuração de dependências e variáveis de ambiente ✅
- [X] 8.1.1 — Verificar que `langchain`, `langchain-openai` e `python-dotenv` estão em `requirements.txt` e executar `pip install -r requirements.txt`
- [X] 8.1.2 — Adicionar ao `.env` as variáveis de IA: `OPENAI_API_KEY=sk-...`, `OPENAI_MODEL=gpt-4o-mini`, `AI_MAX_TOKENS=2000`, `AI_TEMPERATURE=0.7`
- [X] 8.1.3 — Atualizar `.env.example` com as variáveis de IA (sem valores reais): `OPENAI_API_KEY=sk-your-openai-api-key-here`, `OPENAI_MODEL=gpt-4o-mini`, `AI_MAX_TOKENS=2000`, `AI_TEMPERATURE=0.7`
- [X] 8.1.4 — Configurar leitura em `settings.py`: `OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')`, `OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')`, `AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '2000'))`, `AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))`
- [X] 8.1.5 — Testar import de `langchain` e `langchain_openai` no shell Django: `python manage.py shell -c "from langchain_openai import ChatOpenAI; print('OK')"`
- [X] 8.1.6 — Verificar que app `ai` está em `INSTALLED_APPS`
- [X] 8.1.7 — Verificar que `.env` está no `.gitignore` (nunca commitar chave real)

#### T8.2 — Estrutura de diretórios da app `ai` ✅
- [X] 8.2.1 — Executar `python manage.py startapp ai` (se ainda não existir)
- [X] 8.2.2 — Criar diretório `ai/agents/` e arquivo `ai/agents/__init__.py`
- [X] 8.2.3 — Criar diretório `ai/tools/` e arquivo `ai/tools/__init__.py`
- [X] 8.2.4 — Criar diretório `ai/services/` e arquivo `ai/services/__init__.py`
- [X] 8.2.5 — Criar diretório `ai/management/` e arquivo `ai/management/__init__.py`
- [X] 8.2.6 — Criar diretório `ai/management/commands/` e arquivo `ai/management/commands/__init__.py`
- [X] 8.2.7 — Criar `ai/apps.py` com configuração adequada e método `ready()`

#### T8.3 — Model AIAnalysis ✅
- [X] 8.3.1 — Criar model `AIAnalysis` em `ai/models.py` com campos: `user` (FK→User, on_delete=CASCADE, related_name='ai_analyses'), `analysis_text` (TextField), `key_insights` (JSONField, default=list), `recommendations` (JSONField, default=list), `period_analyzed` (CharField max_length=100), `model_used` (CharField max_length=50), `tokens_input` (IntegerField, default=0), `tokens_output` (IntegerField, default=0), `is_latest` (BooleanField, default=True), `created_at`, `updated_at`
- [X] 8.3.2 — Adicionar `__str__` retornando `f'{self.user.email} - {self.period_analyzed}'`
- [X] 8.3.3 — Adicionar `class Meta` com `ordering = ['-created_at']`, `verbose_name = 'análise IA'`, `verbose_name_plural = 'análises IA'`
- [X] 8.3.4 — Adicionar indexes em `user` e `created_at`: `indexes = [models.Index(fields=['user', '-created_at']), models.Index(fields=['user', 'is_latest'])]`
- [X] 8.3.5 — Implementar lógica de `is_latest` no `save()`: ao salvar nova análise com `is_latest=True`, setar `is_latest=False` nas análises anteriores do mesmo usuário
- [X] 8.3.6 — Adicionar método `get_latest_for_user(user_id)` como class method: `AIAnalysis.objects.filter(user_id=user_id, is_latest=True).first()`

#### T8.4 — Admin de AIAnalysis ✅
- [X] 8.4.1 — Criar `AIAnalysisAdmin` em `ai/admin.py` com `list_display`: user, period_analyzed, model_used, created_at
- [X] 8.4.2 — Configurar `list_filter`: created_at
- [X] 8.4.3 — Configurar `search_fields`: user__email, analysis_text
- [X] 8.4.4 — Configurar `readonly_fields`: created_at, updated_at, tokens_input, tokens_output
- [X] 8.4.5 — Configurar `date_hierarchy`: created_at
- [X] 8.4.6 — Registrar `AIAnalysis` com `AIAnalysisAdmin`

#### T8.5 — Migration de AIAnalysis ✅
- [X] 8.5.1 — Executar `python manage.py makemigrations ai`
- [X] 8.5.2 — Revisar arquivo de migration gerado
- [X] 8.5.3 — Executar `python manage.py migrate`
- [X] 8.5.4 — Verificar tabela no banco de dados
- [X] 8.5.5 — Testar criação manual de `AIAnalysis` no Django shell

#### T8.6 — LangChain Database Tools ✅
- [X] 8.6.1 — Criar arquivo `ai/tools/database_tools.py`
- [X] 8.6.2 — Importar `@tool` decorator do `langchain_core.tools`
- [X] 8.6.3 — Criar `@tool get_user_transactions(user_id: int, period: str = 'month')` — busca transações dos últimos 30/90/365 dias, retorna lista formatada com data, valor, tipo, categoria, descrição
- [X] 8.6.4 — Criar `@tool get_user_accounts(user_id: int)` — retorna contas com nome, tipo, instituição e saldo
- [X] 8.6.5 — Criar `@tool get_user_categories(user_id: int)` — retorna categorias com nome e tipo
- [X] 8.6.6 — Criar `@tool get_spending_by_category(user_id: int)` — retorna total gasto por categoria nos últimos 30 dias, ordenado do maior para o menor
- [X] 8.6.7 — Criar `@tool get_income_vs_expense(user_id: int)` — retorna total de receitas, despesas e saldo dos últimos 30 dias
- [X] 8.6.8 — Adicionar docstrings detalhadas em cada tool (o agente usa para decidir qual tool chamar)
- [X] 8.6.9 — Adicionar tratamento de exceções em cada tool (retornar string de erro amigável)
- [X] 8.6.10 — Garantir que todas as tools filtram dados por `user_id` (isolamento de dados)
- [X] 8.6.11 — Otimizar queries com `select_related` onde aplicável
- [X] 8.6.12 — Testar tools individualmente no Django shell

#### T8.7 — Agente LangChain (finance_insight_agent)
- [ ] 8.7.1 — Criar arquivo `ai/agents/finance_insight_agent.py`
- [ ] 8.7.2 — Importar `ChatOpenAI` do `langchain_openai`, `create_tool_calling_agent` e `AgentExecutor` do `langchain.agents`, `ChatPromptTemplate` do `langchain_core.prompts`
- [ ] 8.7.3 — Importar tools de `ai.tools.database_tools`
- [ ] 8.7.4 — Configurar ChatOpenAI com `model=settings.OPENAI_MODEL`, `temperature=settings.AI_TEMPERATURE`, `max_tokens=settings.AI_MAX_TOKENS`, `api_key=settings.OPENAI_API_KEY`
- [ ] 8.7.5 — Criar system prompt detalhado: analista financeiro pessoal, responde em pt-BR, estrutura com visão geral, insights, recomendações, alertas
- [ ] 8.7.6 — Criar `ChatPromptTemplate` com system message, user message e placeholder para agent_scratchpad
- [ ] 8.7.7 — Criar agente com `create_tool_calling_agent(llm, tools, prompt)`
- [ ] 8.7.8 — Criar `AgentExecutor` com `agent`, `tools`, `verbose=True`, `handle_parsing_errors=True`
- [ ] 8.7.9 — Criar função `run_analysis(user_id: int) -> dict` que invoca o agente e retorna dict com `analysis_text`, `insights`, `recommendations`
- [ ] 8.7.10 — Adicionar logging de execução (tempo, tokens, usuário)
- [ ] 8.7.11 — Adicionar tratamento de erros: `AuthenticationError`, `RateLimitError`, `APIError` do OpenAI
- [ ] 8.7.12 — Adicionar fallback se API OpenAI falhar (retornar mensagem de erro amigável)

#### T8.8 — Serviço de Análise (analysis_service)
- [ ] 8.8.1 — Criar arquivo `ai/services/analysis_service.py`
- [ ] 8.8.2 — Importar `AIAnalysis`, `get_user_model`, funções do `finance_insight_agent`
- [ ] 8.8.3 — Criar função `generate_analysis_for_user(user_id: int) -> AIAnalysis`
- [ ] 8.8.4 — Validar que usuário existe e está ativo
- [ ] 8.8.5 — Implementar rate limiting: não gerar nova análise se a última for há menos de 24h (configurável)
- [ ] 8.8.6 — Chamar `run_analysis(user_id)` do agente
- [ ] 8.8.7 — Parsear resultado: extrair `analysis_text`, `key_insights`, `recommendations`, `period_analyzed`
- [ ] 8.8.8 — Criar objeto `AIAnalysis` e salvar no banco com `is_latest=True`
- [ ] 8.8.9 — Implementar lógica de `is_latest`: marcar `is_latest=False` nas análises anteriores do mesmo usuário
- [ ] 8.8.10 — Registrar `model_used`, `tokens_input`, `tokens_output` na análise
- [ ] 8.8.11 — Adicionar logging detalhado (início, fim, duração, erros)
- [ ] 8.8.12 — Adicionar tratamento de exceções completo (continuar para próximo usuário em caso de erro)
- [ ] 8.8.13 — Criar função `get_latest_analysis(user_id: int) -> AIAnalysis | None` que retorna a análise mais recente

#### T8.9 — Django Command (run_finance_analysis)
- [ ] 8.9.1 — Criar arquivo `ai/management/commands/run_finance_analysis.py` com `BaseCommand`
- [ ] 8.9.2 — Definir help text descritivo
- [ ] 8.9.3 — Adicionar argumento `--user-email` (opcional) para executar análise para um usuário específico por email
- [ ] 8.9.4 — Adicionar flag `--all` para executar análise para todos os usuários ativos
- [ ] 8.9.5 — Implementar lógica: se `--user-email`, processar apenas esse usuário; se `--all` ou sem argumentos, iterar sobre todos os ativos
- [ ] 8.9.6 — Adicionar output informativo com `self.stdout.write`: "Analisando usuário X...", "Análise concluída", "Erro ao analisar..."
- [ ] 8.9.7 — Adicionar tratamento de erros por usuário (continuar para o próximo em caso de falha)
- [ ] 8.9.8 — Testar comando: `python manage.py run_finance_analysis --user-email test@example.com`
- [ ] 8.9.9 — Testar comando: `python manage.py run_finance_analysis --all`

#### T8.10 — Exibição no Dashboard
- [ ] 8.10.1 — Atualizar `DashboardView` em `core/views.py` para incluir `latest_analysis = AIAnalysis.objects.filter(user=request.user).order_by('-created_at').first()`
- [ ] 8.10.2 — Adicionar `latest_analysis` ao context do template
- [ ] 8.10.3 — Criar seção "Análise Financeira IA" no template do dashboard após as estatísticas
- [ ] 8.10.4 — Verificar `{% if latest_analysis %}` e exibir card com gradiente destacado
- [ ] 8.10.5 — Exibir ícone, título "Sua Análise Financeira Personalizada", data e `analysis_text` formatado
- [ ] 8.10.6 — Se não houver análise, exibir call-to-action informativo
- [ ] 8.10.7 — Estilizar card com TailwindCSS seguindo design system (gradiente violet/indigo)

#### T8.11 — Template do Card de Análise
- [ ] 8.11.1 — Criar parcial `templates/includes/ai_analysis_card.html`
- [ ] 8.11.2 — Receber `analysis` como parâmetro do include
- [ ] 8.11.3 — Criar card com bg-gradient (roxo/azul) seguindo design system
- [ ] 8.11.4 — Header com ícone e título "Sua Análise Financeira Personalizada"
- [ ] 8.11.5 — Data de geração em formato legível (`created_at`)
- [ ] 8.11.6 — Corpo com `analysis_text` formatado (usar `white-space: pre-wrap`)
- [ ] 8.11.7 — Seção de insights destacada (se `key_insights` existir)
- [ ] 8.11.8 — Seção de recomendações destacada (se `recommendations` existir)
- [ ] 8.11.9 — Footer com período analisado (`period_analyzed`) e modelo usado
- [ ] 8.11.10 — Responsividade mobile
- [ ] 8.11.11 — Incluir no dashboard: `{% include 'includes/ai_analysis_card.html' with analysis=latest_analysis %}`

#### T8.12 — View de Detalhe da Análise
- [ ] 8.12.1 — Criar view `AIAnalysisDetailView` (DetailView) em `ai/views.py` com `LoginRequiredMixin`
- [ ] 8.12.2 — Garantir que apenas o dono da análise pode acessá-la (verificar `request.user == obj.user`)
- [ ] 8.12.3 — Criar `templates/ai/analysis_detail.html` herdando de `layouts/app.html`
- [ ] 8.12.4 — Exibir análise completa com `analysis_text`, `key_insights`, `recommendations`, `period_analyzed`, `model_used`, `created_at`
- [ ] 8.12.5 — Criar `ai/urls.py` com `app_name = 'ai'` e rota `path('analise/<int:pk>/', AIAnalysisDetailView.as_view(), name='analysis_detail')`
- [ ] 8.12.6 — Incluir URLs de `ai` em `core/urls.py`
- [ ] 8.12.7 — Adicionar link no card do dashboard para "Ver análise completa"

#### T8.13 — Testes manuais
- [ ] 8.13.1 — Criar usuário de teste com dados financeiros variados (5+ contas, 20+ transações)
- [ ] 8.13.2 — Executar `python manage.py run_finance_analysis --user-email test@example.com`
- [ ] 8.13.3 — Verificar que análise foi gerada no terminal
- [ ] 8.13.4 — Verificar que `AIAnalysis` foi criado no banco (via Django Admin)
- [ ] 8.13.5 — Acessar dashboard e verificar exibição do card de análise
- [ ] 8.13.6 — Verificar formatação e estilo do card
- [ ] 8.13.7 — Tentar gerar nova análise antes de 24h (deve ser impedido pelo rate limiting)
- [ ] 8.13.8 — Testar com usuário sem transações (deve lidar graciosamente com dados vazios)
- [ ] 8.13.9 — Testar comando `--all` com múltiplos usuários
- [ ] 8.13.10 — Verificar logs de execução

#### T8.14 — Segurança e isolamento de dados
- [ ] 8.14.1 — Verificar que `OPENAI_API_KEY` não está em nenhum arquivo versionado (apenas no `.env`)
- [ ] 8.14.2 — Verificar isolamento de dados: todas as tools filtram por `user_id`
- [ ] 8.14.3 — Verificar que prompts não vazam dados de outros usuários
- [ ] 8.14.4 — Adicionar validação de `user_id` em todas as tools (tipo int, usuário ativo)
- [ ] 8.14.5 — Testar que usuário A não acessa análise de usuário B
- [ ] 8.14.6 — Verificar que logs não expõem dados financeiros sensíveis
- [ ] 8.14.7 — Adicionar disclaimer sobre uso de IA (dados enviados à OpenAI)

#### T8.15 — Documentação técnica
- [ ] 8.15.1 — Atualizar `docs/apps.md` com informações da app `ai`
- [ ] 8.15.2 — Atualizar `docs/models.md` com o model `AIAnalysis`
- [ ] 8.15.3 — Atualizar `docs/arquitetura.md` com a app `ai` e diagrama ER
- [ ] 8.15.4 — Atualizar `docs/ai-finance-agent.md` com documentação técnica completa (arquitetura, fluxo, tools, configuração, execução, segurança, troubleshooting)
- [ ] 8.15.5 — Atualizar `docs/README.md` com referência à documentação de IA
- [ ] 8.15.6 — Atualizar `AGENTS.md` com referência ao agente especialista de IA
- [ ] 8.15.7 — Atualizar `agents/README.md` com entrada do `ai_integration_expert`
- [ ] 8.15.8 — Adicionar comando `run_finance_analysis` na documentação com exemplos de uso

---

### Sprint 9 — Docker e Deploy (sprint futura)

#### T9.1 — Containerização
- [ ] 9.1.1 — Criar `Dockerfile` para a aplicação
- [ ] 9.1.2 — Criar `docker-compose.yml` com serviços (app, banco)
- [ ] 9.1.3 — Configurar variáveis de ambiente para produção
- [ ] 9.1.4 — Configurar `requirements.txt` com dependências de produção

#### T9.2 — Deploy
- [ ] 9.2.1 — Configurar `settings.py` para produção (DEBUG=False, ALLOWED_HOSTS, SECRET_KEY do env)
- [ ] 9.2.2 — Configurar coleta de arquivos estáticos (`collectstatic`)
- [ ] 9.2.3 — Configurar WSGI com Gunicorn
- [ ] 9.2.4 — Testar deploy em ambiente de staging