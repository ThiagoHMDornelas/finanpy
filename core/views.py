from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone

from accounts.models import Account
from ai.models import AIAnalysis
from transactions.models import Transaction


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

        transactions_month = Transaction.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month,
        )

        monthly_income = transactions_month.filter(
            transaction_type='entrada',
        ).aggregate(total=Sum('amount'))['total'] or 0

        monthly_expense = transactions_month.filter(
            transaction_type='saida',
        ).aggregate(total=Sum('amount'))['total'] or 0

        monthly_balance = monthly_income - monthly_expense

        recent_transactions = Transaction.objects.filter(
            user=user,
        ).select_related('account', 'category')[:5]

        monthly_data = []
        for i in range(5, -1, -1):
            month_date = today - timedelta(days=30 * i)
            month_trans = Transaction.objects.filter(
                user=user,
                date__year=month_date.year,
                date__month=month_date.month,
            )
            income = month_trans.filter(
                transaction_type='entrada',
            ).aggregate(total=Sum('amount'))['total'] or 0
            expense = month_trans.filter(
                transaction_type='saida',
            ).aggregate(total=Sum('amount'))['total'] or 0
            monthly_data.append({
                'month': month_date.strftime('%b/%y'),
                'income': float(income),
                'expense': float(expense),
            })

        max_value = max(
            max(d['income'] for d in monthly_data),
            max(d['expense'] for d in monthly_data),
            1,
        )
        for d in monthly_data:
            d['income_pct'] = int((d['income'] / max_value) * 100) if max_value else 0
            d['expense_pct'] = int((d['expense'] / max_value) * 100) if max_value else 0

        context['total_balance'] = total_balance
        context['monthly_income'] = monthly_income
        context['monthly_expense'] = monthly_expense
        context['monthly_balance'] = monthly_balance
        context['recent_transactions'] = recent_transactions
        context['accounts'] = accounts
        context['monthly_data'] = monthly_data

        context['latest_analysis'] = AIAnalysis.get_latest_for_user(user.id)

        return context
