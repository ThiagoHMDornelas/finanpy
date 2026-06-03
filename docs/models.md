# Models

Definicao dos models planejados para o projeto Finanpy. Todos os models possuem campos `created_at` e `updated_at`.

## Diagrama de relacionamentos

```mermaid
erDiagram
    User ||--o|| Profile : has
    User ||--o{ Account : owns
    User ||--o{ Category : owns
    User ||--o{ Transaction : creates
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