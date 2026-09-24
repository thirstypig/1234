"""Concept B — Grid-Paper Classroom. Leads with PATTERN (田字格 / 作文簿)."""
import re
from base import PATHS, EN, ZH

KEY="B"; NAME="Grid-Paper Classroom"; NAMESPACE="GridPaperB"
TITLE="Concept B · Grid-Paper Classroom"
FONT_URL="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Atkinson+Hyperlegible:wght@400;700&family=LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"
ZH_BOX_LEVELS=("display","h2")
SECTION={"hero":"b-gridbg","how":"b-gridbg b-section-rule","problem":"b-section-rule","doctor":"b-section-rule","visit":"b-section-rule","faq":"b-section-rule","locations":"b-section-rule"}

# ---------- icons: felt-marker style (a soft bleed stroke under a crisp stroke) ----------
def icon(name, cls="ui-ico"):
    p=PATHS[name]
    return (f'<svg class="{cls} b-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'<g stroke-width="3.6" opacity=".18" transform="translate(.5 .6)">{p}</g><g stroke-width="2.3">{p}</g></svg>')

REDCHECK='<svg class="b-check" viewBox="0 0 40 32" aria-hidden="true"><path d="M3 17c4 2.5 7 6 9.5 11C18 16 26 7 37 3" fill="none" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def _strip(t): return re.sub(r"<[^>]+>","",t)
def zh_heading(tag, level, text, cls=""):
    lines=[_strip(x) for x in re.split(r"<br\s*/?>", text)]
    out=[]
    for li,line in enumerate(lines):
        hl=' b-boxline--hl' if (level=="display" and li==1) else ''
        out.append(f'<span class="b-boxline{hl}" aria-hidden="true">'+"".join(f'<span class="b-box">{ch}</span>' for ch in line)+'</span>')
    plain="".join(lines)
    return f'<{tag} class="ui-{level} b-boxed {cls}" aria-label="{plain}">{"".join(out)}</{tag}>'

def sticker(text, tone="yellow", tilt=-4, icon_name=None, shape="round"):
    ic=icon(icon_name) if icon_name else ""
    return f'<span class="b-sticker b-sticker--{tone} b-sticker--{shape}" style="--tilt:{tilt}deg">{ic}<span>{text}</span></span>'

def pasted(label, sub, ratio="4/5", tilt=-1.5, tape=True):
    t='<span class="b-tape b-tape--l" aria-hidden="true"></span><span class="b-tape b-tape--r" aria-hidden="true"></span>' if tape else ''
    return f'''<figure class="b-pasted" style="--tilt:{tilt}deg">{t}<div class="ui-photo" style="aspect-ratio:{ratio}" role="img" aria-label="{label}">{icon("camera")}<span>{label}<small>{sub}</small></span></div></figure>'''

def hero_aside(B, c):
    zh=c["lang"]=="zh"
    return f'''<div class="b-hero-art">{pasted("照片：戴完鏡片、上學不用戴眼鏡的孩子" if zh else "Photo: a child at school, no glasses", "自然光・真實病人（家長同意）" if zh else "Real patient, parent's consent, natural light", "4/5", 2)}
<div class="b-hero-stickers">{sticker(c["trust"][0][1],"red",-5,"eye","tag")}{sticker(c["trust"][1][1],"yellow",4,None,"round")}</div></div>'''
def hero_trust(B, c):
    return f'<ul class="b-checklist b-checklist--compact">'+"".join(f'<li class="{"b-mobile-only" if i<2 else ""}">{REDCHECK}<span>{t}</span></li>' for i,(_,t) in enumerate(c["trust"]))+'</ul>'
def hero_after(B, c): return ""
def step_marker(B, c, i, ic):
    return f'<span class="b-numbox" aria-hidden="true"><span>{i}</span></span><span class="b-step-ico">{icon(ic)}</span>'
def how_art(B, c): return sticker("3 步驟" if c["lang"]=="zh" else "3 steps","green",-3,None,"tag")
def doctor_photo(B, c):
    return pasted(c["photo"], "胡醫師與小病人一起，自然光" if c["lang"]=="zh" else "Dr. Woo at eye level with the child, natural light", "4/5", -2)
def loc_media(B, c, key, soon):
    lab = c["map_soon"] if soon else c["map"]
    return f'<div class="ui-map b-map" role="img" aria-label="{lab}">{icon("map")}<span>{lab}</span></div>'
def band_art(B, c): return ""

def extras(B):
    lab=B.lab
    grid=f'''<div class="ui-spec"><div class="b-spec-grid">
<div>{lab("Exercise-book grid · section background")}<div class="b-gridbg b-swatchgrid"></div><p class="ui-small">Cell <code>grid-cell</code> 24px · line <code>grid-line</code> 1px · every 4th line <code>grid-line-strong</code></p></div>
<div>{lab("田字格 box · headline characters")}<div style="display:flex;gap:10px;align-items:center">{zh_heading("div","h2","看得清楚")}</div><p class="ui-small">Box = 1 character, outer line <code>grid-line-strong</code>, dashed centre cross <code>grid-line</code>. Punctuation takes its own box.</p></div>
<div>{lab("Number box · step numbers")}<div style="display:flex;gap:12px">{"".join(f'<span class="b-numbox"><span>{i}</span></span>' for i in (1,2,3))}</div><p class="ui-small">Numbers sit in a 田字格 box on steps only.</p></div></div>
<div style="height:24px"></div>{lab("Where the grid is allowed — and where it isn't")}
<div class="ui-dodont"><ul class="ok"><li>{icon("check")}<span>Hero and How-it-works section backgrounds</span></li><li>{icon("check")}<span>Step numbers (number box)</span></li><li>{icon("check")}<span>Chinese display and H2 headlines, one character per box</span></li><li>{icon("check")}<span>The cover and sticker-sized decorations</span></li></ul>
<ul class="no"><li>{icon("alert")}<span>Behind body text, FAQ answers, forms or addresses — these sit on white paper cards</span></li><li>{icon("alert")}<span>English headlines (no boxes; letters don't fit a square)</span></li><li>{icon("alert")}<span>Long H1/H3 Chinese headlines (too many boxes to read)</span></li><li>{icon("alert")}<span>More than two grid sections in a row</span></li></ul></div></div>'''
    stick=f'''<div class="ui-spec"><div class="ui-state-grid">
<div class="ui-state">{lab("Round · pencil yellow")}{sticker("30 years of ortho-k experience","yellow",4,None,"round")}</div>
<div class="ui-state">{lab("Tag · red pen")}{sticker("Dr. Paul T. Woo, OD","red",-4,"eye","tag")}</div>
<div class="ui-state">{lab("Tag · grid green")}{sticker("3 steps","green",-3,None,"tag")}</div>
<div class="ui-state" lang="zh-Hant">{lab("繁體")}{sticker("近30年角膜塑型經驗","yellow",3,None,"round")}</div></div></div>'''
    checked=f'''<div class="ui-spec"><div class="b-spec-grid">
<div>{lab("Checked list · EN")}<ul class="b-checklist">{"".join(f"<li>{REDCHECK}<span>{t}</span></li>" for _,t in EN["trust"])}</ul></div>
<div lang="zh-Hant">{lab("繁體")}<ul class="b-checklist">{"".join(f"<li>{REDCHECK}<span>{t}</span></li>" for _,t in ZH["trust"])}</ul></div></div></div>'''
    return [
      ("Grid pattern",620,f'<div class="ui-page">{grid}</div>',"# Grid pattern\n\nThe 作文簿 / 田字格 exercise-book grid is a design element with rules: section backgrounds (hero, How it works), step number boxes, and Chinese display/H2 headlines one character per box. Never behind body text — reading copy always sits on a white `surface` card.",1100),
      ("Sticker badge",260,f'<div class="ui-page">{stick}</div>',"# Sticker badge\n\nShort trust facts as stickers slapped on the page: white die-cut edge, small tilt (−5° to +5°), crisp sticker shadow. Round = pencil yellow with ink text; tag = red pen or grid green with white text. Max two per screen, never on body text, never for claims the client hasn't given.",1100),
      ("Checked list",300,f'<div class="ui-page">{checked}</div>',"# Checked list\n\nA list marked off with a red-pen check — the way a good teacher marks correct answers. Used for trust facts in the hero and in How it works. Check = `secondary` (red pen); text = `text-primary`.",1100),
    ]

ROLES=[("primary","Primary"),("secondary","Secondary"),("accent","Accent"),("background","Background"),("surface","Surface (cards)"),("text-primary","Text Primary"),("text-secondary","Text Secondary"),("border","Border"),("success","Success"),("error","Error")]
CONTRAST_FGS=[("text-primary","Text Primary"),("text-secondary","Text Secondary"),("primary","Primary (as text)"),("secondary","Red pen (as text)"),("success","Success"),("error","Error"),("on-primary","On-primary (white)")]
CONTRAST_BGS=[("background","Background"),("paper","Grid paper"),("accent","Pencil yellow"),("wash","Wash"),("primary","Primary fill"),("secondary","Red-pen fill")]
CONTRAST_SKIP={(f,b) for f,_ in CONTRAST_FGS for b in ("primary","secondary") if f!="on-primary"}|{("on-primary",b) for b in ("background","paper","accent","wash")}
CONTRAST_NOTE="Pencil yellow is a sticker and highlight color only: ink and text-secondary pass on it; green and red text don't. Grid lines are decorative (no contrast requirement) and never sit under body text. Control edges use <code>border-strong</code> (3.4:1+). Focus ring = <code>text-primary</code>, 16:1."

COLORS=[
("primary","#1D6A48","PRIMARY · Grid green. Primary button fill, links, step numerals. White on it 6.6:1. As text: on `background`, `paper`, `wash` (5.9:1+). Not on `accent`."),
("primary-hover","#175A3C","Primary button hover. White 8.2:1."),
("primary-pressed","#104530","Primary button pressed. White 11:1."),
("on-primary","#FFFFFF","Text and icons on `primary` and `secondary` fills."),
("secondary","#C2272D","SECONDARY · Red pen. Check marks, the current-language underline, tag stickers, the first-visit numerals. As text 5.5:1+ on white and paper — short labels only. White on it 5.8:1."),
("accent","#F7CB46","ACCENT · Pencil yellow. Round stickers, the highlighted line of the hero headline boxes. Only `text-primary` (10.4:1) and `text-secondary` (4.7:1) on it."),
("background","#FFFFFF","BACKGROUND · White exercise-book paper. Most of the page stays plain white so it reads trustworthy."),
("paper","#F6FAF7","Grid sections' ground, under the grid lines. `text-primary` 15:1."),
("surface","#FFFFFF","SURFACE · Cards. White cards with a `border` edge; body copy always sits on these, never on the grid."),
("wash","#EEF5F0","Hover wash behind secondary buttons, nav links, FAQ rows."),
("wash-strong","#DDEBE2","Pressed wash; the open FAQ row."),
("text-primary","#18241E","TEXT PRIMARY · Pencil-lead ink. Headlines and body on every ground (13:1+)."),
("text-secondary","#4B5A52","TEXT SECONDARY. Captions, hours, hints, footer on white/paper/wash (5.9:1+)."),
("border","#D3DDD6","BORDER · Card edges and dividers (decorative)."),
("border-strong","#7B8B82","Control edges — fields, contact chips (3.4:1+ on white and paper)."),
("grid-line","#C9E0D1","Exercise-book grid line and 田字格 centre cross. Decorative."),
("grid-line-strong","#8DBFA2","Every 4th grid line and the outer edge of each 田字格 box. Decorative."),
("success","#1D6A48","SUCCESS · Same grid green, always with a check icon and words."),
("error","#A3171C","ERROR · Darker than red pen (7.8:1 on white) and always with an alert icon and a sentence."),
("footer","#16392A","Footer ground (deep green blackboard). `on-primary` on it 12.6:1."),
]
FAMILIES=[("English heading","en-heading","Fredoka 600",600,"Google Fonts · OFL · bold, rounded"),("English body","en-body","Atkinson Hyperlegible",400,"Google Fonts · OFL · made for legibility"),("Chinese heading","zh-heading","霞鶩文楷 TC",700,"LXGW WenKai TC · OFL · 楷書, handwriting-practice feel"),("Chinese body","zh-body","思源黑體 Noto Sans TC",400,"Google Fonts · OFL · plain and clear")]
TYPE=[("display",56,40,1.1,600,52,36,1.3,700,"Clear vision all day.","白天看得清楚，"),("h1",40,32,1.15,600,38,30,1.35,700,"Book a visit at either clinic","兩間診所，歡迎預約"),("h2",30,26,1.2,600,30,24,1.4,700,"How ortho-k works","角膜塑型怎麼進行"),("h3",22,20,1.3,600,22,20,1.5,700,"Custom lenses made for your child","為孩子量身訂製鏡片"),("body",18,17,1.6,400,18,17,1.8,400,"Your child wears special lenses while they sleep.","孩子晚上睡覺時戴上特製鏡片，早上取下就能看清楚。"),("small",15,14,1.5,400,15,15,1.7,400,"Tue & Fri 12–6 pm, Sat 12–4 pm","週二及週五 中午12點至下午6點"),("button",17,17,1.0,600,17,17,1.0,500,"Book a consultation","預約諮詢")]
RADIUS=[("radius-sm","3px","SMALL: chips, language tab, number boxes."),("radius-md","6px","MEDIUM: buttons, fields, FAQ rows, contact chips."),("radius-lg","8px","LARGE: cards, booking band, menu sheet. Paper corners stay crisp."),("radius-sticker","999px","Round stickers only.")]
SHADOWS=[("shadow-none","none","Cards and fields: flat paper."),("shadow-sticker","0 1px 0 rgba(24, 36, 30, 0.10), 0 3px 6px rgba(24, 36, 30, 0.14)","Stickers and pasted photos — the slight lift of something stuck on."),("shadow-float","0 10px 28px rgba(24, 36, 30, 0.16)","Mobile menu sheet and sticky bar only.")]
EXTRA_FAMILIES={"pattern":{"note":"The exercise-book grid.","tokens":[{"name":"grid-cell","value":"24px","usage":"Grid cell size on section backgrounds (3 × space-1)."},{"name":"grid-major","value":"96px","usage":"Every 4th line is `grid-line-strong`."},{"name":"box-size","value":"1.25em","usage":"田字格 headline box: 1.25 × the headline font size, one character per box."}]}}
SECTION_RHYTHM="Sections: 80px top and bottom on desktop (<code>space-10</code>), 64px on mobile. Sections are separated by a 2px <code>grid-line-strong</code> rule, like the margin line of an exercise book."
SHAPE_BORDERS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px"><b>Hairline</b><p class="ui-small">1px <code>border</code> — cards, dividers</p></div><div class="ui-fam" style="width:220px;border:1.5px solid var(--border-strong)"><b>Control</b><p class="ui-small">1.5px <code>border-strong</code> — fields, chips</p></div><div class="ui-fam" style="width:220px;border-top:2px solid var(--grid-line-strong)"><b>Section rule</b><p class="ui-small">2px <code>grid-line-strong</code> between sections</p></div><div class="ui-fam" style="width:220px;border:1px dashed var(--border-strong)"><b>Placeholder</b><p class="ui-small">1px dashed — coming soon, draft copy</p></div></div>'''
SHAPE_SHADOWS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px"><b>shadow-none</b><p class="ui-small">Cards and fields</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-sticker);transform:rotate(-2deg)"><b>shadow-sticker</b><p class="ui-small">Stickers and pasted photos</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-float)"><b>shadow-float</b><p class="ui-small">Menu sheet, sticky bar</p></div></div>'''

IMAGERY_H=640
def imagery(B):
    return f'''<div class="b-spec-grid" style="align-items:start">{pasted("Photo: Dr. Woo with a child patient","Pasted in: white border, tape, a small tilt","4/5",-2)}
<div class="ui-stack-lg"><p class="ui-body">Real photos only, framed like prints pasted into an exercise book: 10px white border, one or two strips of translucent yellow tape, a tilt between −2° and +2°, <code>shadow-sticker</code>. No illustrations or storybook scenes.</p>
<div class="ui-dodont"><ul class="ok"><li>{icon("check")}<span>Real patients and the real clinic, with written parental consent</span></li><li>{icon("check")}<span>Natural light, everyday moments: a child reading, walking into school</span></li><li>{icon("check")}<span>Max two pasted photos per screen</span></li></ul>
<ul class="no"><li>{icon("alert")}<span>Stock photos, watercolor, storybook illustration</span></li><li>{icon("alert")}<span>Photos placed on top of the grid behind body text</span></li><li>{icon("alert")}<span>Close-ups of lenses on fingertips</span></li></ul></div></div></div>'''
VOICE=dict(words=["Encouraging","Clear","Patient"],
  right_en="Great question. Here's how it works, one step at a time.", right_zh="問得好！我們一步一步來說明。", right_why="Praises the question, then teaches in small steps.",
  wrong_en="Failure to comply with the lens-care protocol may result in adverse outcomes.", wrong_zh="若未遵守鏡片護理規範，可能導致不良後果。", wrong_why="Scolds instead of teaches. A good teacher explains why and how.")

README_COLOR="# Color\n\nWhite paper with three school-supply accents: grid green (actions), red pen (checks and marks), pencil yellow (stickers). Lots of white keeps it trustworthy."
README_TYPE="# Typography\n\nFredoka for English headlines, Atkinson Hyperlegible for English body. 霞鶩文楷 TC (a 楷書 face like handwriting practice) for Chinese headlines, sitting in 田字格 boxes at display and H2; Noto Sans TC for Chinese body."
README_SPACING="# Spacing & Layout\n\n8px steps; the background grid cell is 24px (3 steps) so boxes, rules and components line up on it."
README_SHAPE="# Shape\n\nSmall radii and crisp edges like paper and stickers. Flat by default; only stickers and pasted photos lift."
README_ICONS="# Icons\n\nSimple drawn line icons in a felt-marker style: 2.3px round stroke with a faint offset bleed underneath. Color `text-primary` or `primary`; red-pen `secondary` only for check marks. Never emoji."
README_IMAGERY="# Imagery\n\nReal photos, pasted in like prints in an exercise book."
README_VOICE="# Voice & Tone\n\nEncouraging, clear, patient — a good teacher who praises the question and explains in small steps."
README_COMP={
 "Primary button":"# Primary button\n\nGrid-green fill, white label, marker calendar icon. Hover darkens, pressed darkens further and drops 1px. Used for booking only.",
 "Secondary button":"# Secondary button\n\nWhite with a 1.5px ink outline — like a boxed answer. Messaging, directions, and every non-booking action. Disabled is dashed.",
 "Language switcher":"# Language switcher\n\nEN / 简体 / 繁體 in the top bar on every page and in the footer; each goes to its own page. Current = ink with a red-pen underline.",
 "Top navigation + mobile menu":"# Top navigation + mobile menu\n\nPlain-text name in Fredoka (no logo), five links, a small Book button. Below 1024px: Menu opens a white sheet; the language switcher stays visible in the top bar.",
 "Hero block":"# Hero block\n\nGrid-paper background. English headline in Fredoka; Chinese headline written into 田字格 boxes with the second line highlighted in pencil yellow. Right: a pasted-in photo with a red-pen tag sticker (Dr. Woo) and a yellow round sticker (30 years). Under the buttons, a red-checked list of the remaining trust facts.",
 "3-step How it works block":"# 3-step How it works block\n\nA checked homework list on a white card: each row has its number in a 田字格 box, a marker icon, the step, and a red-pen check.",
 "Doctor card":"# Doctor card\n\nPasted-in photo of Dr. Woo with a child (tape + tilt), name as H1, the provided lines, languages as chips, Book button.",
 "FAQ accordion":"# FAQ accordion\n\nWhite rows with ink edges, marker question icon, +/− on the right. Answers on white only — never on the grid.",
 "Booking call-to-action band":"# Booking call-to-action band\n\nA grid-paper card with a heavy green top rule — the last page of the notebook — with Book + Message.",
 "Location card":"# Location card\n\nWhite card: map placeholder, name with its other-language name, address, hours, phones, Book here + Directions. Walnut shows coming soon and a dashed disabled button.",
 "Contact row":"# Contact row\n\nCall, Book online, WeChat, LINE, WhatsApp as outlined chips. App icons are dashed placeholders for the official marks.",
 "Form field set":"# Form field set\n\nLabels above, 52px fields, 1.5px `border-strong`, ink focus ring; errors in dark red with an alert icon and a sentence.",
 "Footer":"# Footer\n\nDeep-green blackboard ground with white text: name, languages, both clinics, phones, legal links.",
}
COVER_DERIVATION=""

CSS=r"""
/* ===== SKIN · Concept B · Grid-Paper Classroom ===== */
:root{--w-head:600;--w-label:600;--w-zh-head:700;--w-zh-label:500;
 --radius-btn:var(--radius-md);--radius-input:var(--radius-md);--focus:var(--text-primary);
 --btn-bg:var(--primary);--btn-fg:var(--on-primary);--btn-bg-hover:var(--primary-hover);--btn-bg-pressed:var(--primary-pressed);
 --btn2-bg:var(--surface);--btn2-fg:var(--text-primary);--btn2-border:var(--text-primary);
 --lang-mark:var(--secondary);--utility-bg:var(--background);--header-bg:var(--background);--brand-ink:var(--text-primary);
 --icon:var(--primary);--numeral:var(--secondary);--photo-bg:#E9EFEA;--photo-fg:var(--text-secondary);
 --band-bg:var(--paper);--band-fg:var(--text-primary);
 --footer-bg:var(--footer);--footer-fg:#FFFFFF;--footer-muted:#D6E6DC;--footer-rule:#3E6452}
.ui-page:lang(zh) .ui-btn,:lang(zh) .ui-btn,:lang(zh) .ui-nav a,:lang(zh) .ui-sheet-links a{font-family:var(--font-zh-body)}
:lang(zh) .ui-sheet-links a{font-weight:500}
.ui-display,.ui-h1,.ui-h2{letter-spacing:-.005em}
.ui-mark{background:linear-gradient(transparent 55%,var(--accent) 55%,var(--accent) 92%,transparent 92%);padding:0 .08em}
/* grid pattern — allowed zones only */
.b-gridbg{background-color:var(--paper);background-image:
 linear-gradient(var(--grid-line-strong) 1px,transparent 1px),linear-gradient(90deg,var(--grid-line-strong) 1px,transparent 1px),
 linear-gradient(var(--grid-line) 1px,transparent 1px),linear-gradient(90deg,var(--grid-line) 1px,transparent 1px);
 background-size:var(--grid-major) var(--grid-major),var(--grid-major) var(--grid-major),var(--grid-cell) var(--grid-cell),var(--grid-cell) var(--grid-cell);background-position:-1px -1px}
.b-section-rule{border-top:2px solid var(--grid-line-strong)}
.ui-hero.b-gridbg{border-bottom:2px solid var(--grid-line-strong)}
/* 田字格 boxed headlines */
.b-boxed{display:flex;flex-direction:column;gap:6px}
.b-boxline{display:flex;flex-wrap:wrap;gap:0}
.b-box{position:relative;display:inline-flex;align-items:center;justify-content:center;width:var(--box-size);height:var(--box-size);margin:0 -1px -1px 0;border:1.5px solid var(--grid-line-strong);background:var(--surface);
 background-image:linear-gradient(90deg,transparent calc(50% - .5px),var(--grid-line) calc(50% - .5px),var(--grid-line) calc(50% + .5px),transparent calc(50% + .5px)),linear-gradient(transparent calc(50% - .5px),var(--grid-line) calc(50% - .5px),var(--grid-line) calc(50% + .5px),transparent calc(50% + .5px));line-height:1}
.b-boxline--hl .b-box{background-color:var(--accent)}
.ui-h2.b-boxed{font-size:26px}
@media (max-width:767px){.ui-display.b-boxed{font-size:30px}.ui-h2.b-boxed{font-size:22px}}
/* hero */
.b-hero-art{position:relative;max-width:400px;margin-left:auto;padding:18px 18px 0 0}
.b-hero-stickers{position:absolute;inset:auto 0 -18px -20px;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none}
.b-hero-stickers .b-sticker--round{transform:rotate(var(--tilt)) translate(18px,-8px)}
@media (max-width:1023px){.b-hero-art{margin:0 auto 24px;max-width:340px}}
/* pasted photos */
.b-pasted{position:relative;background:#fff;padding:10px 10px 12px;box-shadow:var(--shadow-sticker);transform:rotate(var(--tilt));margin:0}
.b-pasted .ui-photo{background:var(--photo-bg);border-radius:0}
.b-tape{position:absolute;top:-12px;width:84px;height:26px;background:rgba(247,203,70,.55);border-left:2px dotted rgba(255,255,255,.6);border-right:2px dotted rgba(255,255,255,.6)}
.b-tape--l{left:-16px;transform:rotate(-28deg)}.b-tape--r{right:-16px;transform:rotate(26deg)}
/* stickers */
.b-sticker{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-en-heading);font-weight:600;font-size:16px;line-height:1.2;border:3px solid #fff;box-shadow:var(--shadow-sticker);transform:rotate(var(--tilt))}
:lang(zh) .b-sticker{font-family:var(--font-zh-body);font-weight:700;letter-spacing:.04em}
.b-sticker .ui-ico{width:20px;height:20px}
.b-sticker--round{border-radius:var(--radius-sticker);width:132px;height:132px;padding:14px;justify-content:center;text-align:center;font-size:16px}
.b-sticker--tag{border-radius:var(--radius-md);padding:10px 16px;max-width:260px}
@media (max-width:767px){.b-hero-stickers{left:-8px}.b-sticker--tag{max-width:210px;font-size:15px}.b-sticker--round{width:116px;height:116px;font-size:14px}}
.b-sticker--yellow{background:var(--accent);color:var(--text-primary)}
.b-sticker--red{background:var(--secondary);color:var(--on-primary)}
.b-sticker--green{background:var(--primary);color:var(--on-primary)}
/* checked list */
.b-checklist{list-style:none;padding:0;margin:0;display:grid;gap:4px}
.b-checklist li{display:grid;grid-template-columns:34px 1fr;gap:8px;align-items:center;padding:6px 0;border-bottom:1px dashed var(--border)}
.b-checklist li:last-child{border-bottom:0}
.b-check{width:30px;height:24px;color:var(--secondary)}
.b-checklist--compact .b-mobile-only{display:none}@media (max-width:1023px){.b-checklist--compact .b-mobile-only{display:grid}}
.b-checklist--compact{margin-top:var(--space-3);max-width:520px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:6px 16px}
/* how it works = checked homework list */
.ui-steps{grid-template-columns:1fr;gap:0;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:8px 24px}
.ui-step{flex-direction:row;align-items:center;gap:var(--space-3);border:0;border-radius:0;background:transparent;padding:18px 56px 18px 0;border-bottom:1px dashed var(--border)}
.ui-step:last-child{border-bottom:0}
.ui-step::after{content:"";position:absolute;right:4px;top:50%;width:40px;height:32px;margin-top:-16px;background:no-repeat center/contain url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 32'%3E%3Cpath d='M3 17c4 2.5 7 6 9.5 11C18 16 26 7 37 3' fill='none' stroke='%23C2272D' stroke-width='4.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")}
.ui-step.is-current{background:var(--wash)}
.b-numbox{position:relative;flex:none;display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border:1.5px solid var(--grid-line-strong);border-radius:var(--radius-sm);background-color:var(--surface);
 background-image:linear-gradient(90deg,transparent 27.5px,var(--grid-line) 27.5px,var(--grid-line) 28.5px,transparent 28.5px),linear-gradient(transparent 27.5px,var(--grid-line) 27.5px,var(--grid-line) 28.5px,transparent 28.5px);
 font-family:var(--font-en-heading);font-weight:700;font-size:30px;color:var(--primary)}
.b-step-ico{color:var(--primary);display:inline-flex}.b-step-ico .ui-ico{width:30px;height:30px}
@media (max-width:767px){.ui-steps{padding:4px 16px}.ui-step{padding:14px 44px 14px 0;gap:12px}.b-numbox{width:48px;height:48px;font-size:26px;background-image:linear-gradient(90deg,transparent 23.5px,var(--grid-line) 23.5px,var(--grid-line) 24.5px,transparent 24.5px),linear-gradient(transparent 23.5px,var(--grid-line) 23.5px,var(--grid-line) 24.5px,transparent 24.5px)}.b-step-ico{display:none}.ui-step::after{width:32px;height:26px;margin-top:-13px}}
.ui-how-head{align-items:center}
/* doctor, first visit, faq */
.ui-doctor .b-pasted{max-width:420px}
.ui-n{font-family:var(--font-en-heading)}
.ui-faq details{border-color:var(--border-strong)}
/* band: last page of the notebook */
.ui-band{background-color:var(--paper);border:1px solid var(--border);border-top:6px solid var(--primary);border-radius:var(--radius-lg)}
.ui-band-text,.ui-band .ui-btn-row{position:relative;background:var(--surface);border-radius:var(--radius-md);padding:0}
.ui-band{background-image:linear-gradient(var(--grid-line) 1px,transparent 1px),linear-gradient(90deg,var(--grid-line) 1px,transparent 1px);background-size:var(--grid-cell) var(--grid-cell)}
.ui-band-text{padding:16px 20px;border:1px solid var(--border)}
.ui-band .ui-btn-row{background:transparent}
.b-map{background-color:#EEF3EF}
.b-map .ui-ico{width:26px;height:26px}
.ui-footer .ui-brand{color:#fff}
.b-spec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:32px}
.b-swatchgrid{height:144px;border:1px solid var(--border);border-radius:6px;margin-bottom:8px}
"""

FAMILY_STACKS={"en-heading":"Fredoka, \"Varela Round\", ui-rounded, system-ui, sans-serif","en-body":"\"Atkinson Hyperlegible\", system-ui, sans-serif",
 "zh-heading":"\"LXGW WenKai TC\", \"Kaiti TC\", BiauKai, DFKai-SB, serif","zh-body":"\"Noto Sans TC\", \"PingFang TC\", \"Microsoft JhengHei\", sans-serif"}
INTRO="**Leads with: pattern.** Built around the 田字格 / 作文簿 exercise-book grid that parents from Taiwan, Hong Kong and mainland China grew up writing in. White paper, grid green, red pen, pencil yellow; stickers, red-pen checks and pasted-in photos. Plenty of white keeps it trustworthy."
COLOR_RULES="""- `text-primary` and `text-secondary` pass on every ground: white, `paper`, `wash`, and pencil-yellow `accent` (4.7:1+).
- `primary` (green) text passes on white, `paper` and `wash` (5.3:1+) — **never on yellow** (4.2:1).
- Red pen (`secondary`) is for check marks, the language underline and tag stickers; as text only for short labels on white (5.8:1). **Never on yellow** (3.8:1).
- White on `primary` 6.6:1, on `secondary` 5.8:1.
- `grid-line` and `grid-line-strong` are decorative and never sit under body text.
- `error` (#A3171C) is darker than red pen so an error never reads as a check mark; always with an alert icon and a sentence."""
TYPE_RULES="""- Chinese display and H2 headlines are written into **田字格 boxes**, one character per box (punctuation too), box = 1.25em. The hero's second line fills its boxes with pencil yellow. H1, H3 and long headlines are set plain.
- Chinese buttons, nav and labels use Noto Sans TC 500 (a 楷書 face is too delicate at 17px).
- Chinese body ≥17px, line height 1.8. English headlines never go in boxes.
- **Simplified pages:** swap to LXGW WenKai (SC) and Noto Sans SC — both free on Google Fonts, same look."""
SHAPE_RULES="Borders: 1px `border` for cards; 1.5px `border-strong` for controls; a 2px `grid-line-strong` rule between sections, like an exercise-book margin line. Shadows: none on cards; `shadow-sticker` only on stickers and pasted photos; `shadow-float` on the mobile menu and sticky bar."
IMAGERY_RULES="""Real photos only, framed like prints pasted into an exercise book: 10px white border, translucent yellow tape, a tilt of −2° to +2°, `shadow-sticker`. Homepage photos: a child at school without glasses (hero), Dr. Woo with a child patient (doctor card).

- Do: real patients and the real clinic with written parental consent · natural light · everyday moments · max two pasted photos per screen.
- Don't: stock photos · watercolor or storybook illustration · photos on the grid behind body text · close-ups of lenses on fingertips."""

def cover():
    return """<!-- @dsCard height=300 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Concept B · Grid-Paper Classroom</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;height:100%}
  body{background:var(--background);color:var(--text-primary);font-family:var(--font-en-heading);overflow:hidden}
  .cover{position:relative;width:960px;height:300px;overflow:hidden}
  .band{position:absolute;top:0;left:0;width:960px;height:120px}
  .paper{fill:var(--paper)} .green{fill:var(--primary)} .red{fill:var(--secondary)} .yellow{fill:var(--accent)} .ink{fill:var(--footer)}
  .rule{stroke:var(--grid-line);stroke-width:1} .rule-strong{stroke:var(--grid-line-strong);stroke-width:1.5}
  .words{position:absolute;left:48px;right:48px;bottom:40px}
  .name{margin:0;font-size:56px;line-height:.95;font-weight:600;color:var(--text-primary)}
  .tag{margin:12px 0 0 2px;font-size:14px;line-height:20px;color:var(--text-secondary);max-width:440px}
</style>
</head>
<body>
<div class="cover">
<svg class="band" viewBox="0 0 960 120" aria-hidden="true">
<!--
  blocks      paper ground 960×120 · primary (grid green) 264×96 slab off the top · footer (blackboard) 144×72 · secondary (red pen) 96×48 tag · accent (pencil yellow) 96×96 disc — ~30% of the cover
  arrangement a strip of unequal blocks across the top on the exercise-book grid (top-band skeleton: the name is too wide for the 440px zone)
  pattern     the exercise-book grid itself — a few grid-line rules at the grid-cell pitch (48px here = 2 cells) and grid-line-strong every 96px (grid-major), crossing the blocks' ground
  scales      sides in grid-cell (24px) multiples; corners radius-lg 8, tag radius-md 6, disc = radius-sticker
-->
<rect class="paper" x="0" y="0" width="960" height="120"/>
<path class="rule" d="M0 24H960M0 72H960M144 0V120M240 0V120M432 0V120M528 0V120M720 0V120M816 0V120"/>
<path class="rule-strong" d="M0 48H960M0 96H960M192 0V120M480 0V120M768 0V120"/>
<rect class="green" x="48" y="-16" width="264" height="112" rx="8"/>
<rect class="ink" x="336" y="24" width="144" height="72" rx="8"/>
<rect class="red" x="528" y="48" width="96" height="48" rx="6" transform="rotate(-4 576 72)"/>
<circle class="yellow" cx="720" cy="60" r="48"/>
<rect class="green" x="792" y="72" width="120" height="24" rx="6"/>
</svg>
<div class="words">
<h1 class="name">Concept B · Grid-Paper Classroom</h1>
<p class="tag">The exercise-book grid every parent grew up with — green, red pen, pencil yellow, and a good teacher's voice.</p>
</div>
</div>
</body>
</html>
"""
