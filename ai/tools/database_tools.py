from langchain_core.tools import tool


@tool
def get_user_transactions(user_id: int, period: str = 'month') -> str:
    '''Busca as transacoes do usuario para um periodo especifico.
    Retorna uma lista formatada com data, tipo, categoria, descricao e valor.

    Args:
        user_id: ID do usuario no sistema
        period: Periodo de busca - "month" (30 dias), "quarter" (90 dias), "year" (365 dias)

    Returns:
        String formatada com as transacoes do periodo
    '''
    try:
        from transactions.models import Transaction
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        period_days = {'month': 30, 'quarter': 90, 'year': 365}
        days = period_days.get(period, 30)
        start_date = now - timedelta(days=days)

        transactions = Transaction.objects.filter(
            user_id=user_id,
            date__gte=start_date.date(),
        ).select_related('category', 'account').order_by('-date')[:50]

        if not transactions.exists():
            return f'Nenhuma transacao encontrada nos ultimos {days} dias.'

        lines = []
        for t in transactions:
            lines.append(
                f'- {t.date} | {t.get_transaction_type_display()} | '
                f'{t.category.name} | {t.description} | R$ {t.amount}'
            )
        return '\n'.join(lines)

    except Exception as e:
        return f'Erro ao buscar transacoes: {str(e)}'


@tool
def get_user_accounts(user_id: int) -> str:
    '''Retorna as contas bancarias do usuario com nome, tipo, instituicao e saldo.

    Args:
        user_id: ID do usuario no sistema

    Returns:
        String formatada com as contas ativas do usuario
    '''
    try:
        from accounts.models import Account

        accounts = Account.objects.filter(
            user_id=user_id,
            is_active=True,
        )

        if not accounts.exists():
            return 'Nenhuma conta encontrada para o usuario.'

        lines = []
        for a in accounts:
            lines.append(
                f'- {a.name} ({a.get_account_type_display()}) | '
                f'Instituicao: {a.institution or "N/A"} | Saldo: R$ {a.balance}'
            )
        return '\n'.join(lines)

    except Exception as e:
        return f'Erro ao buscar contas: {str(e)}'


@tool
def get_user_categories(user_id: int) -> str:
    '''Retorna as categorias do usuario com nome e tipo (receita ou despesa).

    Args:
        user_id: ID do usuario no sistema

    Returns:
        String formatada com as categorias do usuario
    '''
    try:
        from categories.models import Category

        categories = Category.objects.filter(user_id=user_id)

        if not categories.exists():
            return 'Nenhuma categoria encontrada para o usuario.'

        lines = []
        for c in categories:
            lines.append(f'- {c.name} ({c.get_category_type_display()})')
        return '\n'.join(lines)

    except Exception as e:
        return f'Erro ao buscar categorias: {str(e)}'


@tool
def get_spending_by_category(user_id: int) -> str:
    '''Retorna o total gasto por categoria nos ultimos 30 dias, ordenado do maior para o menor.
    Apenas despesas (saidas).

    Args:
        user_id: ID do usuario no sistema

    Returns:
        String formatada com os gastos por categoria
    '''
    try:
        from transactions.models import Transaction
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        start_date = now - timedelta(days=30)

        transactions = Transaction.objects.filter(
            user_id=user_id,
            transaction_type='saida',
            date__gte=start_date.date(),
        ).select_related('category')

        if not transactions.exists():
            return 'Nenhuma despesa encontrada nos ultimos 30 dias.'

        spending = {}
        for t in transactions:
            cat_name = t.category.name if t.category else 'Sem categoria'
            spending[cat_name] = spending.get(cat_name, 0) + t.amount

        sorted_spending = sorted(spending.items(), key=lambda x: x[1], reverse=True)

        lines = []
        for cat, total in sorted_spending:
            lines.append(f'- {cat}: R$ {total}')
        return '\n'.join(lines)

    except Exception as e:
        return f'Erro ao buscar gastos por categoria: {str(e)}'


@tool
def get_income_vs_expense(user_id: int) -> str:
    '''Retorna o total de receitas, despesas e saldo dos ultimos 30 dias.

    Args:
        user_id: ID do usuario no sistema

    Returns:
        String formatada com receitas, despesas e saldo
    '''
    try:
        from transactions.models import Transaction
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        start_date = now - timedelta(days=30)

        transactions = Transaction.objects.filter(
            user_id=user_id,
            date__gte=start_date.date(),
        )

        total_income = sum(
            t.amount for t in transactions.filter(transaction_type='entrada')
        )
        total_expense = sum(
            t.amount for t in transactions.filter(transaction_type='saida')
        )
        balance = total_income - total_expense

        return (
            f'Resumo financeiro dos ultimos 30 dias (ID: {user_id}):\n'
            f'- Total de receitas: R$ {total_income}\n'
            f'- Total de despesas: R$ {total_expense}\n'
            f'- Saldo: R$ {balance}'
        )

    except Exception as e:
        return f'Erro ao buscar receitas vs despesas: {str(e)}'