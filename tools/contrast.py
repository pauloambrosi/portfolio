#!/usr/bin/env python3
"""Verifica o contraste dos pares de cor usados no site (WCAG 2.2)."""

def lum(hexc):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

LIGHT = dict(bg="#F7F5F0", bg_tint="#F1EEE6", surface="#FFFFFF", surface2="#F1EEE6",
             ink="#22261C", ink_muted="#59604E", moss="#4F5D3F", moss_soft="#7A8A66",
             moss_wash="#E8EADF", accent="#B05023", accent_hover="#94431D",
             border_ctrl="#8E897D", feature_bg="#4F5D3F", feature_ink="#FFFFFF",
             feature_muted="#DDE3D1", feature_accent="#FFC299")
DARK = dict(bg="#161A14", bg_tint="#1C211A", surface="#1F241C", surface2="#272D23",
            ink="#F0EEE8", ink_muted="#A9B19B", moss="#A9BA8E", moss_soft="#8A9B70",
            moss_wash="#262D20", accent="#F08A4B", accent_hover="#F8A873",
            border_ctrl="#6F7667", feature_bg="#2C3623", feature_ink="#F2F0EA",
            feature_muted="#BDC8AC", feature_accent="#F49A62")

# (rótulo, cor de frente, cor de fundo, mínimo exigido)
def checks(t):
    return [
        ("texto sobre fundo",            t["ink"],         t["bg"],         4.5),
        ("texto sobre fundo tonalizado", t["ink"],         t["bg_tint"],    4.5),
        ("texto sobre superfície",       t["ink"],         t["surface"],    4.5),
        ("texto secundário / fundo",     t["ink_muted"],   t["bg"],         4.5),
        ("texto secundário / tonalizado",t["ink_muted"],   t["bg_tint"],    4.5),
        ("texto secundário / superfície",t["ink_muted"],   t["surface"],    4.5),
        ("link laranja / fundo",         t["accent"],      t["bg"],         4.5),
        ("link laranja / tonalizado",    t["accent"],      t["bg_tint"],    4.5),
        ("link laranja / superfície",    t["accent"],      t["surface"],    4.5),
        ("eyebrow musgo / fundo",        t["moss"],        t["bg"],         4.5),
        ("eyebrow musgo / tonalizado",   t["moss"],        t["bg_tint"],    4.5),
        ("musgo sobre moss-wash",        t["moss"],        t["moss_wash"],  4.5),
        ("destaque: texto",              t["feature_ink"], t["feature_bg"], 4.5),
        ("destaque: texto secundário",   t["feature_muted"],t["feature_bg"],4.5),
        ("destaque: acento",             t["feature_accent"],t["feature_bg"],4.5),
        ("borda de foco / fundo",        t["accent"],      t["bg"],         3.0),
        ("borda de controle / fundo",    t["border_ctrl"], t["bg"],         3.0),
        ("borda de controle / superfície",t["border_ctrl"],t["surface2"],  3.0),
        ("traço musgo claro / fundo",    t["moss_soft"],   t["bg"],         3.0),
    ]

fail = 0
for name, t in (("CLARO", LIGHT), ("ESCURO", DARK)):
    print(f"\n=== tema {name} ===")
    for label, fg, bg, need in checks(t):
        r = ratio(fg, bg)
        ok = r >= need
        if not ok:
            fail += 1
        print(f"  {'ok  ' if ok else 'FALHA'} {r:5.2f}:1  (mín {need})  {label}  {fg} sobre {bg}")

print(f"\n{fail} par(es) abaixo do mínimo" if fail else "\ntodos os pares passam")
raise SystemExit(1 if fail else 0)
