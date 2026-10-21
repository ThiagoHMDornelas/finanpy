# AGENTS.md — finanpy

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
Sistema de **gestão de finanças pessoais** em Django, com agente de IA (LangChain/LangGraph) para análise dos lançamentos. Existe um `PRD.md` na raiz — consultar antes de implementar features.

**Stack:** Django 5.2.14 · Python 3.11 · LangChain 1.x + LangGraph · SQLite · OpenAI · Docker

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `core/` — projeto Django (`core/settings.py`)
- `accounts/`, `users/`, `profiles/` — autenticação e perfil
- `categories/`, `transactions/` — domínio financeiro
- `ai/` — agente de análise (LangChain + OpenAI)
- `PRD.md` — requisitos do produto

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Testes e lint
```bash
python manage.py test
flake8
```

## Particularidades
- Login é por **email**; `first_name` é obrigatório na criação do usuário.
- Superusuário automatizado via `DJANGO_SUPERUSER_EMAIL/FIRST_NAME/PASSWORD` (`createsuperuser --noinput`).
- Sem `OPENAI_API_KEY` o módulo de análise por IA fica indisponível (o resto funciona).
- No Docker, o caminho do SQLite pode ser ajustado por `SQLITE_PATH`.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
