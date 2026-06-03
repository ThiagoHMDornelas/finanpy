from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone

from accounts.models import Account


class LandingPageView(TemplateView):
    template_name = 'pages/landing.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year

        accounts = Account.objects.filter(user=user, is_active=True)
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0

        context['total_balance'] = total_balance
        context['monthly_income'] = 0
        context['monthly_expense'] = 0
        context['monthly_balance'] = 0
        context['recent_transactions'] = []
        context['accounts'] = accounts
        return context