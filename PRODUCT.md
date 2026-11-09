# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: **clients and companies** (managers, business owners, teams) looking for someone to build a digital product or to integrate AI into management systems, automation, or AI agents, as a project or a consultancy. They arrive from LinkedIn, a referral, or a search, and they want to know quickly whether Paulo can deliver what they need.

Recruiters and tech leads still visit, but they come second. The site is bilingual (pt-BR and en), so Brazilian and international visitors are both expected.

## Product Purpose

Personal portfolio of Paulo Ambrosi at https://paulo.ambrosi.top. Its job is to convince a prospective client that Paulo builds digital products with AI inside, and then get them to make contact.

**Success = the visitor sends an email or messages him on LinkedIn.** The case pages (FLOW, SENAI Class, IA, Moodle) are the proof that makes that contact happen. They are not the goal.

## Positioning

**End-to-end product delivery.** Paulo builds, deploys, and maintains products on his own: architecture, backend, frontend, AI integration, deployment, and the final exported artifact (for example SCORM 1.2/2004). FLOW and SENAI Class are real, working examples of this.

Emphasis order, decided 2026-11-06: digital products and AI solutions come first (AI integrated with management systems and automation, AI agents). Virtual learning environments and educational technology come second. Moodle, the experience section, and the tags were not reframed, at his request.

## Operating Context

- Visitors usually come from LinkedIn or a direct link, often on a phone.
- Sharing previews matter: the og-image and the title/description are what show up on LinkedIn.
- There is a light/dark theme toggle and a pt-BR/en language switch on every page.

## Capabilities and Constraints

- Static site on GitHub Pages (`main` branch, repo root). No backend, no build step, no installed dependencies: HTML5, CSS3, vanilla JS. The only external request is Google Fonts, with a system fallback.
- `CNAME` (`paulo.ambrosi.top`) must stay at the root. Canonical URLs and the sitemap always use the domain.
- Nine pages: home, `flow/`, `moodle/`, `ia/`, their `en/` mirrors, and `404.html`. Every pt-BR change is mirrored in en.
- `css/styles.css` and `js/main.js` are cache-busted with `?v=AAAAMMDD` across every HTML file.
- `tools/check.py` (site validator) and `tools/contrast.py` (WCAG contrast) run before each push.
- Contact channels are **email and LinkedIn only**. No phone number, to avoid spam. The validator fails if the number appears again.
- Open: the four Moodle screenshot slots still use `assets/moodle/placeholder.svg` until real captures are taken.

## Brand Commitments

- Name: Paulo Ambrosi. Headline: "Produtos Digitais e Soluções com IA".
- Voice: first person, plain verbs about real work ("Construo, implemento e testo produtos digitais."). The hero cycles these phrases through `data-typer` / `data-phrases`, with a screen-reader copy next to it.
- Recurring idea: "IA que propõe e uma pessoa decide". The AI suggests and a person makes the final call.

## Evidence on Hand

- Biography, experience, education, and projects come from the `pauloambrosi/cv` repo (pt-BR `index.html`, en `en.html`). 12+ years of experience at SENAI Bahia.
- FLOW case: drawn from the system's README. Screenshots are in `assets/flow/` and come from a demo environment ("Ana Conteudista (demo)", "UC-DEMO").
- SENAI Class: screenshots are in `assets/senaiclass/`.
- AI page (`ia/`): taken directly from the FLOW and SENAI Class code. Assistant over SSE, assisted proofreading with a diff, personalized assessment, question generation, open-answer grading reviewed by the teacher, image generation. Plus his own AI-assisted development setup (`CLAUDE.md` files, code graph, spec-driven development, hooks).
- ObsPLE-PL2: "1000+" students ("mais de mil" in running text) and 4 course editions.
- Moodle screenshots are in `assets/moodle-prints/`.
- **Absent, must not be fabricated:** client testimonials, client logos, prices, external metrics beyond the ones above. Never publish secrets, internal paths, server IPs, student data, or the security notes from the FLOW README. The skills in `flow_2/.claude/skills/` came with a plugin and must not be credited to him.

## Product Principles

1. **Proof before promise.** Every claim is backed by a real system, screenshot, or number from the sources above. Nothing is invented.
2. **Contact is the destination.** Every page leaves a short, obvious path to email or LinkedIn.
3. **Products first, education second.** Lead with digital products and AI. EAD/Moodle supports the story.
4. **One person, whole product.** Show the full chain of delivery, not isolated skills.
5. **Bilingual parity.** pt-BR and en say the same thing.

## Accessibility & Inclusion

WCAG 2.2 AA, checked with `tools/contrast.py` in both themes. Typed and animated content always has a static text equivalent for screen readers. Reduced motion is respected.
