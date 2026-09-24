import sys, os, json, re, importlib, datetime, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import Builder, compile_tokens_css, type_groups, EN, ZH
from contrast import cr

def build(key):
    K = importlib.import_module(f"concept_{key.lower()}")
    root = f"out/{key}"
    if os.path.exists(root): shutil.rmtree(root)
    os.makedirs(f"{root}/project/components", exist_ok=True)
    tok = {"name": K.TITLE, "version": 1,
      "color": {"themes": [{"id": "light", "name": "Light"}],
                "tokens": [{"name": n, "value": v, "usage": u} for n, v, u in K.COLORS]},
      "type": {"fonts": [], "families": K.FAMILY_STACKS, "groups": type_groups(K.TYPE, None)},
      "spacing": {"tokens": [{"name": a, "value": b, "usage": c} for a, b, c in SPACING]},
      "layout": {"note": "Page width and column grid.", "tokens": [{"name": a, "value": b, "usage": c} for a, b, c in LAYOUT]},
      "radius": {"tokens": [{"name": a, "value": b, "usage": c} for a, b, c in K.RADIUS]},
      "border": {"tokens": [{"name": "border-hairline", "value": "1px", "usage": "Card outlines and dividers (`border`)."},
                            {"name": "border-control", "value": "1.5px", "usage": "Control edges: secondary button, fields, chips."},
                            {"name": "focus-width", "value": "3px", "usage": "Keyboard focus ring width, 3px offset."}]},
      "shadow": {"tokens": [{"name": a, "value": b, "usage": c} for a, b, c in K.SHADOWS]},
    }
    for k, v in getattr(K, "EXTRA_FAMILIES", {}).items(): tok[k] = v
    json.dump(tok, open(f"{root}/project/tokens.json", "w"), ensure_ascii=False, indent=1)
    open(f"{root}/tokens.local.css", "w").write(compile_tokens_css(tok))
    open(f"{root}/project/components/bundle.css", "w").write(
        f"/* 1234 Ortho-K Vision Care — {K.TITLE}. Structure is shared by concepts B–D; the skin below it is this concept's. */\n"
        + open("base.css").read() + K.CSS)
    B = Builder(K)
    B.catalogue(tok, cr)
    B.write(root)
    open(f"{root}/project/README.md", "w").write(readme(K, tok))
    cov = K.cover()
    os.makedirs(f"{root}/project/components/Cover", exist_ok=True); os.makedirs(f"{root}/local/Cover", exist_ok=True)
    open(f"{root}/project/components/Cover/preview.html", "w").write(cov)
    open(f"{root}/local/Cover/preview.html", "w").write(cov.replace("</head>", '<link rel="stylesheet" href="../../tokens.local.css"></head>').replace("<html lang", '<html data-theme="light" lang'))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump({"v": 3, "layout": "files", "createdOnFiles": {"v": 1, "at": now}, "title": K.TITLE, "namespace": K.NAMESPACE, "libraries": [],
               "sections": {}, "groups": [], "assetGroups": {}, "blobs": {}, "docs": {"readme": "project/README.md", "sections": []},
               "lastChange": {"by": "Jimmy", "at": now, "via": "Cowork", "note": f"{K.TITLE}: design system, EN + 繁體 homepages, desktop + mobile"}},
              open(f"{root}/project/design-system.json", "w"), ensure_ascii=False, indent=1)
    files = {}
    for r, _, fs in os.walk(f"{root}/project"):
        for f in fs:
            p = os.path.relpath(os.path.join(r, f), root)
            if p != "project/design-system.json": files[p] = p
    json.dump(files, open(f"{root}/files.json", "w"), ensure_ascii=False)
    # standalone exports
    tcss = open(f"{root}/tokens.local.css").read(); bcss = open(f"{root}/project/components/bundle.css").read()
    for src, name in (("Homepage desktop EN", "EN"), ("Homepage Traditional Chinese desktop", "zh-Hant")):
        h = open(f"{root}/project/components/{src}/preview.html").read().split("\n", 1)[1]
        h = h.replace("</head>", f"<style>{tcss}\n{bcss}</style></head>").replace(f"<title>{src}</title>", f"<title>1234 Ortho-K · Concept {key}</title>")
        open(f"{root}/Concept{key}-{K.NAME.replace(' ', '').replace('-', '')}-homepage-{name}.html", "w").write(h)
    print(key, len(B.comps), "cards,", len(files), "files")
    return root

SPACING = [("space-0-5", "4px", "Icon to label inside chips."), ("space-1", "8px", "Base unit."), ("space-2", "16px", "Inside fields and chips; gap between buttons."),
           ("space-3", "24px", "Card padding (mobile); grid gutter (desktop)."), ("space-4", "32px", "Card padding (desktop); gap between cards."),
           ("space-6", "48px", "Heading to content on desktop."), ("space-8", "64px", "Section padding on mobile."), ("space-10", "80px", "Section padding on desktop."), ("space-12", "96px", "Large hero spacing.")]
LAYOUT = [("page-max", "1120px", "Content max width, 24px side padding on desktop."), ("reading-max", "680px", "Max width of paragraphs and FAQ answers."),
          ("gutter-mobile", "20px", "Side margin on phones."), ("grid-desktop", "12", "12 columns, 24px gutter (≥1024px)."),
          ("grid-tablet", "8", "8 columns, 24px gutter (768–1023px)."), ("grid-mobile", "4", "4 columns, 16px gutter (<768px).")]

def readme(K, tok):
    col = {t["name"]: t for t in tok["color"]["tokens"]}
    clean = lambda u: re.sub(r'^[A-Z][A-Z ()]+ · [A-Za-z -]+\. ', '', re.sub(r'^[A-Z][A-Z ()]+\. ', '', u))
    roles = "\n".join(f"| {l} | `{n}` | {col[n]['value']} | {clean(col[n]['usage'])} |" for n, l in K.ROLES)
    fams = "\n".join(f"| {r} | **{n}** | {note} |" for r, k, n, w, note in K.FAMILIES)
    ts = "\n".join(f"| {n.upper() if n[0]=='h' else n.title()} | {ed} / {em} | {zd} / {zm} | {el} · {zl} |" for n, ed, em, el, ew, zd, zm, zl, zw, se, sz in K.TYPE)
    rad = " · ".join(f"`{a}` {b}" for a, b, c in K.RADIUS)
    comps = " · ".join(["Primary button", "Secondary button", "Language switcher", "Top navigation + mobile menu", "Hero block", "3-step How it works block", "Doctor card", "FAQ accordion", "Booking call-to-action band", "Location card", "Contact row", "Form field set", "Footer"])
    extras = " · ".join(n for n, *_ in K.extras(Builder(K)))
    strip = lambda s: s.split("\n\n", 1)[1] if "\n\n" in s else s
    v = K.VOICE
    return f"""**1234 Ortho-K Vision Care · 1234兒童視力矯正中心** — website design concept {K.KEY} of four. {K.INTRO}

No logo is designed here. The header shows the plain text **1234 Ortho-K Vision Care** in the English heading font; Chinese pages add **1234兒童視力矯正中心** beneath it. Logo and identity are a separate project.

## 1. Color

{strip(K.README_COLOR)}

| Role | Token | Hex | Use |
|---|---|---|---|
{roles}

{K.COLOR_RULES}

## 2. Typography

| Role | Family | Notes |
|---|---|---|
{fams}

Type scale — desktop / mobile (mobile below 768px):

| Level | English px | 繁體中文 px | Line height EN · 中 |
|---|---|---|---|
{ts}

{K.TYPE_RULES}

## 3. Spacing & Layout

- Spacing steps on 8px: `space-0-5` 4 · `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-10` 80 · `space-12` 96.
- Page max width **1120px** (`page-max`); paragraphs and FAQ answers max **680px** (`reading-max`).
- Desktop ≥1024px: **12 columns**, 24px gutter. Tablet: 8 columns. Mobile <768px: **4 columns**, 16px gutter, 20px side margins.
- {K.SECTION_RHYTHM.replace('<code>','`').replace('</code>','`')}

## 4. Shape

- Radius: {rad}.
- {K.SHAPE_RULES}

## 5. Components

In this order: **{comps}.** Concept {K.KEY} extras: **{extras}.**

- Every interactive component shows default, hover and pressed; keyboard focus is always a solid 3px ring.
- Booking is the only primary action; Message us is always the secondary button beside it.
- Mobile keeps **Book a consultation** and **Message us** in a sticky bottom bar, because the clinic is open only a few days a week.
- Placeholders look like placeholders: dashed boxes for app icons, "Placeholder copy" tags, "coming soon" for Walnut.

## 6. Icons

{strip(K.README_ICONS)} The six sample icons: eye · moon · sun · calendar · phone · question. The same set also covers message, pin, lens, clock, map, camera, check, alert, menu, close, arrow. WeChat, LINE and WhatsApp use each company's official mark (dashed placeholders until then).

## 7. Imagery

{K.IMAGERY_RULES}

## 8. Voice & Tone

**{' · '.join(v['words'])}** — {strip(K.README_VOICE)}

- Right: "{v['right_en']}" / 「{v['right_zh']}」
- Wrong: "{v['wrong_en']}" / 「{v['wrong_zh']}」

Never add statistics, success rates, patient counts, or "best" / "most effective" claims.

## Homepage

Four live cards at the end: desktop (1280px) and mobile (390px), in English and Traditional Chinese, built only from these components. Section order is identical in all four concepts: header → hero → the problem → how ortho-k works → meet the doctor → first visit → parent questions → book + locations → booking band → footer.
"""

if __name__ == "__main__":
    for k in sys.argv[1:]: build(k)
