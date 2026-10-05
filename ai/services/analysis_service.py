import logging

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from ai.agents.finance_insight_agent import run_analysis
from ai.models import AIAnalysis

logger = logging.getLogger(__name__)

RATE_LIMIT_HOURS = 24


def generate_analysis_for_user(user_id: int) -> AIAnalysis:
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id, is_active=True)
    except User.DoesNotExist:
        logger.warning('Usuario ID=%s nao encontrado ou inativo', user_id)
        raise ValueError(f'Usuario ID {user_id} nao encontrado ou inativo.')

    latest = AIAnalysis.get_latest_for_user(user.id)
    if latest:
        time_since_last = timezone.now() - latest.created_at
        if time_since_last < timedelta(hours=RATE_LIMIT_HOURS):
            remaining = timedelta(hours=RATE_LIMIT_HOURS) - time_since_last
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            raise ValueError(
                f'A ultima analise foi ha menos de {RATE_LIMIT_HOURS}h. '
                f'Aguarde aproximadamente {hours}h{minutes}min para gerar uma nova analise.'
            )

    logger.info('Gerando analise financeira para usuario ID=%s', user.id)

    try:
        result = run_analysis(user_id=user.id, user_name=user.get_full_name() or user.email)

        analysis_text = result.get('analysis_text', '')
        insights = result.get('insights', [])
        recommendations = result.get('recommendations', [])

        analysis = AIAnalysis.objects.create(
            user=user,
            analysis_text=analysis_text,
            key_insights=insights,
            recommendations=recommendations,
            period_analyzed='Últimos 30 dias',
            model_used=settings.OPENAI_MODEL,
            tokens_input=result.get('tokens_input', 0),
            tokens_output=result.get('tokens_output', 0),
            is_latest=True,
        )

        logger.info(
            'Analise ID=%s criada para usuario ID=%s',
            analysis.id,
            user.id,
        )

        return analysis

    except ValueError:
        raise

    except Exception as e:
        logger.error(
            'Erro ao gerar analise para usuario ID=%s: %s',
            user.id,
            str(e),
            exc_info=True,
        )
        raise


def get_latest_analysis(user_id: int) -> AIAnalysis | None:
    return AIAnalysis.get_latest_for_user(user_id)
