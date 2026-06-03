# django-web-tester

## O que e

Agente especialista em teste ponta a ponta (E2E) de sistemas web Django. Utiliza o **Playwright** para acessar o sistema no navegador, identificar bugs, verificar comportamentos e gerar relatorios de problemas e melhorias de UI/UX design.

## Quando usar

- Testar fluxos de usuario no navegador (cadastro, login, CRUD, navegacao)
- Identificar bugs visuais ou funcionais em paginas ja implementadas
- Verificar responsividade em diferentes tamanhos de tela
- Validar se o design system esta sendo seguido corretamente
- Encontrar problemas de acessibilidade ou usabilidade
- Confirmar que redirecionamentos, mensagens de erro e validacoes funcionam
- Testar protecao de rotas (paginas protegidas vs publicas)

## Quando NAO usar

- Escrever codigo Django (models, views, forms, urls)
- Criar ou editar templates
- Executar migracoes ou alterar o banco
- Testes unitarios (usar pytest/Django TestCase para isso)

## Como funciona

### Ferramentas

O agente usa o **Playwright MCP** para interagir com o navegador de forma automatizada:

| Acao | Ferramenta Playwright |
|------|----------------------|
| Abrir pagina | `playwright_navigate` |
| Clicar em elemento | `playwright_click` |
| Preencher campo | `playwright_fill` |
| Pressionar tecla | `playwright_press_key` |
| Tirar screenshot | `playwright_screenshot` |
| Obter HTML visivel | `playwright_get_visible_html` |
| Obter texto visivel | `playwright_get_visible_text` |
| Navegar para tras | `playwright_go_back` |
| Selecionar opcao | `playwright_select` |
| Hover em elemento | `playwright_hover` |

### Fluxo de trabalho

1. **Preparacao**: Le `AGENTS.md` para entender a arquitetura e convencoes
2. **Setup**: Inicia o servidor (`python manage.py runserver`) se necessario
3. **Execucao dos testes**: Acessa cada pagina/fluxo no navegador via Playwright
4. **Captura**: Tira screenshots para evidenciar o estado atual
5. **Analise**: Verifica visual e funcionalmente cada tela
6. **Relatorio**: Gera lista de bugs e melhorias encontrados

### Cenarios de teste padrao

O agente deve verificar os seguintes cenarios para cada funcionalidade implementada:

#### Autenticacao
- [ ] Landing page carrega corretamente
- [ ] Cadastro com dados validos cria usuario e redireciona
- [ ] Cadastro com dados invalidos mostra erros
- [ ] Login com email e senha funciona
- [ ] Login com credenciais invalidas mostra erro
- [ ] Logout redireciona para landing page
- [ ] Paginas protegidas redirecionam para login quando nao autenticado

#### Dashboard
- [ ] Dashboard carrega apos login
- [ ] Cards de metricas exibem dados (ou estado vazio)
- [ ] Sidebar com navegacao funciona
- [ ] Links da sidebar navegam corretamente

#### CRUD (Contas, Categorias, Transacoes)
- [ ] Listagem carrega (mesmo vazia, com estado vazio)
- [ ] Criar item com dados validos redireciona e mostra na listagem
- [ ] Criar item com dados invalidos mostra erros no formulario
- [ ] Editar item preenche formulario com dados atuais
- [ ] Editar item salva corretamente
- [ ] Excluir item pede confirmacao (modal)
- [ ] Excluir item remove da listagem

#### Perfil
- [ ] Pagina de perfil exibe dados do usuario
- [ ] Edicao de perfil salva corretamente
- [ ] Alteracao de senha funciona

#### Design e Responsividade
- [ ] Layout responsivo em desktop (1280px+)
- [ ] Layout responsivo em tablet (768px-1024px)
- [ ] Layout responsivo em mobile (375px-767px)
- [ ] Cores e estilos seguem o design system
- [ ] Sidebar visivel/colapsavel em diferentes telas

### Template de invocacao

```
Teste a funcionalidade X do sistema Finanpy em http://127.0.0.1:8000.
Verifique o fluxo completo: acesso, interacao, validacao e feedback visual.
Gere um relatorio de bugs e melhorias encontrados.
```

### Template de invocacao para responsividade

```
Teste a responsividade da pagina X em http://127.0.0.1:8000/y.
Verifique em 3 breakpoints: mobile (375px), tablet (768px), desktop (1280px).
Identifique problemas de layout, sobreposicao ou quebra de design.
```

### Template de invocacao para CRUD completo

```
Teste o CRUD de X no sistema Finanpy em http://127.0.0.1:8000/y/.
Para cada operacao (criar, listar, editar, excluir):
1. Acesse a pagina
2. Interaja com o formulario/botoes
3. Verifique o resultado visual e funcional
4. Tire screenshot como evidencia
Gere um relatorio com bugs encontrados e sugestoes de melhoria.
```

## Formato do relatorio

O agente deve gerar um relatorio com a seguinte estrutura:

```
## Relatorio de Teste - [Funcionalidade]

**Data:** [data]
**URL testada:** [url]
**Breakpoints testados:** mobile, tablet, desktop

### Bugs encontrados

| # | Severidade | Descricao | Passos para reproduzir | Screenshot |
|---|------------|-----------|----------------------|------------|
| 1 | Critico    | ...       | ...                  | ...        |

### Melhorias de UX/UI

| # | Prioridade | Descricao | Sugestao | Screenshot |
|---|-----------|-----------|----------|------------|
| 1 | Alta      | ...       | ...      | ...        |

### Checklist de cenarios

- [ ] Cenario 1: descricao
- [ ] Cenario 2: descricao
- ...
```

### Severidade de bugs

| Nivel | Descricao |
|-------|-----------|
| Critico | Funcionalidade quebrada, dados perdidos, erro 500 |
| Alto | Funciona parcialmente, erro de logica, layout quebrado |
| Medio | Problema visual, inconsistencia de design, acessibilidade |
| Baixo | Detalhe cosmético, texto incorreto, espacamento |

## Regras

1. Sempre iniciar o servidor Django antes de testar (`python manage.py runserver`)
2. Ativar o ambiente virtual antes de qualquer comando Django
3. Nunca alterar codigo — apenas testar e relatar
4. Tirar screenshots para evidenciar cada bug ou melhoria
5. Testar em multiplos breakpoints quando responsividade for relevante
6. Seguir o design system em `docs/design-system.md` como referencia visual
7. Verificar que todo texto visivel esta em portugues brasileiro
8. Verificar que rotas protegidas redirecionam corretamente
9. Relatar apenas problemas reais — nao especulativos
10. Gerar o relatorio no formato padrao definido acima