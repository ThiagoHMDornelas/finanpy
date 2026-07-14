from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'category_type', 'color', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
                'placeholder': 'Nome da categoria',
            }),
            'category_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200 appearance-none',
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
            'category_type': 'Tipo',
            'color': 'Cor',
            'is_active': 'Ativa',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category_type = cleaned_data.get('category_type')
        if not name or not category_type or not self.user:
            return cleaned_data
        qs = Category.objects.filter(
            user=self.user,
            name__iexact=name,
            category_type=category_type,
        )
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('name', 'Já existe uma categoria com esse nome e tipo.')
        return cleaned_data
