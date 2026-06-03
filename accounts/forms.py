from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'account_type', 'balance', 'institution', 'color')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': 'Nome da conta',
            }),
            'account_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200 appearance-none',
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': 'Nome da instituição (opcional)',
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'type': 'color',
            }),
        }
        labels = {
            'name': 'Nome',
            'account_type': 'Tipo',
            'balance': 'Saldo inicial',
            'institution': 'Instituição',
            'color': 'Cor',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].required = False