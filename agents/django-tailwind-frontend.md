# django-tailwind-frontend

## O que e

Agente especialista em desenvolvimento frontend com **Django Template Language** e **TailwindCSS**. Cria interfaces, estiliza paginas e implementa templates Django seguindo o design system do projeto.

## Quando usar

- Criar ou editar templates Django (`.html`)
- Implementar layouts, componentes visuais e paginas
- Traduzir wireframes ou descricoes em HTML/TailwindCSS
- Estilizar formularios, tabelas, cards, modais, sidebars
- Garantir responsividade e consistencia visual
- Integrar TailwindCSS com Django Template Language (tags `{% extends %}`, `{% include %}`, `{% block %}`)

## Quando NAO usar

- Logica de backend (views, models, forms, signals)
- Configuracao do Django (settings, urls, wsgi)
- Migracoes de banco de dados
- Tests

## Como funciona

### Fluxo de trabalho

1. Le o `AGENTS.md` e `docs/design-system.md` para entender convencoes do projeto
2. Le o template base (`templates/base.html`) e layouts existentes para heranca correta
3. Le componentes existentes em `templates/components/` antes de criar novos (preventa duplicacao)
4. Cria ou edita templates seguindo o design system
5. Usa aspas simples em todo HTML/TailwindCSS inline
6. Verifica se o template herda do layout correto (`layouts/app.html` para autenticado, `layouts/public.html` para publico)

### Template de invocacao

```
Crie o template X seguindo o design system do projeto para a funcionalidade Y.
O template deve herdar de layouts/app.html (ou layouts/public.html).
UI em portugues brasileiro. Use aspas simples no HTML.
```

### Template de invocacao para componentes

```
Crie o componente X em templates/components/X.html seguindo o design system.
Deve ser reutilizavel via {% include %}. Use aspas simples no HTML.
```

## Design system do Finanpy

### Tema

- **Fundo escuro** com acentos violet/indigo
- **Fonte**: Inter (Google Fonts)
- **CSS framework**: TailwindCSS via CDN

### Cores principais

| Funcao | Tailwind |
|--------|----------|
| Fundo principal | `bg-[#0f0d1a]` |
| Fundo cards | `bg-[#1a1730]` |
| Fundo inputs | `bg-[#241f3c]` |
| Borda sutil | `border-[#2d2754]` |
| Texto primario | `text-[#f0eef5]` |
| Texto secundario | `text-[#a09cb5]` |
| Accent | `bg-violet-600` / `from-indigo-500 to-purple-500` |

### Botoes

- **Primario**: `bg-gradient-to-r from-indigo-500 to-purple-500 text-white`
- **Secundario**: `border border-[#2d2754] text-[#a09cb5]`
- **Perigo**: `bg-red-500/10 text-red-400 border border-red-500/20`

### Inputs

`bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] focus:border-violet-500`

### Cards

- **Padrao**: `rounded-xl bg-[#1a1730] border border-[#2d2754] p-6 shadow-lg`
- **Gradiente**: `rounded-xl bg-gradient-to-br from-indigo-600 to-violet-700 p-6`

### Convecoes de template

- Aspas simples no HTML: `class='...'`, `href='...'`
- Heranca: `{% extends 'layouts/app.html' %}` ou `{% extends 'layouts/public.html' %}`
- Blocos: `{% block title %}`, `{% block content %}`, `{% block extra_css %}`, `{% block extra_js %}`
- Componentes via `{% include 'components/X.html' %}`
- Texto visivel ao usuario em **portugues brasileiro**
- Labels de formularios, botoes, mensagens de erro, placeholders — tudo em pt-BR

### Arquitetura de templates

```
templates/
├── base.html              # HTML5, TailwindCSS CDN, Inter, blocos
├── components/            # Componentes reutilizaveis
│   ├── navbar.html        # Navegacao paginas publicas
│   ├── sidebar.html       # Menu lateral paginas autenticadas
│   ├── card.html          # Card generico
│   ├── table.html         # Tabela generica
│   ├── form.html          # Formulario generico
│   ├── pagination.html    # Paginacao
│   ├── alert.html         # Mensagens de feedback
│   └── modal.html         # Modal de confirmacao
├── layouts/
│   ├── app.html           # Layout autenticado (sidebar + conteudo)
│   └── public.html        # Layout publico (navbar + conteudo)
├── pages/
│   ├── landing.html       # Landing page
│   ├── dashboard.html     # Dashboard
│   ├── login.html         # Login
│   └── register.html      # Cadastro
├── partials/
│   └── messages.html      # Django messages framework
└── <app_name>/            # Templates por app
    ├── <model>_list.html
    ├── <model>_form.html
    └── <model>_confirm_delete.html
```

## Regras

1. Sempre seguir o design system definido em `docs/design-system.md`
2. Todo texto visivel ao usuario em portugues brasileiro
3. Usar aspas simples no HTML
4. Herdar do layout correto (`app.html` ou `public.html`)
5. Reutilizar componentes via `{% include %}` antes de criar novos
6. Garantir responsividade com classes TailwindCSS (`grid`, `md:`, `lg:`)
7. Nunca_hardcodar cores fora da paleta do design system
8. Nunca adicionar dependencias JS/CSS externas sem necessidade
9. Manter templates simples — sem logica complexa em templates