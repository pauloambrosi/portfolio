# Portfólio Paulo Ambrosi — Design

Data: 2026-09-21
Status: aprovado pelo usuário

## Objetivo

Site de portfólio estático, bilíngue (pt-BR / en), hospedado no GitHub Pages
em `https://paulo.ambrosi.top`, para apresentar habilidades, o sistema FLOW e
os trabalhos com Moodle. Alvo: recrutadores e clientes buscando especialista
em Moodle / EAD / desenvolvimento web no Brasil.

## Restrições

- GitHub Pages: apenas arquivos estáticos, sem backend, sem etapa de build.
- Sem dependências instaladas: HTML5 + CSS3 + JavaScript vanilla.
  Única requisição externa permitida: Google Fonts (com fallback de sistema).
- O arquivo `CNAME` (`paulo.ambrosi.top`) deve permanecer na raiz.
- Caminhos relativos em todo lugar, para funcionar tanto em
  `paulo.ambrosi.top` quanto em `pauloambrosi.github.io/portfolio`.
- Acessibilidade WCAG 2.2 AA, mantendo o padrão já adotado no repo `cv`.

## Fonte de conteúdo

Todo o texto vem do CV existente (`pauloambrosi/cv`, `index.html` + `en.html`).
Nada é inventado. Números citados: 12+ anos de experiência, ~750 usuários no
ObsPLE-PL2, 4 projetos selecionados.

Dados de contato publicados: `ambrosipaulo@gmail.com` e
`linkedin.com/in/pauloambrosi`. **O telefone NÃO vai para o site** (decisão do
usuário: evitar spam).

## Estrutura de arquivos

```
/
├── index.html              home pt-BR
├── flow/index.html         case study FLOW (pt-BR)
├── moodle/index.html       case study Moodle e AVAs (pt-BR)
├── en/index.html           home en
├── en/flow/index.html      case study FLOW (en)
├── en/moodle/index.html    case study Moodle e AVAs (en)
├── 404.html
├── css/styles.css          folha única, custom properties
├── js/main.js              nav, scrollspy, reveal, filtros, tema, contadores
├── assets/
│   ├── profile.jpg         copiado do repo cv
│   ├── favicon.svg
│   ├── og-image.png        gerado (1200×630)
│   └── moodle/             prints do Moodle (placeholders até a captura)
├── CNAME                   preservado
├── robots.txt
└── sitemap.xml
```

## Seções da home

1. **Hero** — nome, título, uma linha de posicionamento, CTAs (ver FLOW / contato),
   seletor de idioma e alternador de tema.
2. **Sobre** — os dois parágrafos do CV + faixa de números animados
   (12+ anos · 4 projetos · ~750 usuários · 3 edições do ObsPLE).
3. **Habilidades** — chips por grupo, filtráveis:
   LMS & EAD · Backend · Frontend · Automação & IA · Dados.
4. **Projetos** — card de destaque do FLOW + 3 cards de AVA, com tags de
   tecnologia; links para as páginas de case.
5. **Experiência** — timeline SENAI CETIND (Analista 2022– · Programador 2015–2022 ·
   Estagiário 2013–2015) + formação (UNIFACS, SENAI Bahia).
6. **Contato** — e-mail, LinkedIn, GitHub, localização.

## Páginas de case

- `/flow/` — o problema (produção de EAD dispersa), o fluxo entre os nove
  perfis de produção, o editor por seções, o assistente de IA (SSE + contexto
  com hash), a exportação (SCORM 1.2, PDF, DOCX, IDML), o papel do Paulo e a
  stack. Conteúdo extraído do README do próprio sistema
  (`/var/www/html/flow_2/README.md`); as capturas vêm do manual do Especialista
  Técnico, de um ambiente de demonstração. As notas de segurança do README
  **não** vão para o site.
- `/moodle/` — o escopo do trabalho com Moodle (administração, plugins, temas,
  integrações, SCORM, relatórios, migração de versão) e os três AVAs
  (ObsPLE-PL2, (Re)Integro, Cruzando Fronteiras) com prints.

## Sistema visual

Custom properties em `:root`, redefinidas em `[data-theme="dark"]` e sob
`@media (prefers-color-scheme: dark)`.

Claro:
- fundo `#F7F5F0` (off-white) · superfície `#FFFFFF`
- verde musgo `#4F5D3F`, escuro `#3A4630`, claro `#7A8A66`
- laranja `#B05023` (acento em texto; escurecido do #D9622B para passar 4.5:1 sobre off-white)
- laranja vivo `#D9622B` só em elemento decorativo não textual (`--accent-deco`)
- borda de controle `#8E897D` (`--border-ctrl`, ≥3:1 — botões, filtros, seletor de idioma)
- tinta `#26281F`

Escuro:
- fundo `#161A14` · superfície `#1F241C`
- texto `#F0EEE8` · verde claro `#A9BA8E`
- laranja `#F08A4B`
- borda de controle `#6F7667`

Todos os pares texto/fundo devem ser verificados em ≥4.5:1 (texto normal) e
≥3:1 (texto grande e bordas de foco) antes de concluir.

Tipografia: Inter (texto) + JetBrains Mono (tags, números, rótulos).
Laranja é acento apenas: links, hover, foco, um detalhe por bloco.

## Interação e animação

- Nav sticky com scrollspy via `IntersectionObserver`; indicador desliza.
- Reveal ao entrar na viewport (fade + translateY, stagger por filho).
- Contadores animados na faixa de números, disparando uma única vez.
- Filtro de habilidades com transição de entrada/saída dos chips.
- Transição entre páginas com View Transitions API quando disponível.
- Menu hambúrguer abaixo de 768px, com foco preso enquanto aberto.
- Preferência de tema persistida em `localStorage`, dentro de try/catch.
- `@media (prefers-reduced-motion: reduce)` neutraliza todas as animações.

## SEO

- `<title>` e `description` únicos por página.
- `canonical` absoluto em `https://paulo.ambrosi.top/...`.
- `hreflang` pt-BR ⇄ en ⇄ x-default em todas as seis páginas.
- Open Graph + Twitter Card com `og-image.png` 1200×630.
- JSON-LD: `Person` (com `knowsAbout`, `alumniOf`, `worksFor`, `sameAs`) na home;
  `CreativeWork` nas páginas de case.
- `sitemap.xml` com as seis URLs; `robots.txt` liberando tudo e apontando o sitemap.
- HTML semântico (`header`/`nav`/`main`/`section`/`article`/`footer`), um `h1`
  por página, skip-link, `alt` em todas as imagens, `width`/`height` e
  `loading="lazy"` nas que estão abaixo da dobra.

## Prints do Moodle

Slots prontos com placeholder SVG marcado. Captura posterior: o usuário faz o
login no navegador e passa o controle; a navegação e a captura são feitas sem
que nenhuma credencial passe pelo assistente. Telas com nome de aluno são
descartadas ou borradas; preferência por telas administrativas.

## Fora de escopo

- Formulário de contato (exigiria backend ou serviço de terceiros).
- Blog, CMS, analytics.
- Terceiro idioma.
- Geração de PDF do currículo (já existe no repo `cv`).

## Critérios de conclusão

- As seis páginas abrem sem erro de console e sem requisição quebrada.
- Navegação, filtros, tema e animações funcionam; `prefers-reduced-motion` respeitado.
- Contraste verificado nos dois temas.
- Layout íntegro em 360px, 768px e 1440px.
- `sitemap.xml` e `hreflang` consistentes com os arquivos reais.
- `CNAME` intacto na raiz.
