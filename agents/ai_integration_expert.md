# Agente Especialista em Integracao de IA (ai_integration_expert)

## Proposito

Este documento serve como **guia de referencia tecnica e automacao** para a criacao e integracao de agentes de IA no sistema Finanpy. Ele contem diretrizes, padroes, boas praticas e exemplos para construir agentes com **LangChain 1.0** integrados ao Django.

---

## 1. Diretrizes para criacao de agentes com LangChain 1.0

### 1.1 Estrutura basica de um agente

Todo agente no Finanpy deve seguir esta estrutura:

```python
# ai/agents/finance_insight_agent.py

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from django.conf import settings


llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=settings.AI_TEMPERATURE,
    max_tokens=settings.AI_MAX_TOKENS,
    api_key=settings.OPENAI_API_KEY,
)


@tool
def get_user_transactions(user_id: int, period: str = 'month') -> str:
    '''Busca as transacoes do usuario para um periodo especifico.
    Args:
        user_id: ID do usuario
        period: Periodo de busca - "month", "quarter", "year"
    Returns:
        String com as transacoes formatadas
    '''
    from transactions.models import Transaction
    # ... logica de consulta


prompt = ChatPromptTemplate.from_messages([
    ('system', 'Voce e um analista financeiro pessoal...'),
    ('user', '{input}'),
    ('placeholder', '{agent_scratchpad}'),
])


tools = [get_user_transactions, get_user_accounts, get_user_categories, get_user_summary]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### 1.2 Principios de design

- **Uma responsabilidade por agente**: Cada agente deve ter um proposito claro e definido
- **Tools como funcoes puras**: As tools devem consultar dados e retorna-los como strings — a inteligencia fica no LLM
- **Prompt especializado**: O system prompt deve ser especifico ao dominio (financas pessoais)
- **Resposta em portugues brasileiro**: Todo output gerado deve ser em pt-BR
- **Isolamento por usuario**: Cada analise e por usuario — nunca compartilhar dados entre usuarios

---

## 2. Padroes de integracao com Django

### 2.1 Configuracao de variaveis de ambiente

Todas as chaves e configuracoes da OpenAI ficam no arquivo `.env` (nunca commitado). O `settings.py` le as variaveis com `os.getenv()`.

```python
# core/settings.py
import os
from dotenv import load_dotenv

load_dotenv(BASE_DIR / '.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-5-mini')
AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '2000'))
AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
```

Arquivo `.env`:
```
SECRET_KEY=django-insecure-...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API (agente de IA financeiro)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5-mini
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7
```

Arquivo `.env.example` (referencia para novos desenvolvedores, sem chaves reais):
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API (agente de IA financeiro)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-5-mini
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7
```

**Regras:**
- **Nunca** commitar o arquivo `.env` no repositorio (esta no `.gitignore`)
- O `.env.example` e commitado como referencia, sem chaves reais
- Sempre ler `OPENAI_API_KEY`, `OPENAI_MODEL`, `AI_MAX_TOKENS` e `AI_TEMPERATURE` de `settings.py`, nunca hardcoded no codigo
- O agente usa `settings.OPENAI_MODEL`, `settings.AI_TEMPERATURE`, `settings.AI_MAX_TOKENS` e `settings.OPENAI_API_KEY` — trocar config basta alterar o `.env`

### 2.2 App Django para IA

A app `ai/` e uma app Django padrao, registrada em `INSTALLED_APPS`:

```python
# core/settings.py
INSTALLED_APPS = [
    # ...
    'ai',
]
```

### 2.3 Camada de servico

O padrao recomendado e ter uma **camada de servico** (`services/`) que separa a logica de negócio da logica do agente:

```python
# ai/services/analysis_service.py

from ai.models import AIAnalysis
from ai.agents.finance_insight_agent import agent_executor


class AnalysisService:
    @staticmethod
    def run_for_user(user_id: int) -> AIAnalysis:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.get(pk=user_id)

        result = agent_executor.invoke({
            'input': f'Analise os dados financeiros do usuario {user.first_name} (ID: {user.id})'
        })

        # Desmarcar analises anteriores
        AIAnalysis.objects.filter(user=user, is_latest=True).update(is_latest=False)

        # Criar nova analise
        analysis = AIAnalysis.objects.create(
            user=user,
            analysis_text=result['output'],
            key_insights=result.get('key_insights', []),
            recommendations=result.get('recommendations', []),
            period_analyzed='Ultimos 30 dias',
            model_used=settings.OPENAI_MODEL,
            tokens_input=result.get('tokens_input', 0),
            tokens_output=result.get('tokens_output', 0),
            is_latest=True,
        )

        return analysis
```

### 2.4 Django Command

```python
# ai/management/commands/run_finance_analysis.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ai.services.analysis_service import AnalysisService


class Command(BaseCommand):
    help = 'Executa analise financeira com IA para usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='ID do usuario para analise especifica',
        )

    def handle(self, *args, **options):
        User = get_user_model()

        if options['user_id']:
            users = User.objects.filter(pk=options['user_id'], is_active=True)
        else:
            users = User.objects.filter(is_active=True)

        for user in users:
            self.stdout.write(f'Analisando usuario: {user.email} (ID: {user.id})...')
            try:
                analysis = AnalysisService.run_for_user(user.id)
                self.stdout.write(self.style.SUCCESS(
                    f'Analise concluida para {user.email}'
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Erro ao analisar {user.email}: {str(e)}'
                ))
```

---

## 3. Modelos de configuracao e boas praticas

### 3.1 Configuracao do LLM

| Parametro | Valor padrao | Descricao |
|-----------|-------------|-----------|
| model | settings.OPENAI_MODEL | Modelo configurado via .env (padrao: gpt-5-mini) |
| temperature | settings.AI_TEMPERATURE | Equilibrio criatividade/consistencia (padrao: 0.7) |
| max_tokens | settings.AI_MAX_TOKENS | Limite de tokens na resposta (padrao: 2000) |
| api_key | settings.OPENAI_API_KEY | Chave obtida do .env via settings.py |

### 3.2 Design de prompts

O prompt do sistema deve conter:

1. **Papel**: Definir quem o agente e (ex: "Voce e um analista financeiro pessoal")
2. **Contexto**: Informar que os dados sao pessoais e confidenciais
3. **Instrucoes**: O que o agente deve analisar e como deve responder
4. **Formato**: Estrutura esperada da resposta
5. **Idioma**: Sempre responder em portugues brasileiro

Exemplo:

```python
SYSTEM_PROMPT = '''Voce e um analista financeiro pessoal especializado em financas domesticas brasileiras.

Seu objetivo e analisar os dados financeiros do usuario e fornecer:
1. Um resumo da saude financeira atual
2. Padroes de gastos identificados
3. Dicas praticas de economia
4. Alertas sobre possíveis riscos

Regras:
- Responda SEMPRE em portugues brasileiro
- Use linguagem acessivel e empática
- Base suas analises APENAS nos dados fornecidos
- Seja especifico com numeros e porcentagens
- Formate a resposta em seções claras com titulos

Formato da resposta:
## Resumo Financeiro
[resumo geral]

## Padroes Identificados
[valores e porcentagens]

## Dicas de Economia
[lista de dicas praticas]

## Alertas
[possíveis riscos ou atenções]
'''
```

### 3.3 Boas praticas para tools

```python
from langchain_core.tools import tool


@tool
def get_user_summary(user_id: int) -> str:
    '''Retorna um resumo financeiro consolidado do usuario.
    Inclui total de receitas, despesas e saldo atual.

    Args:
        user_id: ID do usuario no sistema

    Returns:
        String formatada com o resumo financeiro
    '''
    from transactions.models import Transaction
    from accounts.models import Account
    from django.db.models import Sum

    total_receitas = Transaction.objects.filter(
        user_id=user_id,
        transaction_type='entrada'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_despesas = Transaction.objects.filter(
        user_id=user_id,
        transaction_type='saida'
    ).aggregate(total=Sum('amount'))['total'] or 0

    saldo_total = Account.objects.filter(
        user_id=user_id,
        is_active=True
    ).aggregate(total=Sum('balance'))['total'] or 0

    return (
        f'Resumo financeiro do usuario (ID: {user_id}):\n'
        f'- Total de receitas: R$ {total_receitas}\n'
        f'- Total de despesas: R$ {total_despesas}\n'
        f'- Saldo total: R$ {saldo_total}'
    )
```

**Regras para tools:**

1. Sempre retornar strings (o LLM processa texto)
2. Incluir type hints nos argumentos
3. Incluir docstring descritiva (o agente usa para decidir qual tool chamar)
4. Fazer consultas filtradas por `user_id` — **nunca** expor dados de outros usuarios
5. Importar models dentro da funcao para evitar circular imports

---

## 4. Uso do Context7 MCP Server para documentacao do LangChain

O **Context7** e um MCP (Model Context Protocol) Server que fornece acesso a documentacao atualizada do LangChain e outras bibliotecas. Ele deve ser usado sempre que houver duvidas sobre a API do LangChain.

### 4.1 Quando usar

- Ao definir novos agentes ou tools
- Ao atualizar codigo existente para novas versoes do LangChain
- Ao resolver erros de integracao com o LangChain
- Ao implementar novas funcionalidades do LangChain 1.0

### 4.2 Como acessar

O Context7 esta disponivel como ferramenta no ambiente. Para consultar:

1. Resolver o ID da biblioteca: buscar por `LangChain`
2. Consultar documentacao especifica com query detalhada
3. Usar os exemplos de codigo como referencia

### 4.3 Exemplos de queries uteis

- "Como criar um agente ReAct com tools customizadas no LangChain 1.0"
- "Como usar ChatOpenAI com gpt-5-mini no LangChain"
- "Como configurar AgentExecutor com memory no LangChain"
- "Como criar custom tools com decorator @tool no LangChain"

---

## 5. Exemplo de fluxo basico de criacao de um agente integrado

### Passo a passo completo

#### Passo 1: Configurar dependencias

```bash
pip install langchain langchain-openai python-dotenv
```

#### Passo 2: Configurar variavel de ambiente

Adicionar ao `.env`:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5-mini
```

O `.env.example` ja deve conter essas variaveis como referencia (sem valor real): `OPENAI_API_KEY=sk-your-openai-api-key-here`, `OPENAI_MODEL=gpt-5-mini`, `AI_MAX_TOKENS=2000`, `AI_TEMPERATURE=0.7`.

#### Passo 3: Configurar settings.py

```python
import os
from dotenv import load_dotenv

load_dotenv(BASE_DIR / '.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-5-mini')
AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '2000'))
AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
```

#### Passo 4: Criar o modelo AIAnalysis

```python
# ai/models.py

from django.db import models
from django.conf import settings


class AIAnalysis(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_analyses',
    )
    analysis_text = models.TextField()
    key_insights = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    period_analyzed = models.CharField(max_length=100)
    model_used = models.CharField(max_length=50, default='gpt-5-mini')
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    is_latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'analise IA'
        verbose_name_plural = 'analises IA'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_latest']),
        ]

    def __str__(self):
        return f'{self.user.email} - {self.period_analyzed}'
```

#### Passo 5: Criar as tools

```python
# ai/agents/finance_insight_agent.py

from langchain_core.tools import tool


@tool
def get_user_transactions(user_id: int, period: str = 'month') -> str:
    '''Busca as transacoes do usuario para um periodo especifico.
    Args:
        user_id: ID do usuario
        period: "month", "quarter" ou "year"
    '''
    from transactions.models import Transaction
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    if period == 'month':
        start = now - timedelta(days=30)
    elif period == 'quarter':
        start = now - timedelta(days=90)
    else:
        start = now - timedelta(days=365)

    transactions = Transaction.objects.filter(
        user_id=user_id, date__gte=start.date()
    ).order_by('-date')[:50]

    if not transactions.exists():
        return 'Nenhuma transacao encontrada no periodo.'

    result = '\n'.join([
        f'- {t.date} | {t.transaction_type} | {t.description} | R$ {t.amount}'
        for t in transactions
    ])
    return result


@tool
def get_user_accounts(user_id: int) -> str:
    '''Retorna as contas bancarias e saldos do usuario.'''
    from accounts.models import Account

    accounts = Account.objects.filter(user_id=user_id, is_active=True)
    if not accounts.exists():
        return 'Nenhuma conta encontrada.'

    result = '\n'.join([
        f'- {a.name} ({a.account_type}): R$ {a.balance}'
        for a in accounts
    ])
    return result


@tool
def get_user_categories(user_id: int) -> str:
    '''Retorna as categorias do usuario com nome e tipo.'''
    from categories.models import Category

    categories = Category.objects.filter(user_id=user_id)
    if not categories.exists():
        return 'Nenhuma categoria encontrada.'

    result = '\n'.join([
        f'- {c.name} ({c.category_type})'
        for c in categories
    ])
    return result


@tool
def get_user_summary(user_id: int) -> str:
    '''Retorna um resumo financeiro consolidado do usuario.'''
    from transactions.models import Transaction
    from accounts.models import Account
    from django.db.models import Sum

    total_receitas = Transaction.objects.filter(
        user_id=user_id, transaction_type='entrada'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_despesas = Transaction.objects.filter(
        user_id=user_id, transaction_type='saida'
    ).aggregate(total=Sum('amount'))['total'] or 0

    saldo_total = Account.objects.filter(
        user_id=user_id, is_active=True
    ).aggregate(total=Sum('balance'))['total'] or 0

    return (
        f'Resumo financeiro (ID: {user_id}):\n'
        f'- Total receitas: R$ {total_receitas}\n'
        f'- Total despesas: R$ {total_despesas}\n'
        f'- Saldo total contas: R$ {saldo_total}'
    )
```

#### Passo 6: Montar o agente

```python
# ai/agents/finance_insight_agent.py (continuacao)

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings


SYSTEM_PROMPT = '''Voce e um analista financeiro pessoal especializado em financas domesticas brasileiras.

Seu objetivo e analisar os dados financeiros do usuario e fornecer:
1. Um resumo da saude financeira atual
2. Padroes de gastos identificados
3. Dicas praticas de economia
4. Alertas sobre possiveis riscos

Regras:
- Responda SEMPRE em portugues brasileiro
- Use linguagem acessivel e empatica
- Base suas analises APENAS nos dados fornecidos
- Seja especifico com numeros e porcentagens
- Formate a resposta com secoes claras

Formato da resposta:
## Resumo Financeiro
[resumo geral]

## Padroes Identificados
[valores e porcentagens]

## Dicas de Economia
[lista de dicas praticas]

## Alertas
[possiveis riscos ou atencoes]
'''

tools = [get_user_transactions, get_user_accounts, get_user_categories, get_user_summary]

prompt = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_PROMPT),
    ('user', '{input}'),
    ('placeholder', '{agent_scratchpad}'),
])


def create_finance_agent():
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=settings.AI_TEMPERATURE,
        max_tokens=settings.AI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


agent_executor = create_finance_agent()
```

#### Passo 7: Criar o Django Command

```python
# ai/management/commands/run_finance_analysis.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ai.services.analysis_service import AnalysisService


class Command(BaseCommand):
    help = 'Executa analise financeira com IA para usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='ID do usuario para analise especifica',
        )

    def handle(self, *args, **options):
        User = get_user_model()

        if options['user_id']:
            users = User.objects.filter(pk=options['user_id'], is_active=True)
        else:
            users = User.objects.filter(is_active=True)

        for user in users:
            self.stdout.write(f'Analisando usuario: {user.email} (ID: {user.id})...')
            try:
                analysis = AnalysisService.run_for_user(user.id)
                self.stdout.write(self.style.SUCCESS(
                    f'Analise concluida para {user.email}: {analysis.summary}'
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Erro ao analisar {user.email}: {str(e)}'
                ))
```

---

## 6. Tratamento de erros

Sempre tratar falhas de API gracefully:

```python
from openai import APIError, RateLimitError, AuthenticationError


try:
    result = agent_executor.invoke({'input': prompt_text})
except AuthenticationError:
    # Chave de API invalida
    logger.error('Chave de API OpenAI invalida')
    raise
except RateLimitError:
    # Limite de taxa atingido
    logger.warning('Limite de taxa da API atingido, aguardando...')
    time.sleep(60)
    # retry logic
except APIError as e:
    # Erro generico da API
    logger.error(f'Erro na API OpenAI: {str(e)}')
    raise
```

---

## 7. Checklist para novos agentes

Ao criar um novo agente de IA no Finanpy, verifique:

- [ ] As tools consultam dados apenas do usuario autenticado/especificado (isolamento de dados)
- [ ] O prompt do sistema esta em portugues brasileiro
- [ ] As variaveis `OPENAI_API_KEY`, `OPENAI_MODEL`, `AI_MAX_TOKENS` e `AI_TEMPERATURE` estao no `.env` e nao no codigo
- [ ] O agente usa `settings.OPENAI_MODEL`, `settings.AI_TEMPERATURE` e `settings.AI_MAX_TOKENS` (nunca hardcoded)
- [ ] O agente esta importado e configurado no `services/`
- [ ] O Django Command esta documentado com `--help`
- [ ] Os imports de models dentro das tools usam imports locais (evitar circular imports)
- [ ] O `is_latest` e atualizado corretamente ao criar novas analises
- [ ] O `apps.py` configura o metodo `ready()` se houver signals
- [ ] O rate limiting esta implementado (1 analise por usuario a cada 24h)
- [ ] O tratamento de erros da API OpenAI esta implementado (AuthenticationError, RateLimitError, APIError)
- [ ] As ferramentas/tools estao em `ai/tools/` separadas do agente