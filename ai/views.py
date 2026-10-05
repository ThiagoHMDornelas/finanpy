import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from ai.exceptions import AIAnalysisError
from ai.models import AIAnalysis

logger = logging.getLogger(__name__)


class AIAnalysisDetailView(LoginRequiredMixin, DetailView):
    model = AIAnalysis
    template_name = 'ai/analysis_detail.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        return AIAnalysis.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj


class GenerateAnalysisView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not settings.OPENAI_API_KEY:
            messages.error(
                request,
                'A análise com IA não está configurada. Defina a variável OPENAI_API_KEY.',
            )
            return redirect('dashboard')

        from ai.services.analysis_service import generate_analysis_for_user

        try:
            analysis = generate_analysis_for_user(request.user.id)
        except ValueError as e:
            messages.warning(request, str(e))
            return redirect('dashboard')
        except AIAnalysisError as e:
            messages.error(request, str(e))
            return redirect('dashboard')
        except Exception:
            logger.exception(
                'Erro ao gerar analise via interface para usuario ID=%s',
                request.user.id,
            )
            messages.error(
                request,
                'Não foi possível gerar a análise no momento. Tente novamente mais tarde.',
            )
            return redirect('dashboard')

        messages.success(request, 'Análise financeira gerada com sucesso!')
        return redirect('ai:analysis_detail', pk=analysis.pk)
