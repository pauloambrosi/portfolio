# Portfólio Paulo Ambrosi — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o portfólio estático bilíngue de Paulo Ambrosi, pronto para publicar no GitHub Pages em `https://paulo.ambrosi.top`.

**Architecture:** Seis páginas HTML estáticas (três em pt-BR, três em en) servidas direto do repositório, compartilhando uma folha de estilo e um módulo JavaScript. Sem build, sem framework, sem dependência instalada. Os tokens visuais vivem em custom properties CSS, o que dá tema claro/escuro sem duplicar regra.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, `IntersectionObserver` via JS), JavaScript ES2020 vanilla, Google Fonts (Inter + JetBrains Mono) com fallback de sistema.

**Spec:** `docs/superpowers/specs/2026-09-21-portfolio-design.md`

## Global Constraints

- Sem etapa de build e sem dependência instalada. Única origem externa: `fonts.googleapis.com` / `fonts.gstatic.com`.
- `CNAME` com o conteúdo `paulo.ambrosi.top` permanece na raiz, intocado.
- Todo caminho interno é relativo (`../css/styles.css`), nunca começa com `/`.
- Canonical e `sitemap.xml` usam o domínio absoluto `https://paulo.ambrosi.top`.
- Contato publicado: `ambrosipaulo@gmail.com` e `https://linkedin.com/in/pauloambrosi`. O telefone `+55 71 99213-9049` **não** aparece em nenhum arquivo.
- Todo texto vem do CV em `pauloambrosi/cv`. Nenhum fato novo é inventado.
- Contraste mínimo 4.5:1 para texto normal e 3:1 para texto grande e indicador de foco, nos dois temas.
- `@media (prefers-reduced-motion: reduce)` zera toda animação e transição.
- Um `<h1>` por página; `alt` em toda imagem; skip-link em toda página.
- Acesso a `localStorage` sempre dentro de `try/catch`.

## Verificação neste projeto

Não há framework de teste — é um site estático. Cada tarefa termina com uma
verificação executável concreta:

- `python3 tools/check.py` — script do projeto que valida, em todo HTML:
  presença de `<title>`, `description`, `canonical`, `hreflang` recíproco,
  `lang` correto, exatamente um `h1`, `alt` em toda `<img>`, ausência do
  telefone, ausência de caminho absoluto interno, e que todo `href`/`src`
  relativo aponte para arquivo existente.
- Navegador (`mcp__Claude_Browser__*`) — console sem erro, layout em
  360/768/1440px, tema claro e escuro.

---

### Task 1: Fundação do projeto

**Files:**
- Create: `css/styles.css`, `robots.txt`, `.gitignore`, `tools/check.py`
- Create: `assets/profile.jpg`, `assets/favicon.svg` (copiados de `pauloambrosi/cv`)
- Preserve: `CNAME`

**Interfaces:**
- Produces: tokens CSS em `:root` consumidos por todas as páginas —
  `--bg`, `--surface`, `--surface-2`, `--ink`, `--ink-muted`, `--moss`,
  `--moss-dark`, `--moss-light`, `--accent`, `--accent-hover`, `--border`,
  `--radius`, `--shadow`, `--ease`, `--maxw`.
- Produces: `tools/check.py`, executado ao fim de cada tarefa seguinte.

- [ ] **Step 1: Copiar os assets do repo cv**

```bash
cp "/home/ambrosi/Downloads/curriculo-benearagao-projeto-main/cv/assets/profile.jpg" assets/profile.jpg
cp "/home/ambrosi/Downloads/curriculo-benearagao-projeto-main/cv/assets/favicon.svg" assets/favicon.svg
```

- [ ] **Step 2: Escrever `css/styles.css`** — reset, tokens claros, bloco
      `[data-theme="dark"]`, bloco `@media (prefers-color-scheme: dark)`
      guardado por `:root:not([data-theme="light"])`, tipografia, e o bloco
      `prefers-reduced-motion`.

- [ ] **Step 3: Escrever `tools/check.py`** com as validações listadas acima.

- [ ] **Step 4: Rodar `python3 tools/check.py`** — esperado: sem HTML ainda,
      saída "0 páginas verificadas", saindo com código 0.

---

### Task 2: Home pt-BR

**Files:**
- Create: `index.html`
- Modify: `css/styles.css` (componentes: nav, hero, stats, chips, cards, timeline, footer)

**Interfaces:**
- Consumes: tokens da Task 1.
- Produces: as âncoras `#sobre`, `#habilidades`, `#projetos`, `#experiencia`,
  `#contato`, e os hooks de JS `data-reveal`, `data-count`,
  `data-filter-group`, `data-filter`, `#nav-toggle`, `#theme-toggle` —
  todos reutilizados pelas demais páginas.

- [ ] **Step 1: Escrever o `<head>`** — title, description, canonical
      `https://paulo.ambrosi.top/`, OG, Twitter Card, `hreflang` pt-BR/en/x-default,
      JSON-LD `Person`.
- [ ] **Step 2: Escrever o corpo** — skip-link, header com nav e os dois
      toggles, as seis seções, footer.
- [ ] **Step 3: Estilizar os componentes** em `css/styles.css`.
- [ ] **Step 4: Rodar `python3 tools/check.py`** — esperado: 1 página, 0 erros.
- [ ] **Step 5: Abrir no navegador** em 360/768/1440px — esperado: console
      limpo, nenhuma barra de rolagem horizontal.

---

### Task 3: Comportamento (JavaScript)

**Files:**
- Create: `js/main.js`
- Modify: `index.html` (incluir `<script src="js/main.js" defer>`)

**Interfaces:**
- Consumes: os hooks `data-*` da Task 2.
- Produces: nada que outras tarefas importem — o script é autocontido e
  inerte em páginas que não tenham os hooks.

- [ ] **Step 1: Tema** — ler `localStorage` em try/catch, aplicar
      `data-theme` no `<html>`, alternar no clique, atualizar `aria-pressed`.
- [ ] **Step 2: Menu mobile** — abrir/fechar, `aria-expanded`, fechar com
      `Escape`, prender o foco enquanto aberto.
- [ ] **Step 3: Scrollspy** — `IntersectionObserver` marcando `aria-current`
      no item de nav visível.
- [ ] **Step 4: Reveal** — `IntersectionObserver` adicionando `.is-visible`
      em `[data-reveal]`, com stagger por `--i`; desativado sob
      `prefers-reduced-motion`.
- [ ] **Step 5: Contadores** — animar `[data-count]` uma única vez ao entrar
      na viewport; sob `prefers-reduced-motion`, escrever o valor final direto.
- [ ] **Step 6: Filtro de habilidades** — botões `[data-filter]` alternando a
      visibilidade dos chips, com `aria-pressed` e um contador de resultados
      em região `aria-live`.
- [ ] **Step 7: Verificar no navegador** — clicar em cada controle, confirmar
      console limpo e `prefers-reduced-motion` respeitado
      (`resize_window` + emulação, ou alternar o media query via devtools).

---

### Task 4: Case study do FLOW (pt-BR)

**Files:**
- Create: `flow/index.html`
- Modify: `css/styles.css` (layout de artigo: sumário lateral, blocos de destaque)

**Interfaces:**
- Consumes: tokens, componentes e hooks das Tasks 1–3.

- [ ] **Step 1: `<head>`** — canonical `https://paulo.ambrosi.top/flow/`,
      hreflang para `/en/flow/`, JSON-LD `CreativeWork`.
- [ ] **Step 2: Corpo** — contexto (produção de EAD do SENAI Bahia dispersa),
      o que o FLOW faz (autoria colaborativa, revisão, versionamento,
      validação, simulação da experiência do aluno, IA via OpenAI API), papel
      do Paulo, stack (PHP, HTML, CSS, JavaScript, OpenAI API), e resultado.
      Todo o conteúdo factual sai do CV; nada além dele.
- [ ] **Step 3: Rodar `python3 tools/check.py`** — esperado: 2 páginas, 0 erros.

---

### Task 5: Case study Moodle (pt-BR)

**Files:**
- Create: `moodle/index.html`, `assets/moodle/placeholder.svg`
- Modify: `css/styles.css` (galeria)

**Interfaces:**
- Consumes: tokens e componentes anteriores.
- Produces: `figure.shot > img[data-shot]` — os slots que receberão os prints
      reais depois da captura.

- [ ] **Step 1: `<head>`** — canonical `https://paulo.ambrosi.top/moodle/`,
      hreflang para `/en/moodle/`, JSON-LD `CreativeWork`.
- [ ] **Step 2: Bloco de competências** — administração, plugins, temas,
      integrações, SCORM, relatórios, migração de versão.
- [ ] **Step 3: Os três AVAs** — ObsPLE-PL2 (CNPq/IILP-CPLP, ~750 usuários,
      três edições), (Re)Integro (Ministério da Justiça/OEI), Cruzando
      Fronteiras (UFRGS/OEI).
- [ ] **Step 4: Galeria** com placeholders marcados como "print pendente".
- [ ] **Step 5: Rodar `python3 tools/check.py`** — esperado: 3 páginas, 0 erros.

---

### Task 6: Espelho em inglês

**Files:**
- Create: `en/index.html`, `en/flow/index.html`, `en/moodle/index.html`

**Interfaces:**
- Consumes: a estrutura das Tasks 2, 4 e 5; caminhos sobem um nível
      (`../css/styles.css`) ou dois (`../../css/styles.css`).

- [ ] **Step 1: Traduzir a home** usando o texto já existente em
      `pauloambrosi/cv/en.html`; `lang="en"`, canonical `/en/`, hreflang recíproco.
- [ ] **Step 2: Traduzir o case do FLOW**; canonical `/en/flow/`.
- [ ] **Step 3: Traduzir o case do Moodle**; canonical `/en/moodle/`.
- [ ] **Step 4: Rodar `python3 tools/check.py`** — esperado: 6 páginas,
      0 erros, todo par hreflang recíproco.

---

### Task 7: SEO, 404 e fechamento

**Files:**
- Create: `404.html`, `sitemap.xml`, `assets/og-image.svg`, `assets/og-image.png`, `README.md`
- Modify: `robots.txt`

**Interfaces:**
- Consumes: as seis URLs finais.

- [ ] **Step 1: Gerar o OG image** 1200×630 em SVG (nome, título, paleta) e
      converter para PNG com a ferramenta disponível
      (`rsvg-convert`, `inkscape` ou `python3 -c` com cairosvg); se nenhuma
      existir, registrar isso e apontar o `og:image` para o SVG.
- [ ] **Step 2: `sitemap.xml`** com as seis URLs e `lastmod` 2026-09-21.
- [ ] **Step 3: `robots.txt`** liberando tudo e apontando o sitemap.
- [ ] **Step 4: `404.html`** no mesmo visual, com link de volta.
- [ ] **Step 5: `README.md`** — como editar o conteúdo, como trocar os prints
      do Moodle, como publicar.
- [ ] **Step 6: Rodar `python3 tools/check.py`** — esperado: 7 páginas, 0 erros.
- [ ] **Step 7: Verificação final no navegador** — as seis páginas nos dois
      temas, em 360px e 1440px, console limpo, `CNAME` ainda presente na raiz.
