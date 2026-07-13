import logging
import time

from django.conf import settings

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from openai import APIError, AuthenticationError, RateLimitError

from ai.tools.database_tools import (
    get_income_vs_expense,
    get_spending_by_category,
    get_user_accounts,
    get_user_categories,
    get_user_transactions,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = '''Você é um analista financeiro pessoal especializado em finanças domésticas brasileiras.

Seu objetivo é analisar os dados financeiros do usuário e fornecer uma análise completa contendo:

1. **Visão Geral**: Resumo da saúde financeira atual do usuário
2. **Principais Insights**: Padrões de gastos identificados, destaques positivos e pontos de atenção
3. **Recomendações**: Dicas práticas e personalizadas de economia e organização financeira
4. **Alertas**: Possíveis riscos ou situações que merecem atenção

Regras obrigatórias:
- Responda SEMPRE em português brasileiro, de forma clara e acessível
- Use linguagem empática e construtiva
- Baseie suas análises APENAS nos dados fornecidos pelas ferramentas
- Seja específico com números, valores e porcentagens sempre que possível
- Formate a resposta em seções claras com títulos e parágrafos
- Se houver dados insuficientes para uma análise significativa, informe isso ao usuário

Formato da resposta:

## 📊 Visão Geral
[resumo geral da situação financeira]

## 💡 Principais Insights
[lista dos insights mais relevantes identificados]

## 🎯 Recomendações
[lista de recomendações práticas e personalizadas]

## ⚠️ Alertas
[alertas sobre possíveis riscos ou situações que merecem atenção]
'''

tools = [
    get_user_transactions,
    get_user_accounts,
    get_user_categories,
    get_spending_by_category,
    get_income_vs_expense,
]


def _build_llm():
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=settings.AI_TEMPERATURE,
        max_tokens=settings.AI_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )


def _build_agent(llm):
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


agent = _build_agent(_build_llm())


def run_analysis(user_id: int, user_name: str = '') -> dict:
    logger.info(
        'Iniciando analise financeira para usuario ID=%s (%s)',
        user_id,
        user_name,
    )
    start_time = time.time()

    prompt_text = (
        f'Analise os dados financeiros do usuario {user_name} (ID: {user_id}). '
        f'Consulte as ferramentas disponiveis para obter transacoes, contas, '
        f'categorias, gastos por categoria e comparativo de receitas vs despesas. '
        f'Gere uma analise completa com visao geral, insights, recomendacoes e alertas.'
    )

    try:
        result = agent.invoke({'messages': [{'role': 'user', 'content': prompt_text}]})

        elapsed = time.time() - start_time
        logger.info(
            'Analise concluida para usuario ID=%s em %.2fs',
            user_id,
            elapsed,
        )

        output_messages = result.get('messages', [])
        analysis_text = ''
        if output_messages:
            last = output_messages[-1]
            if hasattr(last, 'content'):
                analysis_text = last.content

        return {
            'analysis_text': analysis_text,
            'insights': [],
            'recommendations': [],
        }

    except AuthenticationError:
        logger.error('Chave de API OpenAI invalida ao analisar usuario ID=%s', user_id)
        return {
            'analysis_text': (
                'Não foi possível realizar a análise financeira no momento. '
                'O serviço de IA está com problemas de autenticação. '
                'Entre em contato com o suporte.'
            ),
            'insights': [],
            'recommendations': [],
        }

    except RateLimitError:
        logger.warning('Limite de taxa da API OpenAI atingido para usuario ID=%s', user_id)
        return {
            'analysis_text': (
                'A análise financeira não pôde ser concluída devido a '
                'limitações de taxa do serviço de IA. Tente novamente em alguns minutos.'
            ),
            'insights': [],
            'recommendations': [],
        }

    except APIError as e:
        logger.error('Erro na API OpenAI para usuario ID=%s: %s', user_id, str(e))
        return {
            'analysis_text': (
                'Ocorreu um erro ao comunicar com o serviço de IA. '
                'Tente novamente mais tarde.'
            ),
            'insights': [],
            'recommendations': [],
        }

    except Exception as e:
        logger.error(
            'Erro inesperado na analise do usuario ID=%s: %s',
            user_id,
            str(e),
            exc_info=True,
        )
        return {
            'analysis_text': (
                'Ocorreu um erro inesperado durante a análise financeira. '
                'Tente novamente mais tarde.'
            ),
            'insights': [],
            'recommendations': [],
        }
