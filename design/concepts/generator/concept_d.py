"""Concept D — Calm Clinical. Leads with PHOTOGRAPHY. Premium, calm, specialist-led."""
from base import PATHS, EN, ZH

KEY="D"; NAME="Calm Clinical"; NAMESPACE="CalmClinicalD"
TITLE="Concept D · Calm Clinical"
FONT_URL="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"
SECTION={"how":"d-alt","faq":"d-alt"}

def icon(name, cls="ui-ico"):
    return (f'<svg class="{cls} d-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{PATHS[name]}</svg>')

def photo(label, brief, ratio="4/5", cls=""):
    return f'<figure class="d-photo {cls}"><div class="ui-photo" style="aspect-ratio:{ratio}" role="img" aria-label="{label}">{icon("camera")}<span>{label}<small>{brief}</small></span></div></figure>'

TRUST={"en":[("Your doctor","Dr. Paul T. Woo, OD"),("Experience","30 years of ortho-k experience"),("Specialty","Ortho-k for children, ages 7–18"),("Technology","Full eye exam and a map of the eye")],
       "zh":[("您的醫師","胡超醫師，眼科視學博士"),("經驗","近30年角膜塑型經驗"),("專長","兒童角膜塑型・7–18歲"),("技術","完整眼睛檢查與角膜地圖")]}
TRUST_ICONS=["eye","clock","lens","map"]
def trust_strip(c):
    items="".join(f'<li>{icon(ic)}<div><span class="d-trust-k">{k}</span><span class="d-trust-v">{v}</span></div></li>' for ic,(k,v) in zip(TRUST_ICONS,TRUST[c["lang"]]))
    return f'<ul class="d-trust">{items}</ul>'

def hero_aside(B,c):
    zh=c["lang"]=="zh"
    return photo("照片：胡醫師與放鬆的小病人" if zh else "Photo: Dr. Woo with a relaxed child patient",
                 "自然窗光・暖色調・真實病人（家長同意）" if zh else "Natural window light · warm tones · real patient, parent's consent","4/5","d-photo--hero")
def hero_trust(B,c): return ""
def hero_after(B,c): return f'<div class="ui-wrap d-trust-wrap">{trust_strip(c)}</div>'
def step_marker(B,c,i,ic): return f'<div class="d-step-top"><span class="d-stepnum">{i:02d}</span>{icon(ic)}</div>'
def how_art(B,c):
    zh=c["lang"]=="zh"
    return photo("照片：角膜地形圖儀器" if zh else "Photo: corneal mapping equipment","診間實拍・自然光・無人物特寫" if zh else "In the exam room · natural light · no staged close-ups","16/9","d-photo--equip")
def doctor_photo(B,c):
    return photo(c["photo"],"大尺寸・自然光・視線與孩子同高" if c["lang"]=="zh" else "Large · natural light · Dr. Woo at the child's eye level","4/5","d-photo--doctor")
def loc_media(B,c,key,soon):
    zh=c["lang"]=="zh"
    if soon:
        lab=c["map_soon"]
        return f'<div class="d-locmedia"><div class="ui-map" role="img" aria-label="{lab}">{icon("map")}<span>{lab}</span></div></div>'
    return f'''<div class="d-locmedia d-locmedia--split">{photo("照片：阿罕布拉診所候診區" if zh else "Photo: Alhambra clinic waiting room","", "4/3")}
<div class="ui-map" role="img" aria-label="{c['map']}">{icon("map")}<span>{c["map"]}</span></div></div>'''
def band_art(B,c): return ""

def extras(B):
    lab=B.lab
    ts=f'<div class="ui-page"><div class="ui-spec">{lab("EN")}{trust_strip(EN)}<div style="height:20px"></div>{lab("繁體")}<div lang="zh-Hant">{trust_strip(ZH)}</div></div></div>'
    pb=f'''<div class="ui-page"><div class="ui-spec"><div class="d-photo-specs">
<div>{lab("Hero · 4:5")}{photo("Dr. Woo with a relaxed child patient","Natural window light, warm","4/5")}</div>
<div>{lab("Equipment · 16:9")}{photo("Corneal mapping equipment","In use, in the real room","16/9")}</div>
<div>{lab("Clinic · 4:3")}{photo("Alhambra clinic","Waiting room, daylight","4/3")}</div></div></div></div>'''
    return [("Trust strip",360,ts,"# Trust strip\n\nFour facts directly under the hero: your doctor, experience, specialty, technology — thin line icon, small label, value. Only facts the client has provided; never numbers of patients, rates or awards.",1200),
            ("Photo block",520,pb,"# Photo block\n\nThe photo slot in three fixed ratios: 4:5 people (hero, doctor), 16:9 equipment, 4:3 clinic spaces. `radius-md`, no border, `shadow-sm`. Until real photos exist, the slot shows the shot brief so the photographer knows exactly what to take.",1200)]

ROLES=[("primary","Primary"),("secondary","Secondary"),("accent","Accent"),("background","Background"),("surface","Surface (cards)"),("text-primary","Text Primary"),("text-secondary","Text Secondary"),("border","Border"),("success","Success"),("error","Error")]
CONTRAST_FGS=[("text-primary","Text Primary"),("text-secondary","Text Secondary"),("primary","Deep teal (as text)"),("success","Success"),("error","Error"),("on-primary","White (on teal)")]
CONTRAST_BGS=[("background","White"),("surface-alt","Alt surface"),("secondary","Teal tint"),("accent","Apricot"),("primary","Deep teal")]
CONTRAST_SKIP={(f,"primary") for f,_ in CONTRAST_FGS if f!="on-primary"}|{("on-primary",b) for b in ("background","surface-alt","secondary","accent")}
CONTRAST_NOTE="Apricot is a button fill: its label is <code>text-primary</code> (8.6:1). <code>text-secondary</code>, success and error do not go on apricot. White and the teal tint read on deep teal (9.8:1 / 8.4:1). Control edges use <code>border-strong</code> (3:1+). Focus ring = <code>primary</code> teal, 9.8:1."
COLORS=[
("primary","#0E4A56","PRIMARY · Deep teal. The calm color: headings' accent, icons, links, secondary button outline, the booking band and footer. White on it 9.8:1; as text 8.4:1+ on white, alt and tint."),
("on-primary","#FFFFFF","Text on `primary` (booking band, footer)."),
("secondary","#E3EFF0","SECONDARY · Teal tint. The trust strip, step icon discs, hover washes. A ground only."),
("accent","#F4B183","ACCENT · Soft apricot. The primary (booking) button fill only; label `text-primary` 8.6:1."),
("accent-hover","#EFA06C","Primary button hover. Label 7.4:1."),
("accent-pressed","#E68E55","Primary button pressed. Label 6.2:1."),
("background","#FFFFFF","BACKGROUND · White. Lots of it."),
("surface","#FFFFFF","SURFACE · Cards on white, set apart by `shadow-sm` and a hairline."),
("surface-alt","#F5F8F8","Alternate section ground (How it works, FAQ)."),
("wash","#EEF4F5","Hover wash for secondary controls."),
("wash-strong","#DDE9EB","Pressed wash; the open FAQ row."),
("text-primary","#13262B","TEXT PRIMARY. Headlines and body on white, alt, tint and apricot (8.6:1+)."),
("text-secondary","#4A5C61","TEXT SECONDARY. Captions, labels, hours on white, alt and tint (6:1+). Not on apricot."),
("border","#DCE4E5","BORDER · Hairlines (decorative)."),
("border-strong","#7F9296","Control edges: fields, chips (3:1+)."),
("photo-ground","#E8E1D9","Warm neutral behind photo slots until real photos arrive."),
("photo-ink","#5A4E44","Shot-brief text inside photo slots (6.2:1 on `photo-ground`)."),
("success","#1F6B50","SUCCESS · With a check icon and words. 5.4:1+ on white, alt, tint."),
("error","#B3372B","ERROR · With an alert icon and a sentence. 5.1:1+ on white, alt, tint."),
]
FAMILY_STACKS={"en-heading":"\"Plus Jakarta Sans\", system-ui, -apple-system, \"Segoe UI\", sans-serif","en-body":"\"Plus Jakarta Sans\", system-ui, -apple-system, \"Segoe UI\", sans-serif",
 "zh-heading":"\"Noto Sans TC\", \"PingFang TC\", \"Microsoft JhengHei\", sans-serif","zh-body":"\"Noto Sans TC\", \"PingFang TC\", \"Microsoft JhengHei\", sans-serif"}
FAMILIES=[("English heading","en-heading","Plus Jakarta Sans 700",700,"Google Fonts · OFL · modern, clean"),("English body","en-body","Plus Jakarta Sans 400",400,"Google Fonts · OFL"),("Chinese heading","zh-heading","思源黑體 Noto Sans TC 700",700,"Google Fonts · OFL · clean 黑體"),("Chinese body","zh-body","思源黑體 Noto Sans TC 400",400,"≥17px · line height 1.8")]
TYPE=[("display",56,38,1.08,700,50,34,1.3,700,"Clear vision all day.","白天看得清楚，"),("h1",40,32,1.15,700,38,30,1.35,700,"Book a visit at either clinic","兩間診所，歡迎預約"),("h2",32,26,1.2,700,30,24,1.4,700,"How ortho-k works","角膜塑型怎麼進行"),("h3",20,19,1.35,600,20,19,1.5,500,"Custom lenses made for your child","為孩子量身訂製鏡片"),("body",18,17,1.65,400,18,17,1.8,400,"Your child wears special lenses while they sleep.","孩子晚上睡覺時戴上特製鏡片，早上取下就能看清楚。"),("small",14,14,1.5,500,15,15,1.7,400,"Tue & Fri 12–6 pm, Sat 12–4 pm","週二及週五 中午12點至下午6點"),("button",16,16,1.0,600,17,17,1.0,500,"Book a consultation","預約諮詢")]
RADIUS=[("radius-sm","4px","SMALL: chips, language tab, inputs' inner parts."),("radius-md","6px","MEDIUM: buttons, fields, photos, FAQ rows."),("radius-lg","10px","LARGE: cards, booking band, menu sheet.")]
SHADOWS=[("shadow-sm","0 1px 2px rgba(19, 38, 43, 0.06), 0 4px 12px rgba(19, 38, 43, 0.06)","Cards and photos: a subtle, precise lift."),("shadow-float","0 12px 32px rgba(19, 38, 43, 0.14)","Mobile menu sheet and sticky bar only.")]
SECTION_RHYTHM="Sections: 80px top and bottom on desktop (<code>space-10</code>), 64px on mobile. Sections alternate white and <code>surface-alt</code>; no rules, no decoration."
SHAPE_BORDERS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;border-radius:10px"><b>Hairline</b><p class="ui-small">1px <code>border</code> — cards, dividers</p></div><div class="ui-fam" style="width:220px;border:1.5px solid var(--border-strong);border-radius:6px"><b>Control</b><p class="ui-small">1.5px <code>border-strong</code> — fields</p></div><div class="ui-fam" style="width:220px;border:1px dashed var(--border-strong);border-radius:6px"><b>Placeholder</b><p class="ui-small">Dashed — coming soon, draft copy</p></div></div>'''
SHAPE_SHADOWS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-sm);border-radius:10px"><b>shadow-sm</b><p class="ui-small">Cards and photos</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-float);border-radius:10px"><b>shadow-float</b><p class="ui-small">Menu sheet, sticky bar</p></div></div>'''
IMAGERY_H=700
def imagery(B):
    return f'''<div class="d-img-grid">{photo("Dr. Woo with a relaxed child patient","Natural window light · warm tones","4/5")}
<div class="ui-stack-lg"><p class="ui-body">Large real photographs lead every section: Dr. Woo, the clinic, the eye-measurement equipment, and a relaxed child patient. One photographer, one session, one light: natural window light, warm white balance, soft shadows, real people at ease.</p>
<p class="ui-body">Shot list: (1) Dr. Woo with a child, 4:5 · (2) Dr. Woo portrait, 4:5 · (3) corneal mapping equipment in use, 16:9 · (4) Alhambra waiting room and exam room, 4:3 · (5) a child after a visit, relaxed, no glasses, 4:5.</p>
<div class="ui-dodont"><ul class="ok"><li>{icon("check")}<span>Natural light, warm tones, real patients with written parental consent</span></li><li>{icon("check")}<span>Calm moments: the child smiling, Dr. Woo explaining at eye level</span></li><li>{icon("check")}<span>Equipment shown in use, clean and uncluttered</span></li></ul>
<ul class="no"><li>{icon("alert")}<span>Stock photography, AI images, illustrations, emoji</span></li><li>{icon("alert")}<span>Cold blue clinical light, masks and gloves in the foreground</span></li><li>{icon("alert")}<span>Close-ups of eyes being touched or lenses on fingertips</span></li><li>{icon("alert")}<span>Text or badges on photos</span></li></ul></div></div></div>'''
VOICE=dict(words=["Confident","Calm","Expert, still gentle"],
  right_en="Dr. Woo will examine your child's eyes, map the front of each eye, and explain what he sees. Your child can ask questions too.", right_zh="胡醫師會為孩子檢查眼睛、拍攝角膜地圖，並說明檢查結果。孩子也可以隨時發問。", right_why="Clear expertise, plain words, and room for a nervous child.",
  wrong_en="Our world-class, state-of-the-art clinic delivers unmatched results.", wrong_zh="本中心擁有世界級頂尖設備，效果無人能及。", wrong_why="Empty superlatives and claims. Confidence comes from specifics, not adjectives.")
INTRO="**Leads with: photography.** Premium, calm and specialist-led. Lots of white, one deep teal, one soft apricot for booking buttons, a clean sans, precise alignment and large real photographs. Friendly through warm words, not cartoons."
COLOR_RULES="""- Lots of white. Deep teal `primary` is the one calm color; apricot `accent` is only the booking button's fill.
- `text-primary` passes everywhere, including apricot (8.6:1). `text-secondary`, success and error pass on white, `surface-alt` and teal tint (5.1:1+) — never on apricot.
- On deep teal (booking band, footer): white (9.8:1) and teal tint (8.4:1).
- `border-strong` (3:1+) for control edges. No bright primary colors anywhere."""
TYPE_RULES="""- One family per script for a clean, strong hierarchy: Plus Jakarta Sans and Noto Sans TC, weights 400 / 500 / 700.
- Chinese body ≥17px, line height 1.8; Chinese headings 700, never tracked tight.
- **Simplified pages:** Noto Sans SC — same family, same weights, free on Google Fonts."""
SHAPE_RULES="Small radii (4 / 6 / 10px), precise alignment to the 12-column grid. Borders: 1px `border` hairlines; 1.5px `border-strong` on controls. Shadows: `shadow-sm` on cards and photos; `shadow-float` on the mobile menu and sticky bar."
IMAGERY_RULES="""Large real photographs lead: Dr. Woo, the clinic, the eye-measurement equipment, a relaxed child patient. One photographer, one session: natural window light, warm tones, real people at ease. Fixed ratios: 4:5 people, 16:9 equipment, 4:3 spaces. Until photos exist, each slot shows its shot brief.

- Do: natural light · warm white balance · real patients with written parental consent · equipment shown in use · Dr. Woo at the child's eye level.
- Don't: stock or AI images · illustrations or emoji · cold blue clinical light · masks and gloves in the foreground · eyes being touched · text on photos."""
README_COLOR="# Color\n\nWhite, one deep calm teal, and one soft apricot reserved for booking buttons."
README_TYPE="# Typography\n\nPlus Jakarta Sans and Noto Sans TC: modern, clean, one family per script, strong hierarchy."
README_SPACING="# Spacing & Layout\n\n8px steps, precise 12-column alignment, big photos on the grid."
README_SHAPE="# Shape\n\nSmall radius, subtle shadows, precise edges."
README_ICONS="# Icons\n\nThin, clean line icons: 1.4px stroke, round caps, 24px grid, drawn in `primary` teal. Never emoji or filled icons."
README_IMAGERY="# Imagery\n\nLarge real photographs of the doctor, the clinic, the equipment and a relaxed child."
README_VOICE="# Voice & Tone\n\nConfident, calm, expert — and still gentle with nervous kids."
README_COMP={
 "Primary button":"# Primary button\n\nApricot fill with ink label (8.6:1), 6px radius, semibold. The only warm color on the page, and only for booking.",
 "Secondary button":"# Secondary button\n\nWhite with a 1.5px deep-teal outline and teal label. Messaging, directions, everything else.",
 "Language switcher":"# Language switcher\n\nEN / 简体 / 繁體 in a quiet top bar and in the footer; each is its own page. Current = ink with a teal underline.",
 "Top navigation + mobile menu":"# Top navigation + mobile menu\n\nWhite bar, plain-text name in Plus Jakarta Sans (no logo), five links, a small apricot Book button. Mobile: Menu opens a white sheet.",
 "Hero block":"# Hero block\n\nText left, a large 4:5 photo of Dr. Woo with a relaxed child right. Directly below: the trust strip (doctor, experience, specialty, technology).",
 "3-step How it works block":"# 3-step How it works block\n\nOn `surface-alt` beside a 16:9 equipment photo: three white cards with a 01 / 02 / 03 numeral and a thin line icon.",
 "Doctor card":"# Doctor card\n\nLarge and prominent: a full-width card, big 4:5 portrait of Dr. Woo with a child, name, provided lines, languages, Book.",
 "FAQ accordion":"# FAQ accordion\n\nWhite rows on `surface-alt`, thin question icon, precise +/−.",
 "Booking call-to-action band":"# Booking call-to-action band\n\nDeep-teal band, white heading, apricot Book + white-outline Message.",
 "Location card":"# Location card\n\nClinic photo beside a map placeholder, then name, address, hours, phones, Book here + Directions. Walnut: map coming soon and a dashed disabled button.",
 "Contact row":"# Contact row\n\nQuiet outlined chips with thin icons: Call, Book online, WeChat, LINE, WhatsApp (dashed placeholders for the official marks).",
 "Form field set":"# Form field set\n\nLabels above, 52px fields, 1.5px `border-strong`, teal focus ring, errors with an alert icon and a sentence.",
 "Footer":"# Footer\n\nDeep-teal footer with white text: name, languages, both clinics, phones, legal links.",
}
CSS=r"""
/* ===== SKIN · Concept D · Calm Clinical ===== */
:root{--w-head:700;--w-label:600;--w-zh-head:700;--w-zh-label:500;
 --radius-btn:var(--radius-md);--radius-input:var(--radius-md);--focus:var(--primary);
 --btn-bg:var(--accent);--btn-fg:var(--text-primary);--btn-bg-hover:var(--accent-hover);--btn-bg-pressed:var(--accent-pressed);
 --btn2-bg:var(--surface);--btn2-fg:var(--primary);--btn2-border:var(--primary);
 --lang-mark:var(--primary);--utility-bg:var(--surface-alt);--header-bg:var(--background);--brand-ink:var(--text-primary);
 --icon:var(--primary);--numeral:var(--primary);--photo-bg:var(--photo-ground);--photo-fg:var(--photo-ink);
 --band-bg:var(--primary);--band-fg:var(--on-primary);
 --footer-bg:#0A3942;--footer-fg:#FFFFFF;--footer-muted:#CFE0E3;--footer-rule:#2C5C66}
.ui-display,.ui-h1,.ui-h2{letter-spacing:-.02em}
:lang(zh) :is(.ui-display,.ui-h1,.ui-h2){letter-spacing:.02em}
.ui-h3{font-weight:600}
:lang(zh) .ui-h3{font-weight:500}
.ui-mark{color:var(--primary)}
.ui-eyebrow{text-transform:uppercase;letter-spacing:.1em;font-size:13px;color:var(--primary)}
:lang(zh) .ui-eyebrow{text-transform:none;font-size:15px}
.ui-utility{border-bottom:0}
.ui-step,.ui-faq details,.ui-loc{box-shadow:var(--shadow-sm);border-color:var(--border)}
.d-alt{background:var(--surface-alt)}
/* photos */
.d-photo{margin:0;border-radius:var(--radius-md);overflow:hidden;box-shadow:var(--shadow-sm)}
.d-photo .ui-photo{border-radius:0}
.d-photo .ui-photo small{font-weight:400}
.d-photo--hero .ui-photo{min-height:520px;aspect-ratio:auto!important}
@media (max-width:1023px){.d-photo--hero .ui-photo{min-height:0;aspect-ratio:4/3!important}}
.ui-hero{padding-bottom:0}
@media (min-width:1024px){.ui-hero-grid{grid-template-columns:6fr 6fr;align-items:stretch}}
.ui-hero-text{align-self:center}
/* trust strip */
.d-trust-wrap{margin-top:var(--space-6);padding-bottom:var(--space-4)}
.d-trust{list-style:none;margin:0;padding:var(--space-3);display:grid;grid-template-columns:repeat(4,1fr);gap:var(--space-3);background:var(--secondary);border-radius:var(--radius-lg)}
.d-trust li{display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:start}
.d-trust .ui-ico{width:30px;height:30px;color:var(--primary)}
.d-trust-k{display:block;font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text-secondary)}
:lang(zh) .d-trust-k{font-size:14px;letter-spacing:.1em;text-transform:none;font-weight:500}
.d-trust-v{display:block;font-size:16px;font-weight:600;line-height:1.35;margin-top:2px;color:var(--text-primary)}
:lang(zh) .d-trust-v{font-weight:500;font-size:17px;line-height:1.5}
@media (max-width:1023px){.d-trust{grid-template-columns:1fr 1fr}}
@media (max-width:767px){.d-trust{grid-template-columns:1fr;gap:var(--space-2);padding:var(--space-2)}.d-trust-wrap{margin-top:var(--space-3)}}
/* how */
.ui-how-head{display:grid;grid-template-columns:5fr 7fr;align-items:center;gap:var(--space-6)}
.d-step-top{display:flex;justify-content:space-between;align-items:center;width:100%}
.d-stepnum{font-size:14px;font-weight:700;letter-spacing:.12em;color:var(--primary)}
.d-step-top .ui-ico{width:32px;height:32px;color:var(--primary)}
@media (max-width:767px){.ui-how-head{grid-template-columns:1fr;gap:var(--space-3)}.ui-step{flex-direction:column;align-items:flex-start}}
/* doctor: large and prominent */
.ui-doctor{background:var(--surface-alt);border-radius:var(--radius-lg);padding:var(--space-4);gap:var(--space-6)}
@media (min-width:768px){.ui-doctor{grid-template-columns:6fr 6fr}}
.ui-doctor .ui-h1{font-size:44px}
:lang(zh) .ui-doctor .ui-h1{font-size:38px}
@media (max-width:767px){.ui-doctor{padding:var(--space-2);grid-template-columns:1fr}.ui-doctor .ui-h1{font-size:32px}:lang(zh) .ui-doctor .ui-h1{font-size:28px}}
.ui-n{font-size:15px;letter-spacing:.1em}
/* locations */
.d-locmedia .ui-map{aspect-ratio:16/8}
.d-locmedia--split{display:grid;grid-template-columns:3fr 2fr}
.d-locmedia--split .d-photo{border-radius:0;box-shadow:none}
.d-locmedia--split .ui-map{aspect-ratio:auto;border-left:1px solid var(--border)}
.ui-map{background:var(--surface-alt);color:var(--text-secondary)}
/* band */
.ui-band{--btn2-bg:transparent;--btn2-fg:#FFFFFF;--btn2-border:#FFFFFF;--wash:rgba(255,255,255,.12);--wash-strong:rgba(255,255,255,.2);--focus:#FFFFFF}
.ui-band .ui-muted{color:var(--secondary)}
.ui-footer :focus-visible{outline-color:#fff}
.d-photo-specs{display:grid;grid-template-columns:1fr 1.4fr 1.2fr;gap:24px;align-items:start}
.d-img-grid{display:grid;grid-template-columns:minmax(240px,340px) 1fr;gap:32px;align-items:start}
@media (max-width:767px){.d-photo-specs,.d-img-grid{grid-template-columns:1fr}}
"""

def cover():
    return """<!-- @dsCard height=300 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Concept D · Calm Clinical</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;height:100%}
  body{background:var(--background);color:var(--text-primary);font-family:var(--font-en-heading);overflow:hidden}
  .cover{position:relative;width:960px;height:300px;overflow:hidden}
  .art{position:absolute;top:0;left:480px;width:480px;height:300px}
  .teal{fill:var(--primary)} .tint{fill:var(--secondary)} .apricot{fill:var(--accent)} .warm{fill:var(--photo-ground)}
  .ring{fill:none;stroke:var(--primary);stroke-width:1.4}
  .words{position:absolute;left:48px;bottom:44px;max-width:440px}
  .name{margin:0;font-size:56px;line-height:.98;font-weight:700;letter-spacing:-.02em;color:var(--text-primary)}
  .tag{margin:14px 0 0 2px;font-size:14px;line-height:20px;color:var(--text-secondary)}
</style>
</head>
<body>
<div class="cover">
<svg class="art" viewBox="0 0 480 300" aria-hidden="true">
<!--
  blocks      primary (deep teal) 224×300 slab bleeding off top and bottom · photo-ground (warm neutral) 176×224 — the photo slot, 4:5 · secondary (teal tint) 112×112 · accent (apricot) 112×40 button — ~40% of the cover
  arrangement a flush modular grid on 16px steps: the photo slot overlapping the teal slab, the tint square and the one apricot button beside it
  pattern     a literal motif (the lens / the eye map): three concentric hairline rings in the stroke weight of the icons (1.4px), centred on the tint square
  scales      sides in space-2 multiples; corners radius-lg 10 on blocks, radius-md 6 on the button
-->
<rect class="teal" x="256" y="-10" width="224" height="320" rx="10"/>
<rect class="warm" x="176" y="40" width="176" height="220" rx="10"/>
<rect class="tint" x="48" y="40" width="112" height="112" rx="10"/>
<circle class="ring" cx="104" cy="96" r="18"/><circle class="ring" cx="104" cy="96" r="32"/><circle class="ring" cx="104" cy="96" r="46"/>
<rect class="apricot" x="48" y="220" width="112" height="40" rx="6"/>
</svg>
<div class="words">
<h1 class="name">Concept D ·<br>Calm Clinical</h1>
<p class="tag">Specialist-led and calm: white space, deep teal, large real photographs.</p>
</div>
</div>
</body>
</html>
"""
