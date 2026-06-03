# Padroes de Codigo

## Regras gerais

- Codigo em **ingles** (variaveis, funcoes, classes, comentarios)
- Interface do usuario em **portugues brasileiro**
- Usar **aspas simples** sempre que possivel
- Seguir **PEP8**
- Sem over engineering: usar recursos nativos do Django
- Sem Docker inicialmente
- Sem testes inicialmente

## Nomenclatura

| Elemento | Padrao | Exemplo |
|----------|--------|---------|
| Model | PascalCase | `Account`, `Transaction` |
| View (classe) | PascalCase + sufixo View | `AccountListView`, `DashboardView` |
| Campo de model | snake_case | `account_type`, `created_at` |
| Variavel | snake_case | `total_balance`, `user_transactions` |
| Funcao/metodo | snake_case | `get_context_data`, `form_valid` |
| Template | snake_case | `account_list.html`, `transaction_form.html` |
| URL | kebab-case ou snake_case | `/contas/nova/`, `/perfil/editar/` |
| App | snake_case | `accounts`, `categories` |
| Arquivo Python | snake_case | `forms.py`, `signals.py` |

## Models

- Todo model deve ter campos `created_at` e `updated_at`:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

- Todo model deve ter `__str__` definido
- Todo model deve ter `class Meta` com `ordering`
- Relacionamentos FK devem usar `on_delete=models.CASCADE` e `related_name`

## Views

- Usar **Class Based Views (CBV)** sempre que possivel
-ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
- Toda view protegida usa `LoginRequiredMixin`
- Filtrar querysets por `request.user`

```python
class AccountListView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
```

## Forms

- Usar `ModelForm` do Django
- Definir `fields` ou `exclude` explicitamente
- Filtrar choices de FK por usuario no `__init__`

```python
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance', 'institution', 'color']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
```

## URLs

- Um arquivo `urls.py` por app
- Incluir em `core/urls.py` com `include()`
- Usar `app_name` para namespacing

```python
# accounts/urls.py
app_name = 'accounts'
urlpatterns = [
    path('', AccountListView.as_view(), name='list'),
    path('nova/', AccountCreateView.as_view(), name='create'),
]
```

## Signals

- Signals ficam em arquivo `signals.py` dentro da app
- Configurar `apps.py` com metodo `ready()` para carregar signals

```python
# profiles/apps.py
class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals
```

## Templates

- Herdar de `base.html` ou layouts
- Usar `{% block %}` para sobreposicao
- Reutilizar components com `{% include %}`
- Texto visivel ao usuario em **portugues brasileiro**

```html
{% extends 'layouts/app.html' %}
{% block title %}Contas - Finanpy{% endblock %}
{% block content %}
  <!-- conteudo -->
{% endblock %}
```

## Admin

- Registrar todos os models no `admin.py` da app correspondente
- Usar `ModelAdmin` com `list_display`, `list_filter`, `search_fields`

## Mensagens

- Usar Django messages framework para feedback
- Tags: `success`, `error`, `warning`, `info`

```python
from django.contrib import messages

messages.success(request, 'Conta criada com sucesso.')
messages.error(request, 'Ocorreu um erro.')
```