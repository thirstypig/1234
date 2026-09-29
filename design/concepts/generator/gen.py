import os, json, re, html
from content import EN, ZH
OUT = "project/components"
FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">'
E = lambda e: f'<span class="nb-emoji" aria-hidden="true">{e}</span>'

def doc(title, body, marker, lang="en", script=""):
    return f"""{marker}
<!doctype html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>{FONT_LINK}
<style>html,body{{margin:0;background:var(--background)}}</style>
</head>
<body>
{body}
{('<script>'+script+'</script>') if script else ''}
</body>
</html>
"""

THEME_JS = """document.querySelectorAll('[data-nb-theme]').forEach(function(b){b.addEventListener('click',function(){var r=document.documentElement,n=r.getAttribute('data-theme')==='night'?'day':'night';r.setAttribute('data-theme',n);document.querySelectorAll('[data-nb-theme]').forEach(function(x){x.setAttribute('aria-pressed',n==='night');var l=x.querySelector('[data-l]');if(l)l.textContent=n==='night'?x.dataset.day:x.dataset.night;var i=x.querySelector('.nb-emoji');if(i)i.textContent=n==='night'?'☀️':'🌙';});});});"""
MENU_JS = """document.querySelectorAll('[data-nb-menu]').forEach(function(b){b.addEventListener('click',function(){var s=document.getElementById(b.getAttribute('aria-controls'));var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',!o);s.hidden=o;});});"""

# ---------- building blocks ----------
def lang_switch(cur="en", cls=""):
    items=[("en","EN","en"),("zh-Hans","简体","zh-Hans"),("zh-Hant","繁體","zh-Hant")]
    out=[]
    for i,(k,t,hl) in enumerate(items):
        ac=' aria-current="page"' if k==cur else ''
        out.append(f'<a href="#" hreflang="{hl}" lang="{hl}"{ac} class="{cls if k!=cur else ""}">{t}</a>')
    return '<nav class="nb-lang" aria-label="Language / 語言">'+'<span class="nb-lang-sep" aria-hidden="true">/</span>'.join(out)+'</nav>'

def toggle(c, icon_only=False, state=""):
    if icon_only:
        return f'<button type="button" class="nb-toggle nb-toggle--icon {state}" data-nb-theme data-day="{c["day"]}" data-night="{c["night"]}" aria-pressed="false" aria-label="{c["night"]} / {c["day"]}">{E("🌙")}</button>'
    return f'<button type="button" class="nb-toggle {state}" data-nb-theme data-day="{c["day"]}" data-night="{c["night"]}" aria-pressed="false">{E("🌙")}<span data-l>{c["night"]}</span></button>'

def btn(label, kind="primary", emoji=None, extra="", href="#"):
    em = E(emoji) if emoji else ""
    return f'<a href="{href}" class="nb-btn nb-btn--{kind} {extra}">{em}<span>{label}</span></a>'

def header(c, cur):
    links="".join(f'<a href="{h}">{t}</a>' for h,t in c["nav"])
    brand=f'<a class="nb-brand" href="#">{c["brand"]}'+(f'<small lang="zh-Hant">{c["brand_zh"]}</small>' if c["brand_zh"] else '')+'</a>'
    return f'''<div class="nb-utility"><div class="nb-wrap nb-utility-in">{lang_switch(cur)}{toggle(c, icon_only=True)}</div></div>
<header class="nb-header"><div class="nb-wrap nb-header-in">{brand}
<nav class="nb-nav" aria-label="Main">{links}</nav>
<div class="nb-header-tools">{btn(c["book"],"primary",None,"nb-btn--sm")}
<button type="button" class="nb-btn nb-btn--secondary nb-btn--sm nb-menu-btn" data-nb-menu aria-expanded="false" aria-controls="nb-menu-{c['lang']}">☰ {c["menu"]}</button></div></div>
<div class="nb-wrap" id="nb-menu-{c['lang']}" hidden style="padding-bottom:16px">{sheet(c)}</div></header>'''

def sheet(c):
    links="".join(f'<li><a href="{h}">{t}<span aria-hidden="true">→</span></a></li>' for h,t in c["nav"])
    return f'''<div class="nb-sheet"><ul class="nb-sheet-links">{links}</ul>
<div class="nb-sheet-foot nb-stack">{btn(c["book"],"primary","📅","nb-btn--block")}{btn(c["message"],"secondary","💬","nb-btn--block")}</div></div>'''

def hero(c):
    trust="".join(f'<li>{E(e)}<span>{t}</span></li>' for e,t in c["trust"])
    return f'''<section class="nb-hero"><div class="nb-wrap nb-hero-grid">
<div><p class="nb-eyebrow">{E("👀")} {c["eyebrow"]}</p>
<h1 class="nb-display">{c["hero_h"]}</h1>
<p class="nb-lead">{c["hero_sub"]}</p>
<div class="nb-btn-row">{btn(c["book"],"primary","📅")}{btn(c["message"],"secondary","💬")}</div></div>
<aside class="nb-note" aria-label="{c['trust_title']}"><p class="nb-note-title">{c["trust_title"]}</p><ul class="nb-checks" style="margin-top:8px">{trust}</ul></aside>
</div></section>'''

def problem(c):
    return f'''<section class="nb-section"><div class="nb-wrap nb-grid">
<h2 class="nb-h1 nb-span-6">{c["prob_h"]}</h2>
<p class="nb-lead nb-at-8">{c["prob_b"]}</p></div></section>'''

def steps_block(c, current=None):
    items=""
    for i,(e,t) in enumerate(c["steps"],1):
        cur=' is-current' if current==i else ''
        items+=f'<li class="nb-step{cur}"><div class="nb-step-top"><span class="nb-step-num">{c["step_word"]} {i}</span>{E(e)}</div><h3 class="nb-h3">{t}</h3></li>'
    return f'<ol class="nb-steps">{items}</ol>'

def how(c):
    return f'''<section class="nb-section" id="how"><div class="nb-wrap"><h2 class="nb-h2" style="margin-bottom:var(--space-6)">{c["how_h"]}</h2>{steps_block(c)}</div></section>'''

def doctor_card(c):
    chips="".join(f'<li class="nb-chip">{E("💬")}{l}</li>' for l in c["langs"])
    lines="".join(f'<p class="nb-lead">{l}</p>' for l in c["doc_lines"])
    return f'''<div class="nb-doctor"><figure class="nb-photo" role="img" aria-label="{c['photo']}"><div>{E("📷")}{c["photo"]}</div></figure>
<div class="nb-stack-lg"><p class="nb-eyebrow">{E("👀")} {c["doc_eyebrow"]}</p><h2 class="nb-h1">{c["doc_name"]}</h2>{lines}<ul class="nb-chips" aria-label="Languages">{chips}</ul>
<div class="nb-btn-row">{btn(c["book"],"primary","📅")}</div></div></div>'''

def visit(c):
    lis="".join(f'<li><span class="nb-n">{i}</span><p class="nb-body">{t}</p></li>' for i,t in enumerate(c["visit"],1))
    return f'''<section class="nb-section" id="visit"><div class="nb-wrap nb-grid">
<div class="nb-span-5"><h2 class="nb-h2">{c["visit_h"]}</h2><p style="margin-top:var(--space-2)"><span class="nb-draft">{c["draft"]}</span></p></div>
<ol class="nb-lines nb-at-7">{lis}</ol></div></section>'''

def faq_block(c, open_idx=0, hover_idx=None):
    out=""
    for i,q in enumerate(c["faqs"]):
        o=' open' if i==open_idx else ''
        h=' class="is-hover"' if i==hover_idx else ''
        out+=f'<li><details{o}><summary{h}>{E("❓")}<span>{q}</span><span class="nb-plus" aria-hidden="true"></span></summary><div class="nb-answer"><p class="nb-body">{c["faq_a"]}</p></div></details></li>'
    return f'<ul class="nb-faq">{out}</ul>'

def faq(c):
    return f'''<section class="nb-section" id="faq"><div class="nb-wrap"><div class="nb-reading" style="max-width:840px;margin:0 auto"><h2 class="nb-h2" style="margin-bottom:var(--space-4)">{c["faq_h"]}</h2>{faq_block(c)}</div></div></section>'''

def contact_row(c, hover=None, pressed=None):
    out=""
    for i,(ic,label,sub) in enumerate(c["contact"]):
        st=' is-hover' if i==hover else (' is-pressed' if i==pressed else '')
        ico = f'<span class="nb-ico">{E(ic)}</span>' if len(ic)<=2 and not ic.isascii() else f'<span class="nb-ico nb-ico--ph" title="App icon placeholder">{ic}</span>'
        s=f'<small>{sub}</small>' if sub else ''
        out+=f'<li><a href="#" class="{st.strip()}">{ico}<span>{label}{s}</span></a></li>'
    return f'<ul class="nb-contact" aria-label="Contact">{out}</ul>'

def loc_card(c, key):
    L=c[key]; soon = key=="walnut"
    addr_cls=' nb-soon' if soon else ''
    btns = (btn(c["book_here"],"primary","📅","nb-btn--sm")+btn(c["directions"],"secondary",None,"nb-btn--sm")) if not soon else f'<span class="nb-btn nb-btn--secondary nb-btn--sm is-disabled" aria-disabled="true">{c["soon_btn"]}</span>'
    return f'''<article class="nb-loc"><div class="nb-map" role="img" aria-label="{c['map']}: {L['name']}">{E("📍")} {c["map"] if not soon else c["map_soon"]}</div>
<div class="nb-loc-body"><div class="nb-loc-name"><h3 class="nb-h3">{L["name"]}</h3><span class="nb-zh" lang="{'en' if c['lang']=='zh' else 'zh-Hant'}">{L["zh"]}</span></div>
<div class="nb-kv"><span class="nb-emoji">📍</span><p class="nb-body{addr_cls}">{L["addr"]}</p></div>
<div class="nb-kv"><span class="nb-emoji">📅</span><p class="nb-body{addr_cls}">{L["hours"]}</p></div>
<div class="nb-kv"><span class="nb-emoji">📞</span><p class="nb-body">{c["phones"]}</p></div>
<div class="nb-btn-row">{btns}</div></div></article>'''

def locations(c):
    return f'''<section class="nb-section" id="locations"><div class="nb-wrap nb-stack-lg">
<h2 class="nb-h1">{c["loc_h"]}</h2>
<p class="nb-note-title">{c["contact_title"]}</p>{contact_row(c)}
<div class="nb-locs" style="margin-top:var(--space-4)">{loc_card(c,"alhambra")}{loc_card(c,"walnut")}</div></div></section>'''

def band(c):
    return f'''<div class="nb-band"><div><h2 class="nb-h2">{c["band_h"]}</h2><p class="nb-body" style="color:var(--text-secondary)">{c["band_b"]}</p></div>
<div class="nb-btn-row">{btn(c["book"],"primary","📅")}{btn(c["message"],"secondary","💬")}</div></div>'''

def footer(c, cur):
    A,W=c["alhambra"],c["walnut"]
    legal="".join(f'<a href="#">{l}</a>' for l in c["legal"])
    return f'''<footer class="nb-footer"><div class="nb-wrap"><div class="nb-footer-grid">
<div><p class="nb-brand" style="font-size:19px">{c["brand"]}</p><p style="margin-top:4px" lang="zh-Hant">1234兒童視力矯正中心</p><div style="margin-top:var(--space-2)"><h3>{c["footer_langs"]}</h3>{lang_switch(cur)}</div></div>
<div><h3>{A["name"]}</h3><p>{A["addr"]}<br>{A["hours"]}</p></div>
<div><h3>{W["name"]}</h3><p>{W["addr"]}<br>{W["hours"]}</p></div>
<div><h3>{c["footer_contact"]}</h3><ul><li><a href="tel:18009918881">(800) 991-8881</a></li><li><a href="tel:16262825388">(626) 282-5388</a></li></ul></div>
</div><div class="nb-footer-legal"><span>{c["copyright"]}</span>{legal}</div></div></footer>'''

def stickybar(c):
    return f'<div class="nb-stickybar" role="region" aria-label="{c["book"]}">{btn(c["book"],"primary","📅")}{btn(c["message"],"secondary","💬")}</div>'

def homepage(c, cur):
    return f'''<div class="nb-page" lang="{c['html_lang']}">
{header(c,cur)}
<main>{hero(c)}{problem(c)}{how(c)}
<section class="nb-section" id="doctor"><div class="nb-wrap">{doctor_card(c)}</div></section>
{visit(c)}{faq(c)}{locations(c)}
<section class="nb-section" style="padding-top:0;border-top:0"><div class="nb-wrap">{band(c)}</div></section></main>
{footer(c,cur)}{stickybar(c)}</div>'''

def form(c, state="default"):
    f=c["form"]; zh=c["lang"]=="zh"
    A=c["alhambra"]["name"]; W=c["walnut"]["name"]+(" （即將開放）" if zh else " (opening soon)")
    err = state=="error"
    foc = ' is-focus' if state in ("focus","error") else ''
    return f'''<form class="nb-form" onsubmit="return false">
<div class="nb-field"><label class="nb-label" for="p-{c['lang']}-{state}">{f["parent"]}</label><input class="nb-input{foc}" id="p-{c['lang']}-{state}" autocomplete="name" value="{'' if state=='default' else ('陳美玲' if zh else 'Mei-Ling Chen')}"></div>
<div class="nb-field{' is-error' if err else ''}"><label class="nb-label" for="t-{c['lang']}-{state}">{f["phone"]}</label><input class="nb-input" id="t-{c['lang']}-{state}" type="tel" autocomplete="tel" placeholder="(626) 000-0000" {'aria-invalid="true"' if err else ''}>
{('<p class="nb-error">'+E("❗")+f["err"]+'</p>') if err else '<p class="nb-hint">'+f["hint"]+'</p>'}</div>
<div class="nb-field"><label class="nb-label" for="a-{c['lang']}-{state}">{f["age"]}</label><select class="nb-input" id="a-{c['lang']}-{state}" style="max-width:200px"><option>{f["age_ph"]}</option>{''.join(f'<option>{i}</option>' for i in range(5,19))}</select></div>
<fieldset class="nb-field" style="border:0;padding:0;margin:0"><legend class="nb-label" style="margin-bottom:8px">{f["loc"]}</legend><div class="nb-radios">
<label class="nb-radio is-checked"><input type="radio" name="l-{c['lang']}-{state}" checked>{A}</label><label class="nb-radio is-disabled"><input type="radio" disabled name="l-{c['lang']}-{state}">{W}</label></div></fieldset>
<div>{'<button class="nb-btn nb-btn--primary" type="submit">'+E("📅")+'<span>'+f["submit"]+'</span></button>'}</div></form>'''

# ---------- component catalog ----------
def page(inner, pad=True):
    return f'<div class="nb-page"><div class="{"nb-spec" if pad else ""}">{inner}</div></div>'
def lab(t): return f'<p class="nb-spec-label">{t}</p>'
def lab_wrap(t): return f'<p class="nb-spec-label" style="padding:16px 24px 0">{t}</p>'
def zhwrap(inner): return f'<div lang="zh-Hant">{inner}</div>'

comps = {}  # name -> (group, height, width, subtitle, body, script, readme)

def add(name, group, height, body, readme, width=None, subtitle="", script="", page_card=False):
    comps[name]=(group,height,width,subtitle,body,script,readme,page_card)

# 1 Color
import tokens_gen as TG
tok=json.load(open("project/tokens.json"))
def swatches():
    names=["primary","secondary","accent","background","surface","text-primary","text-secondary","border","success","error"]
    labels=["Primary","Secondary","Accent","Background","Surface (cards)","Text Primary","Text Secondary","Border","Success","Error"]
    tk={t["name"]:t for t in tok["color"]["tokens"]}
    cards=""
    for n,l in zip(names,labels):
        v=tk[n]["value"]; use=tk[n]["usage"]
        import re as _r; use=_r.sub(r"^[A-Z][A-Z ()]+ · [A-Za-z]+\. ","",use); use=_r.sub(r"^[A-Z][A-Z ()]+\. ","",use); use=_r.sub(r"`([^`]+)`",r"<code>\1</code>",use)
        cards+=f'''<div style="border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden;background:var(--surface)">
<div style="height:64px;background:var(--{n});border-bottom:1px solid var(--border)"></div>
<div style="padding:12px"><p style="font-weight:800;font-size:15px">{l}</p><p class="nb-small" style="font-family:ui-monospace,monospace;font-weight:600">--{n}<br>Day {v["day"]} · Night {v["night"]}</p><p style="font-size:14px;line-height:1.45;margin-top:6px;color:var(--text-secondary)">{use}</p></div></div>'''
    return f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px">{cards}</div>'

from contrast import cr
def contrast_table():
    tk={t["name"]:t["value"] for t in tok["color"]["tokens"]}
    fgs=[("text-primary","Text Primary"),("text-secondary","Text Secondary"),("primary","Primary (as text)"),("success","Success"),("error","Error"),("on-primary","On-primary")]
    bgs=[("background","Background"),("surface","Surface"),("accent","Accent"),("secondary-hover","Wash"),("primary","Primary fill")]
    rows=""
    for th in ("day","night"):
        rows+=f'<tr><th colspan="{len(bgs)+1}" style="text-align:left;padding:14px 8px 6px;font-size:15px">{"☀️ Day" if th=="day" else "🌙 Night"}</th></tr>'
        for f,fl in fgs:
            cells=""
            for b,bl in bgs:
                if (f=="on-primary")!=(b=="primary"): cells+='<td style="color:var(--text-secondary);text-align:center">—</td>'; continue
                r=cr(tk[f][th],tk[b][th]); ok=r>=4.5
                cells+=f'<td style="text-align:center;padding:6px"><span style="display:inline-block;min-width:92px;padding:4px 8px;border-radius:6px;background:{tk[b][th]};color:{tk[f][th]};border:1px solid {tk["border"][th]};font-weight:800">Aa {r:.1f}</span><br><span style="font-size:12px;font-weight:800;color:var(--{"success" if ok else "error"})">{"✅ AA" if ok else "❗ fail — don’t use"}</span></td>'
            rows+=f'<tr><td style="padding:6px 8px;font-weight:700;font-size:14px">{fl}</td>{cells}</tr>'
    head="".join(f'<th style="font-size:13px;padding:6px">{bl}</th>' for b,bl in bgs)
    return f'<table style="border-collapse:collapse;width:100%"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table><p class="nb-small" style="margin-top:12px">Both themes are shown regardless of the page theme. Controls: <code>border-strong</code> is 3.6:1+ on every surface (3:1 needed). Focus ring = <code>secondary</code>, 11:1+.</p>'

add("Color","1 · Color",900,page(lab("Swatches · 10 roles")+swatches()+'<div style="height:32px"></div>'+lab("Contrast · which text passes on which ground")+contrast_table()),
    "# Color\n\nPaper, ink and one tomato. Ten roles plus state tokens, each defined for **Day** and **Night**. The swatch card shows the live theme; the contrast table shows both themes.\n\n- `primary` (tomato) is the only color with a job beyond ink — buttons, the current-language underline, step numbers in First visit.\n- `accent` is a highlighter behind a few words, never a fill for a button or a text color.\n- Never put `primary` text on `accent` (4.3:1 by day — fails).",
    page_card=True)

# 2 Typography
def type_scale():
    rows=""
    for s in ["display","h1","h2","h3","body","small","button"]:
        en=[x for x in tok["type"]["groups"][0]["styles"] if x["name"]==f"en-{s}"][0]
        enm=[x for x in tok["type"]["groups"][1]["styles"] if x["name"]==f"en-{s}-m"][0]
        zh=[x for x in tok["type"]["groups"][2]["styles"] if x["name"]==f"zh-{s}"][0]
        zhm=[x for x in tok["type"]["groups"][3]["styles"] if x["name"]==f"zh-{s}-m"][0]
        fe="var(--font-en-heading)" if s in ("display","h1","h2","h3","button") else "var(--font-en-body)"
        fz="var(--font-zh-heading)" if s in ("display","h1","h2","h3","button") else "var(--font-zh-body)"
        rows+=f'''<tr style="border-top:1px solid var(--border)"><td style="padding:16px 8px;vertical-align:top;width:120px"><p style="font-weight:800">{s.title() if s!="h1" and s!="h2" and s!="h3" else s.upper()}</p><p class="nb-small">EN {en["fontSize"]} / {enm["fontSize"]}<br>繁 {zh["fontSize"]} / {zhm["fontSize"]}<br>LH {en["lineHeight"]} · {zh["lineHeight"]}</p></td>
<td style="padding:16px 8px;vertical-align:top"><p style="font-family:{fe};font-size:{en["fontSize"]};line-height:{en["lineHeight"]};font-weight:{en["fontWeight"]}">{en["sample"]}</p><p class="nb-spec-label" style="margin:10px 0 2px">mobile {enm["fontSize"]}</p><p style="font-family:{fe};font-size:{enm["fontSize"]};line-height:{en["lineHeight"]};font-weight:{en["fontWeight"]}">{en["sample"]}</p></td>
<td style="padding:16px 8px;vertical-align:top" lang="zh-Hant"><p style="font-family:{fz};font-size:{zh["fontSize"]};line-height:{zh["lineHeight"]};letter-spacing:.02em">{zh["sample"]}</p><p class="nb-spec-label" lang="en" style="margin:10px 0 2px">mobile {zhm["fontSize"]}</p><p style="font-family:{fz};font-size:{zhm["fontSize"]};line-height:{zh["lineHeight"]};letter-spacing:.02em">{zh["sample"]}</p></td></tr>'''
    fams=f'''<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;margin-bottom:24px">
<div class="nb-note" style="padding:16px"><p class="nb-note-title">English heading</p><p style="font-family:var(--font-en-heading);font-weight:800;font-size:28px">Nunito 800</p><p class="nb-small">Google Fonts · OFL</p></div>
<div class="nb-note" style="padding:16px"><p class="nb-note-title">English body</p><p style="font-family:var(--font-en-body);font-size:22px">Nunito 400 / 600</p><p class="nb-small">Google Fonts · OFL</p></div>
<div class="nb-note" style="padding:16px" lang="zh-Hant"><p class="nb-note-title" lang="en">Chinese heading</p><p style="font-family:var(--font-zh-heading);font-size:28px">jf open 粉圓</p><p class="nb-small" lang="en">justfont · OFL · one weight</p></div>
<div class="nb-note" style="padding:16px" lang="zh-Hant"><p class="nb-note-title" lang="en">Chinese body</p><p style="font-family:var(--font-zh-body);font-size:22px">jf open 粉圓 400</p><p class="nb-small" lang="en">≥17px · line height 1.8</p></div></div>'''
    return fams+f'<table style="border-collapse:collapse;width:100%;table-layout:fixed"><colgroup><col style="width:150px"><col><col></colgroup><thead><tr><th style="text-align:left;padding:8px" class="nb-spec-label">Level · desktop / mobile</th><th style="text-align:left;padding:8px" class="nb-spec-label">English (desktop size)</th><th style="text-align:left;padding:8px" class="nb-spec-label">繁體中文 (desktop size)</th></tr></thead><tbody>{rows}</tbody></table>'
add("Typography","2 · Typography",1700,page(type_scale()),
    "# Typography\n\nNunito for English, jf open 粉圓 for Chinese — both rounded, both friendly. Seven levels, each with a desktop and a mobile size, English and Traditional Chinese side by side. Chinese never drops below 17px for body and never below 1.7 line height (the system uses 1.8).",
    page_card=True)

# 3 Spacing & layout
def spacing():
    sp=tok["spacing"]["tokens"]
    bars="".join(f'<div style="display:grid;grid-template-columns:110px 60px 1fr;align-items:center;gap:12px;padding:6px 0"><code style="font-size:14px">{t["name"]}</code><span class="nb-small">{t["value"]}</span><div><div style="height:16px;width:{t["value"]};background:var(--primary);border-radius:3px"></div></div></div>' for t in sp)
    cols=lambda n,g: f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:{g}px;height:80px">'+''.join('<div style="background:var(--accent);border-radius:4px"></div>' for _ in range(n))+'</div>'
    return f'''{lab("Spacing scale · 8px base")}{bars}
<div style="height:24px"></div>{lab("Page · max width 1120px content, 680px reading column")}
<div style="border:1px dashed var(--border-strong);border-radius:8px;padding:12px"><div style="max-width:680px;margin:0 auto;border:1px solid var(--border);background:var(--surface);border-radius:8px;padding:10px;text-align:center" class="nb-small">reading-max 680px — paragraphs, FAQ</div><p class="nb-small" style="text-align:center;margin-top:6px">page-max 1120px · 24px side padding (desktop) · 20px (mobile)</p></div>
<div style="height:24px"></div>{lab("Desktop grid · 12 columns · 24px gutter (≥1024px)")}{cols(12,24)}
<div style="height:16px"></div>{lab("Tablet grid · 8 columns · 24px gutter (768–1023px)")}{cols(8,24)}
<div style="height:16px"></div>{lab("Mobile grid · 4 columns · 16px gutter · 20px margins (<768px)")}<div style="max-width:390px;padding:0 20px;border:1px dashed var(--border-strong);border-radius:8px">{cols(4,16)}</div>
<div style="height:16px"></div><p class="nb-small">Section rhythm: 96px top/bottom on desktop (<code>space-12</code>), 64px on mobile (<code>space-8</code>), a 1px <code>border</code> rule between sections.</p>'''
add("Spacing & Layout","3 · Spacing & Layout",760,page(spacing()),
    "# Spacing & Layout\n\nEverything steps on 8px. Sections breathe (96px desktop, 64px mobile) and are separated by a single hairline — like pages in a notebook. Paragraphs never run wider than 680px.",
    page_card=True)

# 4 Shape
def shape():
    r="".join(f'<div style="text-align:center"><div style="width:120px;height:80px;border:1.5px solid var(--secondary);border-radius:var(--{n});background:var(--surface)"></div><p class="nb-small" style="margin-top:6px"><code>{n}</code> {v}</p></div>' for n,v in [("radius-sm","6px"),("radius-md","12px"),("radius-lg","20px"),("radius-pill","999px")])
    return f'''{lab("Corner radius")}<div style="display:flex;gap:24px;flex-wrap:wrap">{r}</div>
<div style="height:24px"></div>{lab("Borders")}<div style="display:flex;gap:24px;flex-wrap:wrap">
<div style="width:220px;padding:16px;border:1px solid var(--border);border-radius:12px;background:var(--surface)"><b>Hairline</b><p class="nb-small">1px <code>border</code> — cards, dividers</p></div>
<div style="width:220px;padding:16px;border:1.5px solid var(--border-strong);border-radius:12px;background:var(--surface)"><b>Control</b><p class="nb-small">1.5px <code>border-strong</code> — inputs, chips</p></div>
<div style="width:220px;padding:16px;border:1px dashed var(--border-strong);border-radius:12px"><b>Placeholder</b><p class="nb-small">1px dashed — "coming soon", draft copy</p></div></div>
<div style="height:24px"></div>{lab("Shadow · almost none")}<div style="display:flex;gap:24px;flex-wrap:wrap">
<div style="width:220px;padding:16px;border:1px solid var(--border);border-radius:20px;background:var(--surface)"><b>shadow-none</b><p class="nb-small">Every card. Paper is flat.</p></div>
<div style="width:220px;padding:16px;border:1px solid var(--border);border-radius:20px;background:var(--surface);box-shadow:var(--shadow-sheet)"><b>shadow-sheet</b><p class="nb-small">Only the mobile menu and sticky bar — things that float.</p></div></div>'''
add("Shape","4 · Shape",560,page(shape()),"# Shape\n\nMedium, friendly corners; thin lines; no depth. Edges come from 1px borders, not shadows.",page_card=True)

# 5 Components
def states(items): return '<div class="nb-state-grid">'+''.join(f'<div class="nb-state">{lab(l)}{h}</div>' for l,h in items)+'</div>'
add("Primary button","5 · Components",260,page(states([("Default",btn(EN["book"],"primary","📅")),("Hover",btn(EN["book"],"primary","📅","is-hover")),("Pressed",btn(EN["book"],"primary","📅","is-pressed")),("Focus (keyboard)",btn(EN["book"],"primary","📅","nb-focus-demo")),("繁體 · default",zhwrap(btn(ZH["book"],"primary","📅"))),("Small (header)",btn(EN["book"],"primary",None,"nb-btn--sm"))])),
    "# Primary button\n\nThe one tomato button — use it for booking and nothing else. Label is a verb phrase; `📅` leads. Height 52px (44px small). Fill `primary` → `primary-hover` → `primary-pressed`; label `on-primary`. At most one per screen region; on mobile it goes full width.",subtitle="Default · hover · pressed")
add("Secondary button","5 · Components",260,page(states([("Default",btn(EN["message"],"secondary","💬")),("Hover",btn(EN["message"],"secondary","💬","is-hover")),("Pressed",btn(EN["message"],"secondary","💬","is-pressed")),("Focus (keyboard)",btn(EN["message"],"secondary","💬","nb-focus-demo")),("繁體 · default",zhwrap(btn(ZH["message"],"secondary","💬"))),("Disabled / coming soon",f'<span class="nb-btn nb-btn--secondary is-disabled">{EN["soon_btn"]}</span>')])),
    "# Secondary button\n\nInk outline, transparent fill. Used for messaging, directions and every non-booking action. Hover and pressed add the `secondary-hover` / `secondary-pressed` wash. Disabled uses a dashed hairline and `text-secondary` — used for the Walnut clinic until it opens.",subtitle="Default · hover · pressed")
add("Language switcher","5 · Components",200,page(states([("Default (EN current)",lang_switch("en")),("Hover on 繁體",lang_switch("en").replace('lang="zh-Hant" class=""','lang="zh-Hant" class="is-hover"')),("Pressed on 简体",lang_switch("en").replace('lang="zh-Hans" class=""','lang="zh-Hans" class="is-pressed"')),("繁體 current",lang_switch("zh-Hant"))])),
    "# Language switcher\n\nEN / 简体 / 繁體 as three plain text links, always visible at the top of every page (in the header on desktop, in the utility bar above the header on mobile), and repeated in the footer. Each link goes to that language's own page (`hreflang`), never a translate widget. Current language: `text-primary` with a 3px `primary` underline and `aria-current=\"page\"`. Tap targets are 44×44px minimum.",subtitle="Default · hover · pressed")
add("Top navigation + mobile menu","5 · Components",620,f'''<div class="nb-page">{lab_wrap("Desktop (≥1024px)")}{header(EN,"en")}
<div style="padding:24px"><p class="nb-spec-label">Nav link states</p><nav class="nb-nav" style="margin:0;display:flex"><a href="#">Default</a><a href="#" class="is-hover">Hover</a><a href="#" class="is-pressed">Pressed</a></nav>
<div style="height:24px"></div><p class="nb-spec-label">Mobile (&lt;1024px) · menu open</p>
<div style="max-width:390px;border:1px solid var(--border);border-radius:16px;overflow:hidden;background:var(--background)"><div class="nb-utility" style="display:flex"><div class="nb-utility-in" style="justify-content:space-between;padding:0 12px">{lang_switch("en")}{toggle(EN,True)}</div></div>
<div class="nb-header"><div class="nb-header-in" style="display:flex;min-height:64px;padding:0 20px"><span class="nb-brand" style="font-size:19px">{EN["brand"]}</span><button class="nb-btn nb-btn--secondary nb-btn--sm is-pressed" style="margin-left:auto" aria-expanded="true">✕ {EN["close"]}</button></div></div>
<div style="padding:12px">{sheet(EN)}</div></div></div></div>''',
    "# Top navigation + mobile menu\n\nDesktop: plain-text name left (Nunito 800 — no logo), five section links, then language switcher, night toggle and a small primary **Book a consultation**. Below 1024px the links collapse into **☰ Menu**; the language switcher and night toggle move to a slim utility bar above the header so they stay visible. The menu opens as a flat sheet (`surface`, `radius-lg`, `shadow-sheet`) with the links as big 56px rows and Book + Message at the bottom.",subtitle="Desktop · mobile menu", script=THEME_JS)
add("Hero block","5 · Components",620,f'<div class="nb-page">{hero(EN)}</div>',"# Hero block\n\nText first: eyebrow with 👀, the headline in `display` with its second sentence on the `accent` marker, the subhead in `lead`, then Book (primary) + Message (secondary). The trust note on the right lists Dr. Woo, 30 years, languages and the two clinics — the first thing a parent checks. On mobile the note drops below the buttons, still inside the first screen's scroll.",subtitle="EN · desktop", width=1200)
add("3-step How it works block","5 · Components",420,page(lab("Default")+steps_block(EN)+'<div style="height:24px"></div>'+lab("繁體 · step 2 highlighted (accent)")+zhwrap(steps_block(ZH,current=2))),
    "# 3-step How it works block\n\nThree tidy note cards, numbered in words (Step 1, 步驟 1), with one emoji marker each: 👀 exam and eye map, 📏 custom lenses, 🌙 wear at night. Step titles are `h3`. On mobile they stack as rows with the emoji on the left. The `accent` tint may mark one step when a page refers to it.")
add("Doctor card","5 · Components",620,f'<div class="nb-page"><div class="nb-wrap" style="padding:32px 24px">{doctor_card(EN)}</div></div>',"# Doctor card\n\nThe only photo on the page: Dr. Woo with a child patient, 4:5, `radius-lg`. Name as `h1`, the two provided lines as `lead`, languages as chips, and a Book button. Never add credentials, awards or numbers that the client hasn't provided.",width=1200)
add("FAQ accordion","5 · Components",620,page(lab("Open · closed · hover (row 3)")+faq_block(EN,0,2)+'<div style="height:24px"></div>'+lab("繁體")+zhwrap(faq_block(ZH,1))),
    "# FAQ accordion\n\nNative `<details>` rows on `surface` with a ❓ marker, question in heading font, + / – on the right. Hover `secondary-hover`, pressed `secondary-pressed`. Answers use `body` and never exceed the 680px reading width. Several may be open at once.",subtitle="Open · closed · hover")
add("Booking call-to-action band","5 · Components",300,f'<div class="nb-page"><div style="padding:24px">{band(EN)}<div style="height:16px"></div><div lang="zh-Hant">{band(ZH)}</div></div></div>',"# Booking call-to-action band\n\nThe bottom-of-page repeat of the hero's actions: a flat note card with an `h2`, one supporting line in `text-secondary`, and Book + Message. One per page, right before the footer.",width=1100)
add("Location card","5 · Components",560,f'<div class="nb-page"><div style="padding:24px"><div class="nb-locs">{loc_card(EN,"alhambra")}{loc_card(EN,"walnut")}</div></div></div>',"# Location card\n\nMap placeholder on top, then clinic name with its other-language name beside it, 📍 address, 📅 hours, 📞 phones, and Book here + Directions. A clinic without an address shows \"coming soon\" in `text-secondary` italic and a dashed, disabled \"Opening soon\" button — never a fake map pin. Side by side on desktop, stacked on mobile.",width=1100)
add("Contact row","5 · Components",260,page(states([("Default",contact_row(EN))])+'<div style="height:16px"></div>'+lab("Hover (Book online) · pressed (WeChat)")+contact_row(EN,1,2)+'<div style="height:16px"></div>'+lab("繁體")+zhwrap(contact_row(ZH))),
    "# Contact row\n\nFive equal chips: 📞 Call, 📅 Book online, WeChat, LINE, WhatsApp. The three app marks are **dashed placeholders** (WC / LINE / WA) — swap in each company's official icon from their brand kit; never redraw them. On mobile the row becomes a 2-column grid with Call full width.",subtitle="Default · hover · pressed")
add("Form field set","5 · Components",900,f'<div class="nb-page"><div class="nb-spec" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:40px"><div>{lab("Default · EN")}{form(EN)}</div><div>{lab("Focus + error · EN")}{form(EN,"error")}</div><div lang="zh-Hant">{lab("繁體")}{form(ZH,"filled")}</div></div></div>',
    "# Form field set\n\nFour fields — parent name, phone, child's age, preferred location — labels always above, never placeholder-only. 52px fields, 1.5px `border-strong`, `radius-md`. Hover darkens the edge to `secondary`; focus adds the 3px ink ring. Errors: 2px `error` edge plus a ❗ sentence in `error` — never color alone. Walnut stays disabled until it opens.",width=1100)
add("Footer","5 · Components",360,f'<div class="nb-page">{footer(EN,"en")}</div>',"# Footer\n\n`surface-muted` ground. Name (plain text) and Chinese name, language switcher, both clinics with address and hours, both phone numbers, then a hairline and the small legal links (privacy policy, notice of privacy practices, accessibility, terms).",width=1200)
add("Light-night toggle","5 · Components · Concept A extra",200,page(states([("Default (day)",toggle(EN)),("Hover",toggle(EN,state="is-hover")),("Pressed",toggle(EN,state="is-pressed")),("Icon-only (header)",toggle(EN,True)),("繁體",zhwrap(toggle(ZH)))])),
    "# Light-night toggle\n\nA pill with 🌙 / ☀️ that flips `data-theme` between `day` and `night` on `<html>`. Try it — this preview is live. Default follows the device (`prefers-color-scheme`); a manual choice is remembered per browser. Icon-only in the header, labelled in menus.",subtitle="Default · hover · pressed · live",script=THEME_JS)

# 6 Icons
icons=[("👀","eye","Exams, the eye map, the hero eyebrow"),("🌙","moon","Wear at night; night mode"),("☀️","sun","See clearly all day; day mode"),("📅","calendar","Booking, hours"),("📞","phone","Call"),("❓","question","Parent questions")]
ic="".join(f'<div class="nb-note" style="padding:16px;text-align:center"><div class="nb-emoji" style="font-size:44px">{e}</div><p style="font-weight:800;margin-top:8px">{n}</p><p class="nb-small">{u}</p></div>' for e,n,u in icons)
ext="".join(f'<span class="nb-chip">{E(e)}{n}</span>' for e,n in [("💬","message"),("📍","address / map"),("📏","custom fit"),("📷","photo placeholder"),("✅","done"),("❗","error")])
add("Icons","6 · Icons",520,page(lab("The six core icons — emoji, not drawn")+f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px">{ic}</div><div style="height:20px"></div>'+lab("Allowed extras (and no others)")+f'<div class="nb-chips">{ext}</div>'),
    "# Icons\n\nEmoji, set in the system emoji font. Rules: one emoji per item, always next to words (never alone as a button label except the icon-only night toggle, which has an `aria-label`); always `aria-hidden`; sizes 18 / 22 / 36 / 44px only; no emoji in headlines. Twelve are allowed — the six core plus six extras shown here. Messaging-app logos are not emoji: use the official marks.",page_card=True)

# 7 Imagery
add("Imagery","7 · Imagery",520,page(f'''<div style="display:grid;grid-template-columns:minmax(220px,300px) 1fr;gap:32px;align-items:start">
<figure class="nb-photo">{E("📷")}Photo: Dr. Woo with a child patient</figure>
<div class="nb-stack-lg"><div><p class="nb-spec-label">Rule</p><p class="nb-body">One real photo on the homepage: Dr. Woo with a child patient. Everything else is words. No illustrations, no stock, no icons-as-pictures.</p></div>
<div class="nb-grid" style="grid-template-columns:1fr 1fr;gap:24px"><div><p class="nb-spec-label">✅ Do</p><ul class="nb-checks"><li>{E("✅")}<span>Natural window light, warm and a little soft</span></li><li>{E("✅")}<span>Dr. Woo at the child's eye level, both relaxed</span></li><li>{E("✅")}<span>Crop 4:5, <code>radius-lg</code>, no filter</span></li><li>{E("✅")}<span>Get written consent from the parent</span></li></ul></div>
<div><p class="nb-spec-label">❗ Don't</p><ul class="nb-checks"><li>{E("❗")}<span>Stock photos or AI-generated people</span></li><li>{E("❗")}<span>Close-ups of lenses on fingertips or eyes being touched</span></li><li>{E("❗")}<span>Illustrations, cartoons, gradients, overlays</span></li><li>{E("❗")}<span>Text baked into the photo</span></li></ul></div></div></div></div>'''),
    "# Imagery\n\nMinimal on purpose. The notebook is words; the one photo is the proof that a real, kind doctor is behind them.",page_card=True)

# 8 Voice
add("Voice & Tone","8 · Voice & Tone",560,page(f'''<div class="nb-chips" style="margin-bottom:24px"><span class="nb-chip" style="font-size:20px;min-height:48px">Kind</span><span class="nb-chip" style="font-size:20px;min-height:48px">Plain</span><span class="nb-chip" style="font-size:20px;min-height:48px">Conversational</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
<div class="nb-note"><p class="nb-note-title">✅ Done right</p><p class="nb-h3" style="margin-top:8px">Not sure if ortho-k is right for your child? Let's talk it through.</p><p class="nb-h3" lang="zh-Hant" style="margin-top:12px">不確定角膜塑型適不適合孩子？我們一起慢慢聊。</p><p class="nb-small" style="margin-top:12px">Short. Talks to the parent. Invites a question.</p></div>
<div class="nb-note" style="border-style:dashed"><p class="nb-note-title">❗ Done wrong</p><p class="nb-body" style="margin-top:8px">Orthokeratology utilizes reverse-geometry rigid gas-permeable lenses to induce controlled corneal reshaping.</p><p class="nb-body" lang="zh-Hant" style="margin-top:12px">本中心採用逆幾何高透氧硬式鏡片，誘導角膜可控性重塑。</p><p class="nb-small" style="margin-top:12px">Jargon. Talks about the clinic, not the child.</p></div></div>'''),
    "# Voice & Tone\n\nKind, plain, conversational — like a friend who happens to be an eye doctor, explaining over tea.",page_card=True)

# Homepages
add("Homepage desktop EN","9 · Homepage",4000,homepage(EN,"en"),"# Homepage desktop EN\n\nThe full homepage at 1280px, built only from the components above. Try the night toggle.",width=1280,script=THEME_JS+MENU_JS)
add("Homepage mobile EN","9 · Homepage",4000,homepage(EN,"en"),"# Homepage mobile EN\n\nThe same page at 390px (iPhone 15). Language switcher and night toggle in the top utility bar, ☰ Menu opens the sheet, and a sticky Book / Message bar follows the scroll.",width=390,script=THEME_JS+MENU_JS)
add("Homepage Traditional Chinese desktop","9 · Homepage",4000,homepage(ZH,"zh-Hant"),"# Homepage Traditional Chinese desktop\n\n繁體中文首頁，1280px。",width=1280,script=THEME_JS+MENU_JS)
add("Homepage Traditional Chinese mobile","9 · Homepage",4000,homepage(ZH,"zh-Hant"),"# Homepage Traditional Chinese mobile\n\n繁體中文首頁，390px。",width=390,script=THEME_JS+MENU_JS)

ORDER=list(comps.keys())
def write_all(local=False):
    base = "local" if local else OUT
    for name,(group,height,width,subtitle,body,script,readme,pc) in comps.items():
        d=os.path.join(base,name); os.makedirs(d,exist_ok=True)
        attrs=f'group="{group}" height={height}'+(f' width={width}' if width else '')+(f' subtitle="{subtitle}"' if subtitle else '')+(' page' if pc else '')
        lang="zh-Hant" if "Chinese" in name else "en"
        h=doc(name, body, f"<!-- @dsCard {attrs} -->", lang, script)
        if local:
            h=h.replace("</head>",'<link rel="stylesheet" href="../../tokens.local.css"><link rel="stylesheet" href="../../project/components/bundle.css"></head>').replace("html lang",'html data-theme="day" lang')
        open(os.path.join(d,"preview.html"),"w").write(h)
        if not local: open(os.path.join(d,"README.md"),"w").write(readme+"\n")
    if not local:
        hdr={"format":4,"namespace":"NotebookA","components":[{"name":n} for n in ORDER]}
        open(os.path.join(OUT,"bundle.js"),"w").write("/* @ds-bundle: "+json.dumps(hdr,ensure_ascii=False)+" */\nwindow.NotebookA = { concept: 'A', name: 'Friendly Notebook' };\n")
    return ORDER

if __name__=="__main__":
    write_all(False); write_all(True)
    # collect CJK chars for font subsetting
    txt=""
    for root,_,fs in os.walk("project"):
        for f in fs:
            if f.endswith((".html",".md",".json",".css")): txt+=open(os.path.join(root,f),encoding="utf-8").read()
    open("chars.txt","w").write("".join(sorted(set(ch for ch in txt if ord(ch)>0x2E7F))))
    print(len(comps), "cards")
