# Models

Definicao dos models planejados para o projeto Finanpy. Todos os models possuem campos `created_at` e `updated_at`.

## Diagrama de relacionamentos

```mermaid
erDiagram
    User ||--o|| Profile : has
    User ||--o{ Account : owns
    User ||--o{ Category : owns
    User ||--o{ Transaction : creates
    User ||--o{ AIAnalysis : generates
    Account ||--o{ Transaction : has
    Category ||--o{ Transaction : belongs_to

    User {
        int id PK
        string email UK
        string password
        string first_name
        string last_name
        boolean is_active
        boolean is_staff
        datetime created_at
        datetime updated_at
    }

    Profile {
        int id PK
        int user_id FK
        string avatar
        datetime created_at
        datetime updated_at
    }

    Account {
        int id PK
        int user_id FK
        string name
        string account_type
        decimal balance
        string institution
        string color
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    Category {
        int id PK
        int user_id FK
        string name
        string category_type
        string color
        string icon
        datetime created_at
        datetime updated_at
    }

    Transaction {
        int id PK
        int user_id FK
        int account_id FK
        int category_id FK
        string description
        decimal amount
        string transaction_type
        date date
        datetime created_at
        datetime updated_at
    }

    AIAnalysis {
        int id PK
        int user_id FK
        string analysis_text
        list key_insights
        list recommendations
        string period_analyzed
        string model_used
        int tokens_input
        int tokens_output
        boolean is_latest
        datetime created_at
        datetime updated_at
    }
```

## User (users app)

Model customizado que herda de `AbstractUser`.

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| email | EmailField | unique, USERNAME_FIELD |
| password | CharField | hasheado |
| first_name | CharField | obrigatorio (REQUIRED_FIELDS) |
| last_name | CharField | opcional |
| is_active | BooleanField | default=True |
| is_staff | BooleanField | default=False |
| username | CharField | blank=True, null=True (nao usado para login) |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- `USERNAME_FIELD = 'email'`
- `REQUIRED_FIELDS = ['first_name']`
- `UserManager` customizado com `create_user` e `create_superuser`

## Profile (profiles app)

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| user | OneToOneField(User) | on_delete=CASCADE, related_name='profile' |
| avatar | ImageField | blank=True, null=True, upload to 'avatars/' |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- Criado automaticamente via signal `post_save` quando um User e criado

## Account (accounts app)

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| user | ForeignKey(User) | on_delete=CASCADE, related_name='accounts' |
| name | CharField | max_length=100 |
| account_type | CharField | max_length=20, choices: corrente/poupanca/carteira/investimento |
| balance | DecimalField | max_digits=12, decimal_places=2, default=0 |
| institution | CharField | max_length=100, blank=True |
| color | CharField | max_length=7, default='#7c3aed' |
| is_active | BooleanField | default=True |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- `Meta.ordering = ['-created_at']`
- `__str__` retorna `self.name`

### Choices de account_type

| Valor | Label |
|-------|-------|
| corrente | Conta Corrente |
| poupanca | Poupanca |
| carteira | Carteira |
| investimento | Investimento |

## Category (categories app)

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| user | ForeignKey(User) | on_delete=CASCADE, related_name='categories' |
| name | CharField | max_length=100 |
| category_type | CharField | max_length=10, choices: receita/despesa |
| color | CharField | max_length=7, default='#7c3aed' |
| icon | CharField | max_length=50, blank=True |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- `Meta.ordering = ['category_type', 'name']`
- `Meta.unique_together = ('user', 'name')`

### Categorias padrao (criadas por signal)

**Despesas:** Alimentacao, Transporte, Moradia, Lazer, Saude, Educacao, Outros
**Receitas:** Salario, Freelance, Investimentos, Outros

## Transaction (transactions app)

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| user | ForeignKey(User) | on_delete=CASCADE, related_name='transactions' |
| account | ForeignKey(Account) | on_delete=CASCADE, related_name='transactions' |
| category | ForeignKey(Category) | on_delete=CASCADE, related_name='transactions' |
| description | CharField | max_length=200 |
| amount | DecimalField | max_digits=12, decimal_places=2 |
| transaction_type | CharField | max_length=10, choices: entrada/saida |
| date | DateField | default=timezone.now |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- `Meta.ordering = ['-date', '-created_at']`
- `__str__` retorna `f'{self.description} - {self.amount}'`

### Choices de transaction_type

| Valor | Label |
|-------|-------|
| entrada | Entrada |
| saida | Saida |

### Signal de saldo

Ao criar uma transacao do tipo "entrada", o saldo da conta e incrementado. Ao criar do tipo "saida", o saldo e decrementado. Ao editar, a diferenca e aplicada. Ao excluir, o valor e revertido.

---

## AIAnalysis (ai app)

Model que armazena as analises financeiras geradas pelo agente de IA.

| Campo | Tipo | Detalhes |
|-------|------|---------|
| id | BigAutoField | PK |
| user | ForeignKey(User) | on_delete=CASCADE, related_name='ai_analyses' |
| analysis_text | TextField | conteudo completo da analise gerada pela IA |
| key_insights | JSONField | default=list, principais insights extraidos |
| recommendations | JSONField | default=list, recomendacoes geradas |
| period_analyzed | CharField | max_length=100, periodo analisado (ex: "Ultimos 30 dias") |
| model_used | CharField | max_length=50, modelo LLM utilizado (valor de settings.OPENAI_MODEL) |
| tokens_input | IntegerField | default=0, tokens de entrada consumidos |
| tokens_output | IntegerField | default=0, tokens de saida consumidos |
| is_latest | BooleanField | default=True, marca a analise mais recente do usuario |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

- `Meta.ordering = ['-created_at']`
- `Meta.verbose_name = 'analise IA'`, `Meta.verbose_name_plural = 'analises IA'`
- Indexes em `(user, -created_at)` e `(user, is_latest)`
- `__str__` retorna `f'{self.user.email} - {self.period_analyzed}'`
- Ao criar nova analise com `is_latest=True`, `is_latest` das analises anteriores do mesmo usuario e setado para `False`
- Rate limiting: nao gerar nova analise se a ultima for ha menos de 24h (configuravel)

### Logica de is_latest

Apenas uma analise por usuario pode ter `is_latest=True`. Ao criar uma nova analise:
1. Todas as analises anteriores do mesmo usuario recebem `is_latest=False`
2. A nova analise e salva com `is_latest=True`
3. O dashboard sempre busca a analise com `is_latest=True`

### Configuracao de ambiente

Variaveis no `.env` (nunca commitar valores reais):

| Variavel | Padrao | Descricao |
|----------|--------|-----------|
| OPENAI_API_KEY | (vazio) | Chave da API OpenAI |
| OPENAI_MODEL | gpt-5-mini | Modelo LLM utilizado |
| AI_MAX_TOKENS | 2000 | Maximo de tokens na resposta |
| AI_TEMPERATURE | 0.7 | Temperatura do modelo (criatividade) |