from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'account_type', 'balance', 'institution', 'color', 'is_active')
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
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded bg-[#0f0d1a] border-[#2d2754] text-violet-500 focus:ring-violet-500 focus:ring-offset-0 transition-all duration-200',
            }),
        }
        labels = {
            'name': 'Nome',
            'account_type': 'Tipo',
            'balance': 'Saldo inicial',
            'institution': 'Instituição',
            'color': 'Cor',
            'is_active': 'Ativa',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['institution'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name or not self.user:
            return cleaned_data
        qs = Account.objects.filter(
            user=self.user,
            name__iexact=name,
        )
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('name', 'Já existe uma conta com esse nome.')
        return cleaned_data
