# Portfólio — Paulo Ambrosi

Site estático publicado em **https://paulo.ambrosi.top** (GitHub Pages, repositório
`pauloambrosi/portfolio`, domínio próprio via `CNAME`).

Bilíngue (pt-BR / en), sem build, sem dependência instalada: HTML5, CSS3 e
JavaScript puro. A única requisição externa é o Google Fonts.

## Estrutura

```
index.html            home (pt-BR)
flow/                 case do FLOW (pt-BR)
moodle/               case do Moodle (pt-BR)
en/                   os mesmos três em inglês
404.html
css/styles.css        folha única; as cores vivem em custom properties no topo
js/main.js            tema, menu, scrollspy, reveal, contadores, filtros
assets/               foto, favicon, og-image, capturas
tools/check.py        validador do site
tools/contrast.py     verificador de contraste WCAG
tools/og-image.html   fonte do og-image (não é publicado como página)
CNAME                 paulo.ambrosi.top — não apagar
sitemap.xml robots.txt
```

## Publicar

```bash
git add -A && git commit -m "atualiza portfólio" && git push
```

O GitHub Pages publica a branch `main` a partir da raiz. Leva 1–2 minutos.

## Antes de cada push

```bash
python3 tools/check.py
```

Verifica, em todas as páginas: `title`, `description`, `canonical`, `hreflang`
recíproco, `lang` correto, um único `h1`, `alt` em toda imagem, ausência do
telefone, ausência de caminho absoluto interno, links quebrados e coerência do
`sitemap.xml`. Sai com código 1 se achar erro.

```bash
python3 tools/contrast.py
```

Confere o contraste de todos os pares de cor nos dois temas (WCAG 2.2 AA).
Rode se mexer nas cores.

## Editar o conteúdo

O texto está direto no HTML — não há CMS nem arquivo de dados. Ao mudar algo em
português, mude o equivalente em inglês: `index.html` ↔ `en/index.html`,
`flow/` ↔ `en/flow/`, `moodle/` ↔ `en/moodle/`.

### Trocar as cores

Tudo em `css/styles.css`, no bloco `:root` (tema claro) e nos dois blocos do
tema escuro — `@media (prefers-color-scheme: dark)` e `[data-theme="dark"]`.
Os três blocos precisam ser alterados juntos. Depois rode `tools/contrast.py`.

### Acrescentar uma habilidade

Em `index.html`, dentro de `<div class="chips">`:

```html
<span class="chip" data-tags="lms">Nova habilidade</span>
```

`data-tags` aceita mais de um grupo separado por espaço. Grupos existentes:
`lms`, `backend`, `frontend`, `ia`, `soft`. Repita em `en/index.html`.

### Trocar as capturas do Moodle

Os quatro slots em `moodle/index.html` usam `assets/moodle/placeholder.svg`.
Substitua o `src` pelo arquivo real, ajuste `width`, `height`, o `alt` e a
`figcaption`, e remova a classe `shot--pending` e o aviso
`<span class="pending-note">`. Faça o mesmo em `en/moodle/index.html`.

Recomendado: JPEG de 1600px de largura, qualidade ~82. Telas com nome de
participante não devem ser publicadas.

### Regerar o og-image

Editar `tools/og-image.html` e, com um servidor local na raiz do projeto:

```bash
google-chrome --headless --disable-gpu --hide-scrollbars --window-size=1200,630 --screenshot=assets/og-image.png --virtual-time-budget=8000 "http://localhost:4173/tools/og-image.html"
```

### Servidor local

```bash
python3 -m http.server 4173
```

## Origem do conteúdo

Os textos vêm do currículo em `pauloambrosi/cv`. O case do FLOW vem do README
do próprio sistema; as capturas saíram do manual do Especialista Técnico, de um
ambiente de demonstração, sem dados reais de usuários.
