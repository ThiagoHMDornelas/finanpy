from datetime import date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.models import Account
from ai.models import AIAnalysis
from transactions.models import Transaction


def _month_start(reference, offset):
    '''Primeiro dia do mes, deslocado por "offset" meses (negativo = passado).'''
    index = reference.year * 12 + (reference.month - 1) + offset
    return date(index // 12, index % 12 + 1, 1)


class LandingPageView(TemplateView):
    template_name = 'pages/landing.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        current_start = timezone.now().date().replace(day=1)
        first_start = _month_start(current_start, -5)

        accounts = list(Account.objects.filter(user=user, is_active=True))
        total_balance = sum((account.balance for account in accounts), Decimal('0'))

        grouped = (
            Transaction.objects.filter(user=user, date__gte=first_start)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                income=Sum('amount', filter=Q(transaction_type='entrada')),
                expense=Sum('amount', filter=Q(transaction_type='saida')),
            )
        )
        by_month = {
            (row['month'].year, row['month'].month): (
                float(row['income'] or 0),
                float(row['expense'] or 0),
            )
            for row in grouped
        }

        monthly_data = []
        for offset in range(-5, 1):
            month_start = _month_start(current_start, offset)
            income, expense = by_month.get((month_start.year, month_start.month), (0.0, 0.0))
            monthly_data.append({
                'month': month_start.strftime('%b/%y'),
                'income': income,
                'expense': expense,
            })

        max_value = max(
            max(item['income'] for item in monthly_data),
            max(item['expense'] for item in monthly_data),
            1,
        )
        for item in monthly_data:
            item['income_pct'] = int((item['income'] / max_value) * 100)
            item['expense_pct'] = int((item['expense'] / max_value) * 100)

        monthly_income = monthly_data[-1]['income']
        monthly_expense = monthly_data[-1]['expense']

        recent_transactions = Transaction.objects.filter(
            user=user,
        ).select_related('account', 'category')[:5]

        context['total_balance'] = total_balance
        context['monthly_income'] = monthly_income
        context['monthly_expense'] = monthly_expense
        context['monthly_balance'] = monthly_income - monthly_expense
        context['recent_transactions'] = recent_transactions
        context['accounts'] = accounts
        context['monthly_data'] = monthly_data
        context['latest_analysis'] = AIAnalysis.get_latest_for_user(user.id)

        return context
