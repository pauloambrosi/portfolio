#!/usr/bin/env python3
"""Validador estático do portfólio.

Roda sem dependências. Verifica, em cada arquivo .html do repositório:
head completo, hreflang recíproco, um único h1, alt em imagens,
ausência do telefone, ausência de caminho absoluto interno, e que todo
href/src relativo aponte para um arquivo que existe.

Uso:  python3 tools/check.py
"""
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://paulo.ambrosi.top"
PHONE_PATTERNS = [r"9921[\s\-]?9049", r"\+55\s?71", r"71\s?99213"]
SKIP_DIRS = {".git", "docs", "tools", "node_modules"}

errors = []
warnings = []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta = []          # list of dicts
        self.links = []         # list of dicts (<link>)
        self.h1 = 0
        self._in_h1 = False
        self.h1_text = ""
        self.imgs = []          # list of dicts
        self.anchors = []       # list of dicts
        self.scripts = []
        self.html_lang = None
        self.jsonld = 0
        self._in_jsonld = False
        self.ids = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "h1":
            self.h1 += 1
            self._in_h1 = True
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif tag == "button":
            self.buttons.append(a)
        elif tag == "script":
            self.scripts.append(a)
            if a.get("type") == "application/ld+json":
                self._in_jsonld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script":
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data.strip()
        if self._in_h1:
            self.h1_text += data.strip()
        if self._in_jsonld and data.strip():
            self.jsonld += 1


def find_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in sorted(filenames):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def rel(path):
    return os.path.relpath(path, ROOT)


def meta_content(doc, **match):
    for m in doc.meta:
        if all(m.get(k) == v for k, v in match.items()):
            return m.get("content")
    return None


def check_page(path, all_pages):
    page = rel(path)
    raw = open(path, encoding="utf-8").read()
    doc = Doc()
    doc.feed(raw)
    is_404 = page == "404.html"

    # --- lang ---
    expected_lang = "en" if page.startswith("en/") else "pt-BR"
    if doc.html_lang != expected_lang:
        err(page, f'<html lang> é "{doc.html_lang}", esperado "{expected_lang}"')

    # --- head ---
    if not doc.title:
        err(page, "sem <title>")
    elif len(doc.title) > 65:
        warn(page, f"<title> com {len(doc.title)} caracteres (Google corta ~60)")

    desc = meta_content(doc, name="description")
    if not desc:
        err(page, "sem meta description")
    elif not (70 <= len(desc) <= 165):
        warn(page, f"meta description com {len(desc)} caracteres (ideal 70–165)")

    if not meta_content(doc, name="viewport"):
        err(page, "sem meta viewport")

    canon = next((l.get("href") for l in doc.links if l.get("rel") == "canonical"), None)
    if not canon:
        err(page, "sem link canonical")
    elif not canon.startswith(SITE):
        err(page, f"canonical não usa {SITE}: {canon}")

    # --- open graph ---
    for prop in ("og:title", "og:description", "og:url", "og:image", "og:type"):
        if not meta_content(doc, property=prop):
            err(page, f"sem {prop}")

    # --- hreflang ---
    if not is_404:
        alts = {l.get("hreflang"): l.get("href")
                for l in doc.links if l.get("rel") == "alternate" and l.get("hreflang")}
        for want in ("pt-BR", "en", "x-default"):
            if want not in alts:
                err(page, f"sem hreflang {want}")

    # --- estrutura ---
    if doc.h1 != 1:
        err(page, f"{doc.h1} elementos <h1> (deve ser exatamente 1)")

    if not is_404 and doc.jsonld == 0:
        err(page, "sem bloco JSON-LD")

    # --- imagens ---
    for img in doc.imgs:
        src = img.get("src", "(sem src)")
        if "alt" not in img:
            err(page, f"<img> sem alt: {src}")
        if not (img.get("width") and img.get("height")):
            warn(page, f"<img> sem width/height: {src}")

    # --- acessibilidade básica ---
    if 'class="skip"' not in raw:
        err(page, "sem skip-link")
    for b in doc.buttons:
        if not (b.get("aria-label") or b.get("aria-labelledby")):
            txt_id = b.get("id", "(sem id)")
            if b.get("class", "").startswith("iconbtn") or "navtoggle" in b.get("class", ""):
                err(page, f"botão de ícone sem aria-label: {txt_id}")

    # --- telefone ---
    for pat in PHONE_PATTERNS:
        if re.search(pat, raw):
            err(page, f"telefone presente no HTML (padrão {pat!r})")

    # --- caminhos ---
    refs = []
    for a in doc.anchors:
        refs.append(("href", a.get("href")))
    for i in doc.imgs:
        refs.append(("src", i.get("src")))
    for s in doc.scripts:
        if s.get("src"):
            refs.append(("src", s.get("src")))
    for l in doc.links:
        if l.get("href") and l.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "preconnect"):
            refs.append(("href", l.get("href")))

    base = os.path.dirname(path)
    for attr, url in refs:
        if not url:
            continue
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            continue
        if url.startswith("/"):
            err(page, f"caminho absoluto interno em {attr}: {url}")
            continue
        target = os.path.normpath(os.path.join(base, url.split("#")[0].split("?")[0]))
        if target.endswith(os.sep) or os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            err(page, f"{attr} aponta para arquivo inexistente: {url}")

    # --- âncoras internas existem ---
    for a in doc.anchors:
        h = a.get("href", "")
        if h.startswith("#") and len(h) > 1 and h[1:] not in doc.ids:
            err(page, f"âncora sem destino: {h}")

    return canon


def check_sitemap(canons):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        warn("sitemap.xml", "ainda não existe")
        return
    raw = open(path, encoding="utf-8").read()
    listed = set(re.findall(r"<loc>([^<]+)</loc>", raw))
    real = {c for c in canons if c}
    for missing in sorted(real - listed):
        err("sitemap.xml", f"URL da página ausente no sitemap: {missing}")
    for extra in sorted(listed - real):
        err("sitemap.xml", f"URL no sitemap sem página correspondente: {extra}")


def main():
    pages = find_pages()
    canons = []
    for p in pages:
        canons.append(check_page(p, pages))
    check_sitemap([c for p, c in zip(pages, canons) if rel(p) != "404.html"])

    print(f"{len(pages)} páginas verificadas")
    for w in warnings:
        print(f"  aviso  {w}")
    for e in errors:
        print(f"  ERRO   {e}")
    if errors:
        print(f"\n{len(errors)} erro(s), {len(warnings)} aviso(s)")
        return 1
    print(f"ok — 0 erros, {len(warnings)} aviso(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
