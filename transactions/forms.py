from django import forms

from .models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('description', 'amount', 'transaction_type', 'date', 'category', 'account')
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': 'Descricao da transacao',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200 appearance-none',
                'id': 'id_transaction_type',
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'type': 'date',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200 appearance-none',
                'id': 'id_category',
            }),
            'account': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200 appearance-none',
            }),
        }
        labels = {
            'description': 'Descricao',
            'amount': 'Valor',
            'transaction_type': 'Tipo',
            'date': 'Data',
            'category': 'Categoria',
            'account': 'Conta',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']

        if self.user:
            self.fields['account'].queryset = Account.objects.filter(user=self.user, is_active=True)
            self.fields['category'].queryset = Category.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')

        if transaction_type and category:
            category_map = {'entrada': 'receita', 'saida': 'despesa'}
            expected_type = category_map.get(transaction_type)
            if expected_type and category.category_type != expected_type:
                self.add_error(
                    'category',
                    f'Selecione uma categoria do tipo {"Receita" if transaction_type == "entrada" else "Despesa"}.'
                )

        return cleaned_data