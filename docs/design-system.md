# Design System

Tema escuro com acentos em violet/indigo. Todos os estilos usam TailwindCSS dentro do Django Template Language.

## Paleta de cores

| Funcao | Cor | Tailwind |
|--------|-----|----------|
| Fundo principal | `#0f0d1a` | `bg-[#0f0d1a]` |
| Fundo cards/superficies | `#1a1730` | `bg-[#1a1730]` |
| Fundo inputs/elevado | `#241f3c` | `bg-[#241f3c]` |
| Borda sutil | `#2d2754` | `border-[#2d2754]` |
| Texto primario | `#f0eef5` | `text-[#f0eef5]` |
| Texto secundario | `#a09cb5` | `text-[#a09cb5]` |
| Texto terciario | `#6b6785` | `text-[#6b6785]` |
| Accent primario | violet-600 | `bg-violet-600` |
| Accent hover | violet-700 | `bg-violet-700` |
| Gradient inicio | indigo-500 | `from-indigo-500` |
| Gradient fim | purple-500 | `to-purple-500` |
| Sucesso/Receita | green-500 | `text-green-500` |
| Erro/Despesa | red-500 | `text-red-500` |
| Aviso | amber-500 | `text-amber-500` |
| Info | blue-500 | `text-blue-500` |

## Gradientes

| Uso | Classes Tailwind |
|-----|-------------------|
| Botoes primarios | `bg-gradient-to-r from-indigo-500 to-purple-500` |
| Card destaque | `bg-gradient-to-br from-indigo-600 to-violet-700` |
| Hero/Landing | `bg-gradient-to-r from-indigo-600 via-purple-600 to-fuchsia-500` |
| Sidebar ativo | `bg-gradient-to-r from-indigo-600/20 to-violet-600/20` |

## Tipografia

| Elemento | Estilo | Classes Tailwind |
|----------|--------|-------------------|
| H1 | Inter Bold 2.5rem | `text-4xl font-bold` |
| H2 | Inter Bold 2rem | `text-3xl font-bold` |
| H3 | Inter Semibold 1.5rem | `text-2xl font-semibold` |
| Body | Inter Regular 1rem | `text-base` |
| Small | Inter Regular 0.875rem | `text-sm` |
| Label | Inter Medium 0.875rem | `text-sm font-medium` |

Fonte: Inter (Google Fonts)

## Componentes

### Botao primario

```html
<button class='px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500
  text-white font-medium hover:from-indigo-600 hover:to-purple-600
  transition-all duration-200 shadow-lg shadow-violet-500/25'>
  Acao
</button>
```

### Botao secundario

```html
<button class='px-4 py-2 rounded-lg border border-[#2d2754] text-[#a09cb5]
  hover:bg-[#241f3c] transition-all duration-200'>
  Cancelar
</button>
```

### Botao de perigo

```html
<button class='px-4 py-2 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20
  hover:bg-red-500/20 transition-all duration-200'>
  Excluir
</button>
```

### Input

```html
<div class='space-y-1'>
  <label class='block text-sm font-medium text-[#a09cb5]'>Campo</label>
  <input type='text'
    class='w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754]
    text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500
    focus:ring-1 focus:ring-violet-500 transition-all duration-200' />
</div>
```

### Card

```html
<div class='rounded-xl bg-[#1a1730] border border-[#2d2754] p-6
  shadow-lg shadow-black/20'>
  <!-- conteudo -->
</div>
```

### Card com gradiente

```html
<div class='rounded-xl bg-gradient-to-br from-indigo-600 to-violet-700 p-6
  shadow-lg shadow-violet-500/20'>
  <!-- conteudo -->
</div>
```

### Tabela

```html
<div class='rounded-xl bg-[#1a1730] border border-[#2d2754] overflow-hidden'>
  <table class='w-full'>
    <thead>
      <tr class='border-b border-[#2d2754]'>
        <th class='px-4 py-3 text-left text-sm font-medium text-[#a09cb5]'>Coluna</th>
      </tr>
    </thead>
    <tbody>
      <tr class='border-b border-[#2d2754]/50 hover:bg-[#241f3c]/50 transition-colors'>
        <td class='px-4 py-3 text-sm text-[#f0eef5]'>Valor</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Sidebar

```html
<nav class='w-64 min-h-screen bg-[#0f0d1a] border-r border-[#2d2754]'>
  <div class='p-6'>
    <a href='#' class='logo text-xl font-bold bg-gradient-to-r from-indigo-500 to-purple-500
      bg-clip-text text-transparent'>Finanpy</a>
  </div>
  <ul class='space-y-1 px-3'>
    <li>
      <a href='#'
        class='flex items-center gap-3 px-4 py-2.5 rounded-lg bg-gradient-to-r
        from-indigo-600/20 to-violet-600/20 text-violet-400 font-medium'>
        <span>Dashboard</span>
      </a>
    </li>
    <li>
      <a href='#'
        class='flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#a09cb5]
        hover:bg-[#1a1730] transition-all duration-200'>
        <span>Contas</span>
      </a>
    </li>
  </ul>
</nav>
```

### Alert successo

```html
<div class='rounded-lg bg-green-500/10 border border-green-500/20 px-4 py-3
  text-green-400 text-sm'>
  Operacao realizada com sucesso.
</div>
```

### Alert erro

```html
<div class='rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3
  text-red-400 text-sm'>
  Ocorreu um erro.
</div>
```

### Modal

```html
<div class='fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm'>
  <div class='w-full max-w-md rounded-xl bg-[#1a1730] border border-[#2d2754] p-6 shadow-2xl'>
    <h3 class='text-lg font-semibold text-[#f0eef5]'>Confirmar acao</h3>
    <p class='mt-2 text-sm text-[#a09cb5]'>Tem certeza?</p>
    <div class='mt-6 flex justify-end gap-3'>
      <button class='px-4 py-2 rounded-lg border border-[#2d2754] text-[#a09cb5]'>Cancelar</button>
      <button class='px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 text-white'>Confirmar</button>
    </div>
  </div>
</div>
```

### Layout autenticado (sidebar + conteudo)

```html
<div class='flex min-h-screen bg-[#0f0d1a]'>
  {% include 'components/sidebar.html' %}
  <main class='flex-1 p-6'>
    <!-- conteudo -->
  </main>
</div>
```

### Grid de cards (dashboard)

```html
<div class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'>
  <!-- cards de metricas -->
</div>
```

## Padroes visuais

| Elemento | Regra |
|----------|-------|
| Border radius | `rounded-lg` para inputs/botoes, `rounded-xl` para cards/modais |
| Shadows | `shadow-lg shadow-black/20` para cards, `shadow-lg shadow-violet-500/25` para botoes gradient |
| Transicoes | `transition-all duration-200` em todos elementos interativos |
| Espacamento | `p-6` cards, `gap-4` grids, `space-y-6` secoes |
| Foco inputs | `focus:border-violet-500 focus:ring-1 focus:ring-violet-500` |
| Hover | Sempre com `transition-all duration-200` |

## Cores semanticas

| Contexto | Cor | Uso |
|----------|-----|-----|
| Entrada/Receita | `green-500` | Texto de valores positivos, badges de receita |
| Saida/Despesa | `red-500` | Texto de valores negativos, badges de despesa |
| Saldo positivo | `green-500` | Indicador de saldo positivo |
| Saldo negativo | `red-500` | Indicador de saldo negativo |