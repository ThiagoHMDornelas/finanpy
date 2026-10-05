from datetime import timedelta
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from ai.agents.finance_insight_agent import (
    _extract_section_items,
    _extract_token_usage,
    run_analysis,
)
from ai.models import AIAnalysis
from ai.services.analysis_service import generate_analysis_for_user
from users.models import User


class AIAnalysisModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='ai@example.com',
            password='testpass123',
            first_name='Ai',
        )

    def _create(self, **kwargs):
        defaults = {
            'user': self.user,
            'analysis_text': 'Analise de teste',
            'period_analyzed': 'Ultimos 30 dias',
            'is_latest': True,
        }
        defaults.update(kwargs)
        return AIAnalysis.objects.create(**defaults)

    def test_str(self):
        analysis = self._create()
        self.assertIn(self.user.email, str(analysis))
        self.assertIn('Ultimos 30 dias', str(analysis))

    def test_ordering_most_recent_first(self):
        first = self._create(analysis_text='Primeira')
        second = self._create(analysis_text='Segunda')
        AIAnalysis.objects.filter(pk=first.pk).update(
            created_at=timezone.now() - timedelta(hours=1),
        )
        self.assertEqual(AIAnalysis.objects.first(), second)

    def test_new_analysis_marks_previous_as_not_latest(self):
        first = self._create()
        second = self._create()
        first.refresh_from_db()
        self.assertFalse(first.is_latest)
        self.assertTrue(second.is_latest)

    def test_get_latest_for_user(self):
        self._create()
        latest = self._create(analysis_text='Mais recente')
        self.assertEqual(AIAnalysis.get_latest_for_user(self.user.id), latest)

    def test_get_latest_for_user_sem_analise(self):
        self.assertIsNone(AIAnalysis.get_latest_for_user(self.user.id))


class AnalysisServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='svc@example.com',
            password='testpass123',
            first_name='Svc',
        )

    @patch('ai.services.analysis_service.run_analysis')
    def test_generate_creates_analysis(self, mock_run):
        mock_run.return_value = {
            'analysis_text': 'Texto gerado',
            'insights': [],
            'recommendations': [],
        }
        analysis = generate_analysis_for_user(self.user.id)
        self.assertEqual(analysis.analysis_text, 'Texto gerado')
        self.assertTrue(analysis.is_latest)
        mock_run.assert_called_once()

    @patch('ai.services.analysis_service.run_analysis')
    def test_rate_limit_blocks_recent_analysis(self, mock_run):
        AIAnalysis.objects.create(
            user=self.user,
            analysis_text='Recente',
            period_analyzed='Ultimos 30 dias',
            is_latest=True,
        )
        with self.assertRaises(ValueError):
            generate_analysis_for_user(self.user.id)
        mock_run.assert_not_called()

    @patch('ai.services.analysis_service.run_analysis')
    def test_rate_limit_allows_after_24h(self, mock_run):
        old = AIAnalysis.objects.create(
            user=self.user,
            analysis_text='Antiga',
            period_analyzed='Ultimos 30 dias',
            is_latest=True,
        )
        AIAnalysis.objects.filter(pk=old.pk).update(
            created_at=timezone.now() - timedelta(hours=25),
        )
        mock_run.return_value = {
            'analysis_text': 'Nova',
            'insights': [],
            'recommendations': [],
        }
        analysis = generate_analysis_for_user(self.user.id)
        self.assertEqual(analysis.analysis_text, 'Nova')

    def test_user_not_found_raises(self):
        with self.assertRaises(ValueError):
            generate_analysis_for_user(999999)

    def test_inactive_user_raises(self):
        self.user.is_active = False
        self.user.save()
        with self.assertRaises(ValueError):
            generate_analysis_for_user(self.user.id)


SAMPLE_ANALYSIS = (
    '## 📊 Visão Geral\nResumo geral.\n\n'
    '## 💡 Principais Insights\n'
    '- Gasto alto com alimentação\n'
    '- Receita estável\n\n'
    '## 🎯 Recomendações\n'
    '1. Reduzir delivery\n'
    '2. Reservar 10% da renda\n\n'
    '## ⚠️ Alertas\n- Saldo apertado\n'
)


class AgentOutputParsingTest(SimpleTestCase):
    def test_extract_insights(self):
        self.assertEqual(
            _extract_section_items(SAMPLE_ANALYSIS, 'Insight'),
            ['Gasto alto com alimentação', 'Receita estável'],
        )

    def test_extract_recommendations(self):
        self.assertEqual(
            _extract_section_items(SAMPLE_ANALYSIS, 'Recomenda'),
            ['Reduzir delivery', 'Reservar 10% da renda'],
        )

    def test_extract_absent_section_returns_empty(self):
        self.assertEqual(_extract_section_items('sem secoes', 'Insight'), [])

    def test_extract_token_usage(self):
        class Msg:
            def __init__(self, inp, out):
                self.usage_metadata = {'input_tokens': inp, 'output_tokens': out}

        self.assertEqual(_extract_token_usage([Msg(10, 5), Msg(3, 2)]), (13, 7))

    def test_extract_token_usage_sem_metadados(self):
        class Msg:
            usage_metadata = None

        self.assertEqual(_extract_token_usage([Msg()]), (0, 0))

    def test_run_analysis_parses_output_and_tokens(self):
        class FakeMessage:
            content = SAMPLE_ANALYSIS
            usage_metadata = {'input_tokens': 12, 'output_tokens': 8}

        class FakeAgent:
            def invoke(self, payload):
                return {'messages': [FakeMessage()]}

        with patch('ai.agents.finance_insight_agent._get_agent', return_value=FakeAgent()):
            result = run_analysis(user_id=1, user_name='Teste')

        self.assertEqual(result['analysis_text'], SAMPLE_ANALYSIS)
        self.assertEqual(result['insights'], ['Gasto alto com alimentação', 'Receita estável'])
        self.assertEqual(result['recommendations'], ['Reduzir delivery', 'Reservar 10% da renda'])
        self.assertEqual(result['tokens_input'], 12)
        self.assertEqual(result['tokens_output'], 8)
