"""Shared structure for concepts B–D. Same components, same homepage markup, same order.
Each concept module supplies a skin: icons, art hooks, CSS, tokens, README."""
import os, json, copy, re
from content import EN as _EN, ZH as _ZH

EMAP = {"👀":"eye","🌙":"moon","💬":"message","📍":"pin","📏":"lens","📅":"calendar","📞":"phone","❓":"question","📷":"camera","✅":"check","❗":"alert","☀️":"sun"}
def _conv(c):
    c = copy.deepcopy(c)
    c["trust"] = [(EMAP[e], t) for e, t in c["trust"]]
    c["steps"] = [(EMAP[e], t) for e, t in c["steps"]]
    c["contact"] = [((EMAP.get(i, i)), l, s) for i, l, s in c["contact"]]
    c["hero_h"] = c["hero_h"].replace('nb-mark', 'ui-mark')
    c["phones"] = c["phones"].replace('nb-nowrap', 'ui-nowrap')
    return c
EN, ZH = _conv(_EN), _conv(_ZH)
EN["hero_plain"] = ("Clear vision all day.", "No glasses at school.")
ZH["hero_plain"] = ("白天看得清楚，", "上學不用戴眼鏡。")
EN["specialty"] = "Children's ortho-k, ages 7–18"; ZH["specialty"] = "兒童角膜塑型・7–18歲"

# ---------------- icon geometry (24×24) ----------------
PATHS = {
 "eye": '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "moon": '<path d="M20 14.6A8.2 8.2 0 1 1 9.4 4a6.6 6.6 0 0 0 10.6 10.6z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 "phone": '<path d="M5.2 3.5h3.4l1.8 4.6-2.3 1.5a11.5 11.5 0 0 0 6.3 6.3l1.5-2.3 4.6 1.8v3.4a1.8 1.8 0 0 1-1.9 1.8A16.4 16.4 0 0 1 3.4 5.4a1.8 1.8 0 0 1 1.8-1.9z"/>',
 "question": '<circle cx="12" cy="12" r="9.5"/><path d="M9.3 9.4a2.8 2.8 0 1 1 3.8 2.6c-.7.3-1.1.9-1.1 1.6v.5"/><path d="M12 17.2v.1"/>',
 "message": '<path d="M4.5 4.5h15a1.5 1.5 0 0 1 1.5 1.5v10a1.5 1.5 0 0 1-1.5 1.5H10l-5 3.5v-3.5h-.5A1.5 1.5 0 0 1 3 16V6a1.5 1.5 0 0 1 1.5-1.5z"/>',
 "pin": '<path d="M12 21s-7-6.1-7-11.4a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.6" r="2.5"/>',
 "lens": '<path d="M3.5 13.5c0-4.7 3.8-8.5 8.5-8.5s8.5 3.8 8.5 8.5c-2.5 1.6-5.4 2.5-8.5 2.5s-6-.9-8.5-2.5z"/><path d="M7.5 11.5c.8-1.7 2.5-2.8 4.5-2.8"/>',
 "camera": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7l1.5-3h5L16 7"/><circle cx="12" cy="13.5" r="3.5"/>',
 "check": '<path d="M4 12.5l5 5L20 6"/>',
 "alert": '<circle cx="12" cy="12" r="9.5"/><path d="M12 7v6.5M12 16.8v.1"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "close": '<path d="M6 6l12 12M18 6L6 18"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
 "chat": '<path d="M4.5 4.5h15a1.5 1.5 0 0 1 1.5 1.5v10a1.5 1.5 0 0 1-1.5 1.5H10l-5 3.5v-3.5h-.5A1.5 1.5 0 0 1 3 16V6a1.5 1.5 0 0 1 1.5-1.5z"/>',
}
def svg_icon(name, stroke=2, extra="", cls="ui-ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{extra}{PATHS[name]}</svg>')

# ---------------- document ----------------
def doc(K, title, body, marker, lang="en", script=""):
    return f"""{marker}
<!doctype html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{K.FONT_URL}" rel="stylesheet">
<style>html,body{{margin:0;background:var(--background)}}</style>
</head>
<body>
{body}
{('<script>'+script+'</script>') if script else ''}
</body>
</html>
"""
MENU_JS = """document.querySelectorAll('[data-ui-menu]').forEach(function(b){b.addEventListener('click',function(){var s=document.getElementById(b.getAttribute('aria-controls'));var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',!o);s.hidden=o;});});"""

class Builder:
    def __init__(self, K):
        self.K = K; self.I = K.icon; self.comps = {}

    # ---------- atoms ----------
    def lang_switch(self, cur="en", states=None):
        states = states or {}
        items=[("en","EN"),("zh-Hans","简体"),("zh-Hant","繁體")]
        out=[]
        for k,t in items:
            ac=' aria-current="page"' if k==cur else ''
            st=states.get(k,"")
            out.append(f'<a href="#" hreflang="{k}" lang="{k}"{ac} class="{st}">{t}</a>')
        return '<nav class="ui-lang" aria-label="Language / 語言">'+'<span class="ui-lang-sep" aria-hidden="true">/</span>'.join(out)+'</nav>'

    def btn(self, label, kind="primary", icon=None, extra="", href="#"):
        ic = self.I(icon) if icon else ""
        return f'<a href="{href}" class="ui-btn ui-btn--{kind} {extra}">{ic}<span>{label}</span></a>'

    def h(self, level, text, c=None, cls="", plain=None):
        """Heading. Concept may render Chinese display text specially (B: grid boxes)."""
        tag = {"display":"h1","h1":"h2","h2":"h2","h3":"h3"}[level]
        if c and c["lang"]=="zh" and hasattr(self.K, "zh_heading") and level in getattr(self.K,"ZH_BOX_LEVELS",()):
            return self.K.zh_heading(tag, level, text, cls)
        return f'<{tag} class="ui-{level} {cls}">{text}</{tag}>'

    # ---------- components ----------
    def header(self, c, cur):
        links="".join(f'<a href="{h}">{t}</a>' for h,t in c["nav"])
        brand=f'<a class="ui-brand" href="#">{c["brand"]}'+(f'<small lang="zh-Hant">{c["brand_zh"]}</small>' if c["brand_zh"] else '')+'</a>'
        return f'''<div class="ui-utility"><div class="ui-wrap ui-utility-in">{self.K.utility_extra(self, c) if hasattr(self.K,"utility_extra") else ""}{self.lang_switch(cur)}</div></div>
<header class="ui-header"><div class="ui-wrap ui-header-in">{brand}
<nav class="ui-nav" aria-label="Main">{links}</nav>
<div class="ui-header-tools">{self.btn(c["book"],"primary",None,"ui-btn--sm")}
<button type="button" class="ui-btn ui-btn--secondary ui-btn--sm ui-menu-btn" data-ui-menu aria-expanded="false" aria-controls="ui-menu-{c['lang']}">{self.I("menu")}<span>{c["menu"]}</span></button></div></div>
<div class="ui-wrap" id="ui-menu-{c['lang']}" hidden style="padding-bottom:16px">{self.sheet(c)}</div></header>'''

    def sheet(self, c):
        links="".join(f'<li><a href="{h}">{t}{self.I("arrow")}</a></li>' for h,t in c["nav"])
        return f'''<div class="ui-sheet"><ul class="ui-sheet-links">{links}</ul>
<div class="ui-sheet-foot ui-stack">{self.btn(c["book"],"primary","calendar","ui-btn--block")}{self.btn(c["message"],"secondary","message","ui-btn--block")}</div></div>'''

    def trust_list(self, c):
        return '<ul class="ui-trust">'+"".join(f'<li>{self.I(i)}<span>{t}</span></li>' for i,t in c["trust"])+'</ul>'

    def hero(self, c):
        K=self.K
        return f'''<section class="ui-hero {K.SECTION.get("hero","")}">{K.hero_bg(c) if hasattr(K,"hero_bg") else ""}<div class="ui-wrap ui-hero-grid">
<div class="ui-hero-text"><p class="ui-eyebrow">{self.I("eye")}<span>{c["eyebrow"]}</span></p>
{self.h("display", c["hero_h"], c, plain=c["hero_plain"])}
<p class="ui-lead">{c["hero_sub"]}</p>
<div class="ui-btn-row">{self.btn(c["book"],"primary","calendar")}{self.btn(c["message"],"secondary","message")}</div>
{K.hero_trust(self, c)}</div>
<div class="ui-hero-art">{K.hero_aside(self, c)}</div>
</div>{K.hero_after(self, c)}</section>'''

    def problem(self, c):
        return f'''<section class="ui-section {self.K.SECTION.get("problem","")}"><div class="ui-wrap ui-grid">
<div class="ui-span-6">{self.h("h1", c["prob_h"], c)}</div>
<p class="ui-lead ui-at-8">{c["prob_b"]}</p></div></section>'''

    def steps_block(self, c, current=None):
        items=""
        for i,(ic,t) in enumerate(c["steps"],1):
            cur=' is-current' if current==i else ''
            items+=f'<li class="ui-step{cur}">{self.K.step_marker(self, c, i, ic)}<h3 class="ui-h3">{t}</h3></li>'
        return f'<ol class="ui-steps">{items}</ol>'

    def how(self, c):
        return f'''<section class="ui-section {self.K.SECTION.get("how","")}" id="how"><div class="ui-wrap">
<div class="ui-how-head">{self.h("h2", c["how_h"], c)}{self.K.how_art(self, c)}</div>{self.steps_block(c)}</div></section>'''

    def doctor_card(self, c):
        chips="".join(f'<li class="ui-chip">{self.I("message")}{l}</li>' for l in c["langs"])
        lines="".join(f'<p class="ui-lead">{l}</p>' for l in c["doc_lines"])
        return f'''<div class="ui-doctor">{self.K.doctor_photo(self, c)}
<div class="ui-doctor-text ui-stack-lg"><p class="ui-eyebrow">{self.I("eye")}<span>{c["doc_eyebrow"]}</span></p>{self.h("h1", c["doc_name"], c)}{lines}<ul class="ui-chips" aria-label="Languages">{chips}</ul>
<div class="ui-btn-row">{self.btn(c["book"],"primary","calendar")}</div></div></div>'''

    def visit(self, c):
        lis="".join(f'<li><span class="ui-n">{i}</span><p class="ui-body">{t}</p></li>' for i,t in enumerate(c["visit"],1))
        return f'''<section class="ui-section {self.K.SECTION.get("visit","")}" id="visit"><div class="ui-wrap ui-grid">
<div class="ui-span-5">{self.h("h2", c["visit_h"], c)}<p style="margin-top:var(--space-2)"><span class="ui-draft">{c["draft"]}</span></p></div>
<ol class="ui-lines ui-at-7">{lis}</ol></div></section>'''

    def faq_block(self, c, open_idx=0, hover_idx=None, pressed_idx=None):
        out=""
        for i,q in enumerate(c["faqs"]):
            o=' open' if i==open_idx else ''
            st=' class="is-hover"' if i==hover_idx else (' class="is-pressed"' if i==pressed_idx else '')
            out+=f'<li><details{o}><summary{st}>{self.I("question")}<span>{q}</span><span class="ui-plus" aria-hidden="true"></span></summary><div class="ui-answer"><p class="ui-body">{c["faq_a"]}</p></div></details></li>'
        return f'<ul class="ui-faq">{out}</ul>'

    def faq(self, c):
        return f'''<section class="ui-section {self.K.SECTION.get("faq","")}" id="faq"><div class="ui-wrap"><div class="ui-faq-wrap">{self.h("h2", c["faq_h"], c)}{self.faq_block(c)}</div></div></section>'''

    def contact_row(self, c, hover=None, pressed=None):
        out=""
        for i,(ic,label,sub) in enumerate(c["contact"]):
            st=' is-hover' if i==hover else (' is-pressed' if i==pressed else '')
            ico = f'<span class="ui-cico">{self.I(ic)}</span>' if ic in PATHS else f'<span class="ui-cico ui-cico--ph" title="Official app icon goes here">{ic}</span>'
            s=f'<small>{sub}</small>' if sub else ''
            out+=f'<li><a href="#" class="{st.strip()}">{ico}<span>{label}{s}</span></a></li>'
        return f'<ul class="ui-contact" aria-label="Contact">{out}</ul>'

    def loc_card(self, c, key):
        L=c[key]; soon = key=="walnut"
        sc=' ui-soon' if soon else ''
        btns = (self.btn(c["book_here"],"primary","calendar","ui-btn--sm")+self.btn(c["directions"],"secondary","map","ui-btn--sm")) if not soon else f'<span class="ui-btn ui-btn--secondary ui-btn--sm is-disabled" aria-disabled="true">{c["soon_btn"]}</span>'
        other = 'en' if c['lang']=='zh' else 'zh-Hant'
        return f'''<article class="ui-loc">{self.K.loc_media(self, c, key, soon)}
<div class="ui-loc-body"><div class="ui-loc-name"><h3 class="ui-h3">{L["name"]}</h3><span class="ui-loc-alt" lang="{other}">{L["zh"]}</span></div>
<div class="ui-kv">{self.I("pin")}<p class="ui-body{sc}">{L["addr"]}</p></div>
<div class="ui-kv">{self.I("clock")}<p class="ui-body{sc}">{L["hours"]}</p></div>
<div class="ui-kv">{self.I("phone")}<p class="ui-body">{c["phones"]}</p></div>
<div class="ui-btn-row">{btns}</div></div></article>'''

    def locations(self, c):
        return f'''<section class="ui-section {self.K.SECTION.get("locations","")}" id="locations"><div class="ui-wrap ui-stack-lg">
{self.h("h1", c["loc_h"], c)}
<p class="ui-label-sm">{c["contact_title"]}</p>{self.contact_row(c)}
<div class="ui-locs">{self.loc_card(c,"alhambra")}{self.loc_card(c,"walnut")}</div></div></section>'''

    def band(self, c):
        return f'''<div class="ui-band">{self.K.band_art(self, c)}<div class="ui-band-text">{self.h("h2", c["band_h"], c)}<p class="ui-body ui-muted">{c["band_b"]}</p></div>
<div class="ui-btn-row">{self.btn(c["book"],"primary","calendar")}{self.btn(c["message"],"secondary","message")}</div></div>'''

    def footer(self, c, cur):
        A,W=c["alhambra"],c["walnut"]
        legal="".join(f'<a href="#">{l}</a>' for l in c["legal"])
        return f'''<footer class="ui-footer"><div class="ui-wrap"><div class="ui-footer-grid">
<div><p class="ui-brand ui-brand--footer">{c["brand"]}</p><p lang="zh-Hant" class="ui-footer-zh">1234兒童視力矯正中心</p><div style="margin-top:var(--space-2)"><h3>{c["footer_langs"]}</h3>{self.lang_switch(cur)}</div></div>
<div><h3>{A["name"]}</h3><p>{A["addr"]}<br>{A["hours"]}</p></div>
<div><h3>{W["name"]}</h3><p>{W["addr"]}<br>{W["hours"]}</p></div>
<div><h3>{c["footer_contact"]}</h3><ul><li><a href="tel:18009918881">(800) 991-8881</a></li><li><a href="tel:16262825388">(626) 282-5388</a></li></ul></div>
</div><div class="ui-footer-legal"><span>{c["copyright"]}</span>{legal}</div></div></footer>'''

    def stickybar(self, c):
        return f'<div class="ui-stickybar" role="region" aria-label="{c["book"]}">{self.btn(c["book"],"primary","calendar")}{self.btn(c["message"],"secondary","message")}</div>'

    def homepage(self, c, cur):
        K=self.K
        return f'''<div class="ui-page" lang="{c['html_lang']}">
{self.header(c,cur)}
<main>{self.hero(c)}{self.problem(c)}{self.how(c)}
<section class="ui-section {K.SECTION.get("doctor","")}" id="doctor"><div class="ui-wrap">{self.doctor_card(c)}</div></section>
{self.visit(c)}{self.faq(c)}{self.locations(c)}
<section class="ui-section ui-section--band {K.SECTION.get("band","")}"><div class="ui-wrap">{self.band(c)}</div></section></main>
{self.footer(c,cur)}{self.stickybar(c)}</div>'''

    def form(self, c, state="default"):
        f=c["form"]; zh=c["lang"]=="zh"; L=c['lang']
        A=c["alhambra"]["name"]; W=c["walnut"]["name"]+("（即將開放）" if zh else " (opening soon)")
        err = state=="error"; foc = ' is-focus' if state in ("focus","error") else ''
        val = '' if state=='default' else ('陳美玲' if zh else 'Mei-Ling Chen')
        msg = (f'<p class="ui-error">{self.I("alert")}<span>{f["err"]}</span></p>') if err else f'<p class="ui-hint">{f["hint"]}</p>'
        return f'''<form class="ui-form" onsubmit="return false">
<div class="ui-field"><label class="ui-label" for="p-{L}-{state}">{f["parent"]}</label><input class="ui-input{foc}" id="p-{L}-{state}" autocomplete="name" value="{val}"></div>
<div class="ui-field{' is-error' if err else ''}"><label class="ui-label" for="t-{L}-{state}">{f["phone"]}</label><input class="ui-input" id="t-{L}-{state}" type="tel" autocomplete="tel" placeholder="(626) 000-0000" {'aria-invalid="true"' if err else ''}>{msg}</div>
<div class="ui-field"><label class="ui-label" for="a-{L}-{state}">{f["age"]}</label><select class="ui-input" id="a-{L}-{state}" style="max-width:200px"><option>{f["age_ph"]}</option>{''.join(f'<option>{i}</option>' for i in range(5,19))}</select></div>
<fieldset class="ui-field ui-fieldset"><legend class="ui-label">{f["loc"]}</legend><div class="ui-radios">
<label class="ui-radio is-checked"><input type="radio" name="l-{L}-{state}" checked>{A}</label><label class="ui-radio is-disabled"><input type="radio" disabled name="l-{L}-{state}">{W}</label></div></fieldset>
<div><button class="ui-btn ui-btn--primary" type="submit">{self.I("calendar")}<span>{f["submit"]}</span></button></div></form>'''

    # ---------- spec helpers ----------
    @staticmethod
    def lab(t): return f'<p class="ui-spec-label">{t}</p>'
    @staticmethod
    def page(inner, pad=True): return f'<div class="ui-page"><div class="{"ui-spec" if pad else ""}">{inner}</div></div>'
    @staticmethod
    def zh(inner): return f'<div lang="zh-Hant">{inner}</div>'
    def states(self, items): return '<div class="ui-state-grid">'+''.join(f'<div class="ui-state">{self.lab(l)}{h}</div>' for l,h in items)+'</div>'

    def add(self, name, group, height, body, readme, width=None, subtitle="", script="", page_card=False):
        self.comps[name]=(group,height,width,subtitle,body,script,readme,page_card)

    # ---------- the fixed catalogue ----------
    def catalogue(self, tok, cr):
        K=self.K; lab=self.lab; page=self.page; zhw=self.zh
        # 1 Color
        tk={t["name"]:t for t in tok["color"]["tokens"]}
        th=tok["color"]["themes"][0]["id"]
        val=lambda n: tk[n]["value"][th] if isinstance(tk[n]["value"],dict) else tk[n]["value"]
        cards=""
        for n,l in K.ROLES:
            use=re.sub(r"`([^`]+)`",r"<code>\1</code>",tk[n]["usage"])
            cards+=f'''<div class="ui-swatch"><div class="ui-swatch-chip" style="background:var(--{n})"></div>
<div class="ui-swatch-body"><p class="ui-swatch-name">{l}</p><p class="ui-swatch-code">--{n} · {val(n).upper()}</p><p class="ui-swatch-use">{use}</p></div></div>'''
        rows=""
        head="".join(f'<th>{bl}</th>' for b,bl in K.CONTRAST_BGS)
        for f,fl in K.CONTRAST_FGS:
            cells=""
            for b,bl in K.CONTRAST_BGS:
                if (f,b) in K.CONTRAST_SKIP: cells+='<td class="ui-ct-na">—</td>'; continue
                r=cr(val(f),val(b)); ok=r>=4.5; big=3<=r<4.5
                verdict="AA" if ok else ("AA large text only" if big else "fails — never use")
                cells+=f'<td><span class="ui-ct-chip" style="background:{val(b)};color:{val(f)}">Aa {r:.1f}</span><span class="ui-ct-v {"ok" if ok else ("mid" if big else "bad")}">{verdict}</span></td>'
            rows+=f'<tr><th scope="row">{fl}</th>{cells}</tr>'
        self.add("Color","1 · Color",1100,page(lab("Swatches · 10 roles")+f'<div class="ui-swatches">{cards}</div><div style="height:32px"></div>'+lab("Contrast · which text passes on which ground (WCAG AA 4.5:1)")+f'<div style="overflow-x:auto"><table class="ui-ct"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div><p class="ui-small" style="margin-top:12px">{K.CONTRAST_NOTE}</p>'),
            K.README_COLOR, page_card=True)
        # 2 Type
        g=tok["type"]["groups"]
        def st(gi,name): return [x for x in g[gi]["styles"] if x["name"]==name][0]
        rows=""
        for s in ["display","h1","h2","h3","body","small","button"]:
            en,enm,zh,zhm=st(0,f"en-{s}"),st(1,f"en-{s}-m"),st(2,f"zh-{s}"),st(3,f"zh-{s}-m")
            fe=f'var(--font-{en["family"]})'; fz=f'var(--font-{zh["family"]})'
            def sm(x,f,l=None): return f'font-family:{f};font-size:{x["fontSize"]};line-height:{x["lineHeight"]};font-weight:{x["fontWeight"]};letter-spacing:{x.get("letterSpacing","0")}'
            rows+=f'''<tr><td class="ui-ts-meta"><p class="ui-ts-name">{s.upper() if s[0]=="h" else s.title()}</p><p class="ui-small">EN {en["fontSize"]} / {enm["fontSize"]}<br>繁 {zh["fontSize"]} / {zhm["fontSize"]}<br>LH {en["lineHeight"]} · {zh["lineHeight"]}</p></td>
<td><p style="{sm(en,fe)}">{en["sample"]}</p><p class="ui-spec-label" style="margin:10px 0 2px">mobile {enm["fontSize"]}</p><p style="{sm(enm,fe)}">{en["sample"]}</p></td>
<td lang="zh-Hant"><p style="{sm(zh,fz)}">{zh["sample"]}</p><p class="ui-spec-label" lang="en" style="margin:10px 0 2px">mobile {zhm["fontSize"]}</p><p style="{sm(zhm,fz)}">{zh["sample"]}</p></td></tr>'''
        fams="".join(f'<div class="ui-fam"><p class="ui-spec-label">{r}</p><p style="font-family:var(--font-{k});font-size:26px;font-weight:{w};line-height:1.3" {"lang=zh-Hant" if "zh" in k else ""}>{n}</p><p class="ui-small">{note}</p></div>' for r,k,n,w,note in K.FAMILIES)
        self.add("Typography","2 · Typography",1700,page(f'<div class="ui-fams">{fams}</div><div style="overflow-x:auto"><table class="ui-ts"><colgroup><col style="width:150px"><col><col></colgroup><thead><tr><th>Level · desktop / mobile</th><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table></div>'+(K.TYPE_EXTRA if hasattr(K,"TYPE_EXTRA") else "")),
            K.README_TYPE, page_card=True)
        # 3 Spacing & layout
        sp=tok["spacing"]["tokens"]
        bars="".join(f'<div class="ui-sp-row"><code>{t["name"]}</code><span class="ui-small">{t["value"]}</span><div><div class="ui-sp-bar" style="width:{t["value"]}"></div></div></div>' for t in sp)
        cols=lambda n,gp: f'<div class="ui-cols" style="grid-template-columns:repeat({n},1fr);gap:{gp}px">'+''.join('<div></div>' for _ in range(n))+'</div>'
        L={t["name"]:t["value"] for t in tok["layout"]["tokens"]}
        self.add("Spacing & Layout","3 · Spacing & Layout",820,page(f'''{lab("Spacing scale · 8px base")}{bars}<div style="height:24px"></div>
{lab(f'Page · max width {L["page-max"]} content, {L["reading-max"]} reading column')}
<div class="ui-pagebox"><div style="max-width:{L["reading-max"]}" class="ui-readbox">reading-max {L["reading-max"]} — paragraphs, FAQ</div><p class="ui-small" style="text-align:center;margin-top:6px">page-max {L["page-max"]} · 24px side padding (desktop) · {L["gutter-mobile"]} (mobile)</p></div>
<div style="height:24px"></div>{lab("Desktop grid · 12 columns · 24px gutter (≥1024px)")}{cols(12,24)}
<div style="height:16px"></div>{lab("Tablet grid · 8 columns · 24px gutter (768–1023px)")}{cols(8,24)}
<div style="height:16px"></div>{lab(f'Mobile grid · 4 columns · 16px gutter · {L["gutter-mobile"]} margins (&lt;768px)')}<div style="max-width:390px;padding:0 {L["gutter-mobile"]};border:1px dashed var(--border-strong);border-radius:8px">{cols(4,16)}</div>
<p class="ui-small" style="margin-top:16px">{K.SECTION_RHYTHM}</p>'''), K.README_SPACING, page_card=True)
        # 4 Shape
        rads=[t for t in tok["radius"]["tokens"]]
        r="".join(f'<div style="text-align:center"><div class="ui-radbox" style="border-radius:var(--{t["name"]})"></div><p class="ui-small" style="margin-top:6px"><code>{t["name"]}</code> {t["value"]}</p></div>' for t in rads)
        self.add("Shape","4 · Shape",620,page(f'{lab("Corner radius")}<div class="ui-row-wrap">{r}</div><div style="height:24px"></div>{lab("Borders")}{K.SHAPE_BORDERS}<div style="height:24px"></div>{lab("Shadow")}{K.SHAPE_SHADOWS}'),
            K.README_SHAPE, page_card=True)
        # 5 Components
        EN_,ZH_=EN,ZH
        self.add("Primary button","5 · Components",300,page(self.states([("Default",self.btn(EN_["book"],"primary","calendar")),("Hover",self.btn(EN_["book"],"primary","calendar","is-hover")),("Pressed",self.btn(EN_["book"],"primary","calendar","is-pressed")),("Focus (keyboard)",self.btn(EN_["book"],"primary","calendar","ui-focus-demo")),("繁體 · default",zhw(self.btn(ZH_["book"],"primary","calendar"))),("Small (header)",self.btn(EN_["book"],"primary",None,"ui-btn--sm"))])),
            K.README_COMP["Primary button"], subtitle="Default · hover · pressed")
        self.add("Secondary button","5 · Components",300,page(self.states([("Default",self.btn(EN_["message"],"secondary","message")),("Hover",self.btn(EN_["message"],"secondary","message","is-hover")),("Pressed",self.btn(EN_["message"],"secondary","message","is-pressed")),("Focus (keyboard)",self.btn(EN_["message"],"secondary","message","ui-focus-demo")),("繁體 · default",zhw(self.btn(ZH_["message"],"secondary","message"))),("Disabled / coming soon",f'<span class="ui-btn ui-btn--secondary is-disabled">{EN_["soon_btn"]}</span>')])),
            K.README_COMP["Secondary button"], subtitle="Default · hover · pressed")
        self.add("Language switcher","5 · Components",220,page(self.states([("Default (EN current)",self.lang_switch("en")),("Hover on 繁體",self.lang_switch("en",{"zh-Hant":"is-hover"})),("Pressed on 简体",self.lang_switch("en",{"zh-Hans":"is-pressed"})),("繁體 current",self.lang_switch("zh-Hant"))])),
            K.README_COMP["Language switcher"], subtitle="Default · hover · pressed")
        self.add("Top navigation + mobile menu","5 · Components",680,f'''<div class="ui-page"><p class="ui-spec-label" style="padding:16px 24px 8px">Desktop (≥1024px)</p>{self.header(EN_,"en")}
<div class="ui-spec"><p class="ui-spec-label">Nav link states</p><nav class="ui-nav ui-nav--demo"><a href="#">Default</a><a href="#" class="is-hover">Hover</a><a href="#" class="is-pressed">Pressed</a></nav>
<div style="height:24px"></div><p class="ui-spec-label">Mobile (&lt;1024px) · menu open</p>
<div class="ui-phone"><div class="ui-utility"><div class="ui-utility-in" style="padding:0 12px">{self.lang_switch("en")}</div></div>
<div class="ui-header"><div class="ui-header-in" style="padding:0 20px"><span class="ui-brand">{EN_["brand"]}</span><button class="ui-btn ui-btn--secondary ui-btn--sm is-pressed" style="margin-left:auto" aria-expanded="true">{self.I("close")}<span>{EN_["close"]}</span></button></div></div>
<div style="padding:12px">{self.sheet(EN_)}</div></div></div></div>''', K.README_COMP["Top navigation + mobile menu"], subtitle="Desktop · mobile menu", script=MENU_JS, width=1100)
        self.add("Hero block","5 · Components",700,f'<div class="ui-page">{self.hero(EN_)}</div>',K.README_COMP["Hero block"],width=1200,subtitle="EN · desktop")
        self.add("3-step How it works block","5 · Components",560,page(lab("Default")+self.steps_block(EN_)+'<div style="height:24px"></div>'+lab("繁體 · step 2 current")+zhw(self.steps_block(ZH_,current=2))),K.README_COMP["3-step How it works block"])
        self.add("Doctor card","5 · Components",700,f'<div class="ui-page"><div class="ui-wrap" style="padding:32px 24px">{self.doctor_card(EN_)}</div></div>',K.README_COMP["Doctor card"],width=1200)
        self.add("FAQ accordion","5 · Components",760,page(lab("Open · closed · hover (row 3) · pressed (row 4)")+self.faq_block(EN_,0,2,3)+'<div style="height:24px"></div>'+lab("繁體")+zhw(self.faq_block(ZH_,1))),K.README_COMP["FAQ accordion"],subtitle="Open · closed · hover · pressed")
        self.add("Booking call-to-action band","5 · Components",420,f'<div class="ui-page"><div style="padding:24px">{self.band(EN_)}<div style="height:16px"></div><div lang="zh-Hant">{self.band(ZH_)}</div></div></div>',K.README_COMP["Booking call-to-action band"],width=1100)
        self.add("Location card","5 · Components",640,f'<div class="ui-page"><div style="padding:24px"><div class="ui-locs">{self.loc_card(EN_,"alhambra")}{self.loc_card(EN_,"walnut")}</div></div></div>',K.README_COMP["Location card"],width=1100)
        self.add("Contact row","5 · Components",340,page(lab("Default")+self.contact_row(EN_)+'<div style="height:16px"></div>'+lab("Hover (Book online) · pressed (WeChat)")+self.contact_row(EN_,1,2)+'<div style="height:16px"></div>'+lab("繁體")+zhw(self.contact_row(ZH_))),K.README_COMP["Contact row"],subtitle="Default · hover · pressed")
        self.add("Form field set","5 · Components",900,f'<div class="ui-page"><div class="ui-spec ui-form-demo"><div>{lab("Default · EN")}{self.form(EN_)}</div><div>{lab("Focus + error · EN")}{self.form(EN_,"error")}</div><div lang="zh-Hant">{lab("繁體 · filled")}{self.form(ZH_,"filled")}</div></div></div>',K.README_COMP["Form field set"],width=1100)
        self.add("Footer","5 · Components",380,f'<div class="ui-page">{self.footer(EN_,"en")}</div>',K.README_COMP["Footer"],width=1200)
        for name,h,body,rd,w in K.extras(self):
            self.add(name,f"5 · Components · Concept {K.KEY} extra",h,body,rd,width=w)
        # 6 Icons
        ic="".join(f'<div class="ui-iconcard">{self.I(n,"ui-ico ui-ico--xl")}<p class="ui-ts-name">{n}</p><p class="ui-small">{u}</p></div>' for n,u in [("eye","Exams, the eye map, eyebrows"),("moon","Wear at night"),("sun","See clearly all day"),("calendar","Booking"),("phone","Call"),("question","Parent questions")])
        more="".join(f'<span class="ui-chip">{self.I(n)}{n}</span>' for n in ["message","pin","lens","clock","map","camera","check","alert","menu","close","arrow"])
        self.add("Icons","6 · Icons",620,page(lab("The six sample icons")+f'<div class="ui-icongrid">{ic}</div><div style="height:20px"></div>'+lab("Rest of the set, same rules")+f'<div class="ui-chips">{more}</div><div style="height:20px"></div>'+lab("Sizes: 16 · 20 · 24 · 32 · 48px")+'<div class="ui-row-wrap" style="align-items:end">'+"".join('<span style="font-size:%dpx;display:inline-flex">%s</span>'%(z,self.I("eye")) for z in (16,20,24,32,48))+'</div>'),
            K.README_ICONS, page_card=True)
        self.add("Imagery","7 · Imagery",K.IMAGERY_H,page(K.imagery(self)),K.README_IMAGERY,page_card=True)
        v=K.VOICE
        self.add("Voice & Tone","8 · Voice & Tone",620,page(f'''<div class="ui-chips" style="margin-bottom:24px">{"".join(f'<span class="ui-chip ui-chip--lg">{w}</span>' for w in v["words"])}</div>
<div class="ui-voice"><div class="ui-voice-card ui-voice-card--right"><p class="ui-spec-label">{self.I("check")} Done right</p><p class="ui-h3">{v["right_en"]}</p><p class="ui-h3" lang="zh-Hant">{v["right_zh"]}</p><p class="ui-small">{v["right_why"]}</p></div>
<div class="ui-voice-card ui-voice-card--wrong"><p class="ui-spec-label">{self.I("alert")} Done wrong</p><p class="ui-body">{v["wrong_en"]}</p><p class="ui-body" lang="zh-Hant">{v["wrong_zh"]}</p><p class="ui-small">{v["wrong_why"]}</p></div></div>'''),
            K.README_VOICE, page_card=True)
        # 9 Homepages
        self.add("Homepage desktop EN","9 · Homepage",4000,self.homepage(EN_,"en"),"# Homepage desktop EN\n\nThe full homepage at 1280px, built only from the components above.",width=1280,script=MENU_JS)
        self.add("Homepage mobile EN","9 · Homepage",4000,self.homepage(EN_,"en"),"# Homepage mobile EN\n\nThe same page at 390px. Language switcher in the top bar, Menu opens the sheet, a sticky Book / Message bar follows the scroll.",width=390,script=MENU_JS)
        self.add("Homepage Traditional Chinese desktop","9 · Homepage",4000,self.homepage(ZH_,"zh-Hant"),"# Homepage Traditional Chinese desktop\n\n繁體中文首頁，1280px。",width=1280,script=MENU_JS)
        self.add("Homepage Traditional Chinese mobile","9 · Homepage",4000,self.homepage(ZH_,"zh-Hant"),"# Homepage Traditional Chinese mobile\n\n繁體中文首頁，390px。",width=390,script=MENU_JS)

    def write(self, root):
        K=self.K; out=os.path.join(root,"project/components"); loc=os.path.join(root,"local")
        for name,(group,height,width,subtitle,body,script,readme,pc) in self.comps.items():
            attrs=f'group="{group}" height={height}'+(f' width={width}' if width else '')+(f' subtitle="{subtitle}"' if subtitle else '')+(' page' if pc else '')
            lang="zh-Hant" if "Chinese" in name else "en"
            h=doc(K, name, body, f"<!-- @dsCard {attrs} -->", lang, script)
            for base,local in ((out,False),(loc,True)):
                d=os.path.join(base,name); os.makedirs(d,exist_ok=True)
                hh=h
                if local:
                    hh=h.replace("</head>",'<link rel="stylesheet" href="../../tokens.local.css"><link rel="stylesheet" href="../../project/components/bundle.css"></head>').replace("<html lang",'<html data-theme="light" lang')
                open(os.path.join(d,"preview.html"),"w").write(hh)
            open(os.path.join(out,name,"README.md"),"w").write(readme+"\n")
        hdr={"format":4,"namespace":K.NAMESPACE,"components":[{"name":n} for n in self.comps]}
        open(os.path.join(out,"bundle.js"),"w").write("/* @ds-bundle: "+json.dumps(hdr,ensure_ascii=False)+" */\nwindow."+K.NAMESPACE+" = { concept: '"+K.KEY+"', name: '"+K.NAME+"' };\n")

def compile_tokens_css(tok, font_url_prefix="project/"):
    th=tok["color"]["themes"]; first=th[0]["id"]
    def v(t,tid):
        x=t["value"]
        if isinstance(x,dict): return x.get(tid,x[first])
        return x
    css=[]
    for t in th:
        sel=f':root, [data-theme="{t["id"]}"]' if t["id"]==first else f'[data-theme="{t["id"]}"]'
        decl=";".join(f'--{c["name"]}:{v(c,t["id"])}' for c in tok["color"]["tokens"])
        if "shadow" in tok: decl+=";"+";".join(f'--{c["name"]}:{v(c,t["id"])}' for c in tok["shadow"]["tokens"])
        css.append(sel+"{"+decl+"}")
    fams=[k for k in tok if isinstance(tok[k],dict) and "tokens" in tok[k] and k not in ("color","shadow")]
    css.append(":root{"+";".join(f'--{x["name"]}:{x["value"]}' for f in fams for x in tok[f]["tokens"])+";"+";".join(f'--font-{k}:{val}' for k,val in tok["type"]["families"].items())+"}")
    for f in tok["type"].get("fonts",[]):
        css.append(f"@font-face{{font-family:'{f['family']}';src:url({font_url_prefix}{f['file']}) format('woff2');font-weight:{f['weight']};font-display:swap}}")
    return "\n".join(css)

def type_groups(S, fams):
    """S rows: name, en_d, en_m, en_lh, en_w, zh_d, zh_m, zh_lh, zh_w, sampleEN, sampleZH"""
    en_d,en_m,zh_d,zh_m=[],[],[],[]
    for n,ed,em,el,ew,zd,zm,zl,zw,se,sz in S:
        head = n in ("display","h1","h2","h3","button")
        fe="en-heading" if head else "en-body"; fz="zh-heading" if head else "zh-body"
        en_d.append({"name":f"en-{n}","family":fe,"fontSize":f"{ed}px","lineHeight":el,"fontWeight":ew,"sample":se,"usage":f"English {n}, desktop (≥768px). Mobile: `en-{n}-m` ({em}px)."})
        en_m.append({"name":f"en-{n}-m","family":fe,"fontSize":f"{em}px","lineHeight":el,"fontWeight":ew,"sample":se,"usage":f"English {n}, mobile (<768px)."})
        zh_d.append({"name":f"zh-{n}","family":fz,"fontSize":f"{zd}px","lineHeight":zl,"fontWeight":zw,"letterSpacing":"0.02em","sample":sz,"usage":f"Traditional Chinese {n}, desktop. Mobile: `zh-{n}-m` ({zm}px)."})
        zh_m.append({"name":f"zh-{n}-m","family":fz,"fontSize":f"{zm}px","lineHeight":zl,"fontWeight":zw,"letterSpacing":"0.02em","sample":sz,"usage":f"Traditional Chinese {n}, mobile (<768px)."})
    return [{"name":"English · desktop","family":"en-heading","styles":en_d},{"name":"English · mobile","family":"en-heading","styles":en_m},{"name":"繁體中文 · desktop","family":"zh-heading","styles":zh_d},{"name":"繁體中文 · mobile","family":"zh-heading","styles":zh_m}]
