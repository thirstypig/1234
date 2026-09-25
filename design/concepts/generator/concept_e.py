"""Concept E — Modern Practice. Leads with CONVENTION: the familiar, mature optometry-practice website, done with restraint."""
from base import PATHS, EN, ZH

KEY="E"; NAME="Modern Practice"; NAMESPACE="ModernPracticeE"
TITLE="Concept E · Modern Practice"
FONT_URL="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Source+Sans+3:wght@400;600;700&family=Noto+Serif+TC:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"
SECTION={"hero":"e-hero","problem":"e-stone","doctor":"e-stone","faq":"e-stone"}

def icon(name, cls="ui-ico"):
    return (f'<svg class="{cls} e-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{PATHS[name]}</svg>')
def ring(name): return f'<span class="e-ring">{icon(name)}</span>'

def photo(label, brief, ratio="4/5", cls=""):
    return f'<figure class="e-photo {cls}"><div class="ui-photo" style="aspect-ratio:{ratio}" role="img" aria-label="{label}">{icon("camera")}<span>{label}<small>{brief}</small></span></div></figure>'

def utility_extra(B,c):
    zh=c["lang"]=="zh"
    hrs="阿罕布拉：週二、週五 12–6 pm・週六 12–4 pm" if zh else "Alhambra: Tue & Fri 12–6 pm · Sat 12–4 pm"
    return f'<div class="e-info"><span>{icon("phone")}<span class="ui-nowrap">(800) 991-8881</span></span><span class="e-info-hrs">{icon("clock")}<span>{hrs}</span></span></div>'

def hero_bg(c):
    zh=c["lang"]=="zh"
    lab="全幅照片：胡醫師與小病人在明亮診間" if zh else "Full-width photo: Dr. Woo with a child patient in the bright exam room"
    return f'<div class="e-hero-photo" role="img" aria-label="{lab}"><span>{icon("camera")}{lab}</span></div><div class="e-hero-scrim" aria-hidden="true"></div>'
def hero_aside(B,c):
    zh=c["lang"]=="zh"
    items="".join(f'<li>{icon(i)}<span>{t}</span></li>' for i,t in c["trust"])
    return f'''<aside class="e-card" aria-label="{c['trust_title']}"><p class="e-kicker">{c["trust_title"]}</p><ul class="e-card-list">{items}</ul>
<a href="#" class="ui-btn ui-btn--primary ui-btn--block e-card-btn">{icon("calendar")}<span>{c["book"]}</span></a></aside>'''
def hero_trust(B,c): return ""
def hero_after(B,c): return ""
def step_marker(B,c,i,ic): return f'<div class="e-step-top"><span class="e-stepnum">{i}</span>{ring(ic)}</div>'
def how_art(B,c):
    return f'<p class="ui-lead e-how-sub">{c["prob_b"]}</p>' if False else ""
def doctor_photo(B,c):
    return photo(c["photo"],"編輯式人像・自然光" if c["lang"]=="zh" else "Editorial portrait · natural light","4/5","e-photo--doctor")
def loc_media(B,c,key,soon):
    lab = c["map_soon"] if soon else c["map"]
    return f'<div class="ui-map e-map" role="img" aria-label="{lab}">{icon("map")}<span>{lab}</span></div>'
def band_art(B,c): return ""

def extras(B):
    lab=B.lab
    info=f'<div class="ui-page"><div class="ui-spec">{lab("EN")}<div class="ui-utility" style="border:1px solid var(--border)"><div class="ui-utility-in" style="padding:0 16px">{utility_extra(B,EN)}{B.lang_switch("en")}</div></div><div style="height:16px"></div>{lab("繁體")}<div lang="zh-Hant" class="ui-utility" style="border:1px solid var(--border)"><div class="ui-utility-in" style="padding:0 16px">{utility_extra(B,ZH)}{B.lang_switch("zh-Hant")}</div></div></div></div>'
    card=f'<div class="ui-page"><div class="ui-spec e-cardspec"><div>{lab("EN")}{hero_aside(B,EN)}</div><div lang="zh-Hant">{lab("繁體")}{hero_aside(B,ZH)}</div></div></div>'
    return [("Info bar",260,info,"# Info bar\n\nThe conventional practice top bar: phone and Alhambra hours on the left, EN / 简体 / 繁體 on the right, on navy. On phones only the phone number and the language switcher stay (hours move to the location cards).",1200),
            ("Appointment card",620,card,"# Appointment card\n\nThe white card that sits over the hero photo: who you'll see (four facts) and a full-width Book button. The one place on the page with a shadow.",1000)]

ROLES=[("primary","Primary"),("secondary","Secondary"),("accent","Accent"),("background","Background"),("surface","Surface (cards)"),("text-primary","Text Primary"),("text-secondary","Text Secondary"),("border","Border"),("success","Success"),("error","Error")]
CONTRAST_FGS=[("text-primary","Text Primary"),("text-secondary","Text Secondary"),("primary","Navy (as text)"),("accent","Brass (as text)"),("success","Success"),("error","Error"),("on-primary","White (on navy)"),("accent-light","Pale brass (on navy)")]
CONTRAST_BGS=[("background","White"),("secondary","Stone"),("surface-alt","Light stone"),("primary","Navy"),("hero-ground","Hero scrim")]
DARK={"primary","hero-ground"}
CONTRAST_SKIP={(f,b) for f,_ in CONTRAST_FGS for b,_ in CONTRAST_BGS if (b in DARK)!=(f in ("on-primary","accent-light"))}
CONTRAST_NOTE="Light grounds take ink, slate, navy, brass, success and error (4.9:1+). Dark grounds (navy, the hero scrim) take white (14:1+) and pale brass (7.7:1+) only. Control edges use <code>border-strong</code> (3.1:1+). Focus ring = <code>primary</code> navy on light, pale brass on dark."
COLORS=[
("primary","#14233F","PRIMARY · Midnight navy. Primary buttons on light grounds, headings' accent, the info bar, booking band and footer. White on it 15.7:1."),
("primary-hover","#1D3257","Primary button hover. White 12.8:1."),
("primary-pressed","#0D182D","Primary button pressed. White 17.7:1."),
("on-primary","#FFFFFF","Text on navy and on the hero scrim."),
("secondary","#EFEBE4","SECONDARY · Warm stone. Alternate section grounds (problem, doctor, FAQ). Ink 13.9:1, slate 5.9:1."),
("accent","#7E5E2B","ACCENT · Brass. Small-caps kickers, thin rules, step numerals. As text 5:1+ on white and stone. Used sparingly."),
("accent-light","#D9B97E","Pale brass. The primary button on dark grounds (navy text 8.3:1) and kickers on navy (8.3:1)."),
("accent-light-hover","#E5CA96","Pale brass button hover."),
("background","#FFFFFF","BACKGROUND · White."),
("surface","#FFFFFF","SURFACE · Cards: steps, FAQ rows, locations, fields, the appointment card."),
("surface-alt","#F6F3EE","Light stone: location cards' media, hover wash."),
("wash","#F3EFE8","Hover wash for secondary controls."),
("wash-strong","#E8E2D8","Pressed wash; the open FAQ row."),
("text-primary","#1A1F29","TEXT PRIMARY · Ink. 13.9:1+ on white and stone."),
("text-secondary","#525A66","TEXT SECONDARY · Slate. 5.9:1+ on white and stone."),
("border","#E2DDD5","BORDER · Hairlines (decorative)."),
("border-strong","#858B94","Control edges (3.1:1+)."),
("hero-ground","#1E2A3E","The hero's darkened photo ground (photo + scrim). White 14.4:1, pale brass 7.7:1."),
("scrim","rgba(12, 20, 36, 0.62)","Dark overlay on the full-width hero photo so white text always reads, whatever the photo."),
("success","#2F6B4A","SUCCESS · With a check icon and words. 5.3:1+."),
("error","#A63A2C","ERROR · With an alert icon and a sentence. 5.4:1+."),
]
FAMILY_STACKS={"en-heading":"Newsreader, \"Iowan Old Style\", Georgia, serif","en-body":"\"Source Sans 3\", system-ui, -apple-system, \"Segoe UI\", sans-serif",
 "zh-heading":"\"Noto Serif TC\", \"Songti TC\", PMingLiU, serif","zh-body":"\"Noto Sans TC\", \"PingFang TC\", \"Microsoft JhengHei\", sans-serif"}
FAMILIES=[("English heading","en-heading","Newsreader 500",500,"Google Fonts · OFL · a modern text serif"),("English body","en-body","Source Sans 3",400,"Google Fonts · OFL · the workhorse sans"),("Chinese heading","zh-heading","思源宋體 Noto Serif TC",600,"Google Fonts · OFL · 明體, mature and formal"),("Chinese body","zh-body","思源黑體 Noto Sans TC",400,"≥17px · line height 1.8")]
TYPE=[("display",60,40,1.06,500,52,34,1.3,600,"Clear vision all day.","白天看得清楚，"),("h1",42,32,1.12,500,38,30,1.35,600,"Book a visit at either clinic","兩間診所，歡迎預約"),("h2",34,28,1.15,500,30,24,1.4,600,"How ortho-k works","角膜塑型怎麼進行"),("h3",22,20,1.3,600,21,20,1.5,600,"Custom lenses made for your child","為孩子量身訂製鏡片"),("body",18,17,1.65,400,18,17,1.8,400,"Your child wears special lenses while they sleep.","孩子晚上睡覺時戴上特製鏡片，早上取下就能看清楚。"),("small",15,14,1.5,400,15,15,1.7,400,"Tue & Fri 12–6 pm, Sat 12–4 pm","週二及週五 中午12點至下午6點"),("button",15,15,1.0,700,17,17,1.0,500,"BOOK A CONSULTATION","預約諮詢")]
RADIUS=[("radius-sm","2px","SMALL: chips, fields, buttons — nearly square."),("radius-md","2px","MEDIUM: FAQ rows and cards — same crisp corner."),("radius-lg","4px","LARGE: the appointment card and photos."),("radius-round","999px","Icon rings only.")]
SHADOWS=[("shadow-card","0 18px 48px rgba(12, 20, 36, 0.22)","Only the appointment card over the hero photo."),("shadow-float","0 12px 32px rgba(12, 20, 36, 0.16)","Mobile menu sheet and sticky bar.")]
SECTION_RHYTHM="Sections: 96px top and bottom on desktop (<code>space-12</code>), 64px on mobile. Sections alternate white and warm stone. A 48px brass rule sits above every section heading."
SHAPE_BORDERS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;border-radius:2px"><b>Hairline</b><p class="ui-small">1px <code>border</code> — cards, rows</p></div><div class="ui-fam" style="width:220px;border:1.5px solid var(--border-strong);border-radius:2px"><b>Control</b><p class="ui-small">1.5px <code>border-strong</code></p></div><div class="ui-fam" style="width:220px;border-radius:2px"><span style="display:block;width:48px;height:2px;background:var(--accent);margin-bottom:12px"></span><b>Brass rule</b><p class="ui-small">48 × 2px above section headings</p></div></div>'''
SHAPE_SHADOWS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;border-radius:2px"><b>No shadow</b><p class="ui-small">Everything, by default</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-card);border-radius:4px"><b>shadow-card</b><p class="ui-small">Appointment card only</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-float);border-radius:4px"><b>shadow-float</b><p class="ui-small">Menu sheet, sticky bar</p></div></div>'''
IMAGERY_H=680
def imagery(B):
    return f'''<div class="e-img-grid"><div>{photo("Full-width hero: Dr. Woo with a child","Wide 21:9 · subject on the right third · dark scrim on the left for text","21/9")}</div>
<div class="ui-stack-lg"><p class="ui-body">The classic practice site, done with restraint: one full-width hero photograph under a dark scrim, an editorial portrait of Dr. Woo, and quiet photos of the two clinics. Photos are composed with room for text on the left third; the scrim keeps white text at 14:1 whatever the photo.</p>
<div class="ui-dodont"><ul class="ok"><li>{icon("check")}<span>Real photos, natural light, neutral-warm grade, same look across all shots</span></li><li>{icon("check")}<span>Hero subject on the right third; calm, confident expressions</span></li><li>{icon("check")}<span>Clinic interiors straight-on, uncluttered</span></li></ul>
<ul class="no"><li>{icon("alert")}<span>Stock "happy family" photos, AI images, illustrations, emoji</span></li><li>{icon("alert")}<span>Text baked into photos; busy photos behind white text without the scrim</span></li><li>{icon("alert")}<span>Insurance-logo walls, review stars, awards badges</span></li></ul></div></div></div>'''
VOICE=dict(words=["Assured","Measured","Warm"],
  right_en="Every child's eyes are different. Dr. Woo will examine your child and explain whether ortho-k is a good fit.", right_zh="每個孩子的眼睛都不一樣。胡醫師會為孩子仔細檢查，並說明是否適合角膜塑型。", right_why="Professional and specific, with a warm promise of attention.",
  wrong_en="LA's #1 ortho-k center — trusted by thousands of families!", wrong_zh="洛杉磯第一的角膜塑型中心，數千家庭的信賴之選！", wrong_why="Unverifiable rankings and counts. Mature brands never shout.")
INTRO="**Leads with: convention.** The familiar, mature optometry-practice website that parents already trust — info bar, full-width hero photo, an appointment card, clean sections — made modern through restraint: midnight navy, warm stone, a touch of brass, a serif for headlines (明體 for Chinese), square corners and generous space. The most 'grown-up' of the five."
COLOR_RULES="""- Light grounds (white, stone, light stone): ink, slate, navy, brass, success and error all pass (4.9:1+).
- Dark grounds (navy info bar, booking band, footer, the hero scrim): white (14:1+) and pale brass (7.7:1+) only.
- The primary button is navy on light grounds and pale brass with navy text on dark grounds (8.3:1).
- Brass is used sparingly: kickers, the 48px section rule, step numerals. Never large fills."""
TYPE_RULES="""- Serif headlines, sans body — the classic editorial pairing. Newsreader 500 for English headlines; 思源宋體 Noto Serif TC 600 (明體) for Chinese headlines; Source Sans 3 and Noto Sans TC for body. This is the only concept with a serif.
- Buttons and kickers in English are small caps (uppercase, +0.08em tracking); Chinese stays as written, +0.1em tracking.
- Chinese body ≥17px, line height 1.8.
- **Simplified pages:** Noto Serif SC and Noto Sans SC — same families on Google Fonts."""
SHAPE_RULES="Nearly square corners (2px; 4px on the appointment card and photos). 1px hairlines, 1.5px control edges, a 48 × 2px brass rule above each section heading. No shadows except the appointment card and the mobile sheet/sticky bar."
IMAGERY_RULES="""One full-width hero photograph under a dark scrim, an editorial portrait of Dr. Woo, quiet clinic photos. Compose with room for text on the left third; the scrim keeps white text at 14:1.

- Do: real photos, natural light, one consistent neutral-warm grade · hero subject on the right third · clinic interiors straight-on.
- Don't: stock "happy family" photos · AI images, illustrations, emoji · text on photos · insurance-logo walls, review stars, award badges."""
README_COLOR="# Color\n\nMidnight navy, warm stone and white, with a touch of brass."
README_TYPE="# Typography\n\nA serif for headlines (Newsreader / 思源宋體), a clean sans for reading (Source Sans 3 / 思源黑體)."
README_SPACING="# Spacing & Layout\n\nConventional practice-site layout on a 12-column grid, generous 96px sections."
README_SHAPE="# Shape\n\nSquare corners, hairlines, brass rules; almost no shadow."
README_ICONS="# Icons\n\nOutline icons at 1.5px stroke, set inside thin brass rings (the classic practice-site treatment) for steps and trust facts; bare in chips and rows. Navy on light, pale brass on dark. Never emoji."
README_IMAGERY="# Imagery\n\nFull-width hero photograph, editorial portrait, quiet clinic photos."
README_VOICE="# Voice & Tone\n\nAssured, measured, warm — the voice of an established practice."
README_COMP={
 "Primary button":"# Primary button\n\nNavy, square, small-caps label on light grounds; pale brass with navy text on dark grounds. Booking only.",
 "Secondary button":"# Secondary button\n\nNavy 1.5px outline, square, small caps. On dark grounds, a white outline.",
 "Language switcher":"# Language switcher\n\nEN / 简体 / 繁體 on the navy info bar (white, current underlined in pale brass) and in the footer.",
 "Top navigation + mobile menu":"# Top navigation + mobile menu\n\nNavy info bar (phone, hours, languages) above a white header: the name set in Newsreader (no logo), five links, a navy Book button. Mobile: Menu opens a white sheet.",
 "Hero block":"# Hero block\n\nFull-width photo under a dark scrim; serif headline in white with the second line in pale brass; pale-brass Book + white-outline Message; the white appointment card on the right lists who you'll see.",
 "3-step How it works block":"# 3-step How it works block\n\nThree open columns separated by hairlines: a large brass serif numeral, an icon in a thin ring, the step as H3.",
 "Doctor card":"# Doctor card\n\nOn warm stone: an editorial 4:5 portrait on the left, kicker, name in serif, the provided lines, languages, Book.",
 "FAQ accordion":"# FAQ accordion\n\nOn stone: square white rows separated by hairlines, serif questions, a thin +/−.",
 "Booking call-to-action band":"# Booking call-to-action band\n\nFull navy band, serif heading in white, pale-brass Book + white-outline Message.",
 "Location card":"# Location card\n\nSquare card: map placeholder, name, address, hours, phones, Book here + Directions. Walnut shows coming soon and a dashed disabled button.",
 "Contact row":"# Contact row\n\nSquare outlined chips with outline icons: Call, Book online, WeChat, LINE, WhatsApp (dashed placeholders for the official marks).",
 "Form field set":"# Form field set\n\nSquare 52px fields, labels above, navy focus ring, errors with an alert icon and a sentence.",
 "Footer":"# Footer\n\nMidnight-navy, four columns: practice name, both clinics, contact, languages; legal links under a hairline.",
}
CSS=r"""
/* ===== SKIN · Concept E · Modern Practice ===== */
:root{--w-head:500;--w-label:700;--w-zh-head:600;--w-zh-label:500;
 --radius-btn:var(--radius-sm);--radius-input:var(--radius-sm);--focus:var(--primary);
 --btn-bg:var(--primary);--btn-fg:var(--on-primary);--btn-bg-hover:var(--primary-hover);--btn-bg-pressed:var(--primary-pressed);
 --btn2-bg:transparent;--btn2-fg:var(--primary);--btn2-border:var(--primary);
 --lang-mark:var(--accent-light);--utility-bg:var(--primary);--header-bg:var(--background);--brand-ink:var(--primary);
 --icon:var(--primary);--numeral:var(--accent);--photo-bg:#D9D3CA;--photo-fg:#3F3A33;
 --band-bg:var(--primary);--band-fg:var(--on-primary);
 --footer-bg:#0D182D;--footer-fg:#FFFFFF;--footer-muted:#C3CAD6;--footer-rule:#2A3A57}
.ui-display,.ui-h1,.ui-h2{letter-spacing:-.01em}
:lang(zh) :is(.ui-display,.ui-h1,.ui-h2,.ui-h3){letter-spacing:.04em}
.ui-display{font-size:60px}.ui-h1{font-size:42px}.ui-h2{font-size:34px}
.ui-h3{font-family:var(--font-en-body);font-weight:600}
:lang(zh) .ui-h3{font-family:var(--font-zh-body);font-weight:500}
@media (max-width:767px){.ui-display{font-size:40px}.ui-h1{font-size:32px}.ui-h2{font-size:28px}}
.ui-btn{text-transform:uppercase;letter-spacing:.08em;font-family:var(--font-en-body);font-size:15px}
:lang(zh) .ui-btn{text-transform:none;letter-spacing:.1em;font-family:var(--font-zh-body);font-size:17px}
.ui-eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:13px;color:var(--accent);font-family:var(--font-en-body)}
:lang(zh) .ui-eyebrow{text-transform:none;letter-spacing:.14em;font-size:15px;font-family:var(--font-zh-body)}
.ui-eyebrow .ui-ico{display:none}
.ui-section{padding:var(--space-12) 0}
@media (max-width:767px){.ui-section{padding:var(--space-8) 0}}
.ui-section :is(.ui-h1,.ui-h2):not(.ui-doctor .ui-h1)::before{content:"";display:block;width:48px;height:2px;background:var(--accent);margin-bottom:20px}
.e-stone{background:var(--secondary)}
/* info bar */
.ui-utility{color:#fff;border-bottom:0}
.ui-utility .ui-lang a{color:#D5DBE5}
.ui-utility .ui-lang a[aria-current="page"],.ui-utility .ui-lang a:hover{color:#fff;background:rgba(255,255,255,.08)}
.ui-utility .ui-lang-sep{color:#5B6A85}
.ui-utility :focus-visible{outline-color:var(--accent-light)}
.e-info{display:flex;gap:24px;align-items:center;margin-right:auto;font-size:14px;color:#E6EAF0}
.e-info>span{display:inline-flex;align-items:center;gap:8px}
.e-info .ui-ico{color:var(--accent-light)}
@media (max-width:767px){.e-info>.e-info-hrs{display:none}.e-info{font-size:13px}}
.ui-utility-in{justify-content:flex-end}
@media (max-width:1023px){.ui-utility-in{justify-content:space-between}}
.ui-brand{font-size:24px;font-weight:600}
@media (max-width:1023px){.ui-brand{font-size:19px}}
@media (max-width:767px){.ui-stickybar .ui-btn{letter-spacing:.02em;font-size:13px}:lang(zh) .ui-stickybar .ui-btn{font-size:15px;letter-spacing:.04em}.ui-header .ui-menu-btn{padding:0 12px}}
.ui-nav a{font-family:var(--font-en-body);font-weight:600;font-size:15px}
/* hero: full-width photo + scrim */
.e-hero{background:var(--hero-ground);color:#fff;padding:var(--space-12) 0!important;min-height:600px;display:flex;align-items:center;
 --btn-bg:var(--accent-light);--btn-fg:var(--primary);--btn-bg-hover:var(--accent-light-hover);--btn-bg-pressed:#CCA965;--btn2-fg:#fff;--btn2-border:#fff;--wash:rgba(255,255,255,.1);--wash-strong:rgba(255,255,255,.18);--focus:var(--accent-light)}
.e-hero>.ui-wrap{width:100%}
.e-hero-photo{position:absolute;inset:0;background:#46536A;display:flex;align-items:flex-end;justify-content:flex-end;padding:20px 28px;color:rgba(255,255,255,.75);font-size:13px}
.e-hero-photo span{display:inline-flex;gap:8px;align-items:center;max-width:320px;text-align:right}
.e-hero-scrim{position:absolute;inset:0;background:linear-gradient(90deg,var(--scrim) 0%,var(--scrim) 45%,rgba(12,20,36,.35) 100%)}
.e-hero .ui-display{color:#fff}.e-hero .ui-lead{color:#EEF1F5}.e-hero .ui-eyebrow{color:var(--accent-light)}
.e-hero .ui-mark{color:var(--accent-light);background:none}
.e-hero .ui-hero-grid{grid-template-columns:7fr 4fr;align-items:center}
@media (max-width:1023px){.e-hero .ui-hero-grid{grid-template-columns:1fr}.e-hero{min-height:0}}
.e-card{background:#fff;color:var(--text-primary);border-radius:var(--radius-lg);box-shadow:var(--shadow-card);padding:28px;border-top:3px solid var(--accent);
 --btn-bg:var(--primary);--btn-fg:#fff;--btn-bg-hover:var(--primary-hover);--btn-bg-pressed:var(--primary-pressed);--focus:var(--primary)}
.e-kicker{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}
:lang(zh) .e-kicker{text-transform:none;font-size:15px;font-weight:500}
.e-card-list{list-style:none;padding:0;margin:0 0 20px}
.e-card-list li{display:grid;grid-template-columns:28px 1fr;gap:10px;padding:11px 0;border-bottom:1px solid var(--border);font-size:16px;line-height:1.45}
:lang(zh) .e-card-list li{font-size:17px;line-height:1.6}
.e-card-list .ui-ico{width:22px;height:22px;color:var(--primary);margin-top:1px}
.e-cardspec{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px;background:var(--hero-ground)}
.e-cardspec .ui-spec-label{color:#C3CAD6}
/* problem as a pull statement */
.e-stone .ui-grid{align-items:end}
/* how: open columns with hairlines */
.ui-how-head{margin-bottom:var(--space-6)}
.ui-steps{gap:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.ui-step{background:transparent;border:0;border-radius:0;padding:var(--space-4) var(--space-4) var(--space-4) 0;border-right:1px solid var(--border)}
.ui-step+.ui-step{padding-left:var(--space-4)}
.ui-step:last-child{border-right:0}
.e-step-top{display:flex;align-items:center;justify-content:space-between;width:100%}
.e-stepnum{font-family:var(--font-en-heading);font-size:56px;line-height:1;color:var(--accent)}
.e-ring{display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;border:1px solid var(--accent);border-radius:var(--radius-round);color:var(--primary)}
.e-ring .ui-ico{width:24px;height:24px}
.ui-step.is-current{background:var(--surface-alt)}
@media (max-width:767px){.ui-steps{border-bottom:0}.ui-step,.ui-step+.ui-step{border-right:0;border-bottom:1px solid var(--border);padding:var(--space-3) 0;flex-direction:column;align-items:flex-start}.e-stepnum{font-size:44px}}
/* doctor */
.e-photo{margin:0;border-radius:var(--radius-lg);overflow:hidden}
.e-photo .ui-photo{border-radius:0}
.ui-doctor .ui-h1{font-size:48px}
:lang(zh) .ui-doctor .ui-h1{font-size:38px}
@media (max-width:767px){.ui-doctor .ui-h1{font-size:34px}:lang(zh) .ui-doctor .ui-h1{font-size:28px}}
.ui-chip{border-radius:var(--radius-sm);background:transparent}
/* first visit */
.ui-n{font-family:var(--font-en-heading);font-size:30px;color:var(--accent)}
/* faq */
.ui-faq{gap:0;border-top:1px solid var(--border)}
.ui-faq details{border:0;border-bottom:1px solid var(--border);border-radius:0;background:transparent}
.ui-faq summary{border-radius:0;font-family:var(--font-en-heading);font-weight:500;font-size:22px;padding-left:0}
:lang(zh) .ui-faq summary{font-family:var(--font-zh-heading);font-weight:600;font-size:20px}
.ui-faq details[open] summary{border-bottom:0;border-radius:0}
.ui-faq summary .ui-ico{display:none}
.ui-faq summary{grid-template-columns:1fr 28px}
.ui-answer{padding:0 0 var(--space-3) 0}
.ui-faq summary:hover,.ui-faq summary.is-hover{background:transparent;color:var(--primary);text-decoration:underline;text-underline-offset:4px}
.ui-faq summary:active,.ui-faq summary.is-pressed{background:var(--wash-strong)}
/* locations */
.ui-loc,.ui-contact a,.ui-input,.ui-radio{border-radius:var(--radius-sm)}
.e-map{background:var(--surface-alt)}
/* band */
.ui-band{border-radius:0;padding:var(--space-8) var(--space-6);--btn-bg:var(--accent-light);--btn-fg:var(--primary);--btn-bg-hover:var(--accent-light-hover);--btn-bg-pressed:#CCA965;--btn2-fg:#fff;--btn2-border:#fff;--wash:rgba(255,255,255,.1);--wash-strong:rgba(255,255,255,.18);--focus:var(--accent-light)}
.ui-band .ui-h2::before{content:"";display:block;width:48px;height:2px;background:var(--accent-light);margin-bottom:20px}
.ui-band .ui-muted{color:#D5DBE5}
.ui-footer .ui-brand{color:#fff;font-family:var(--font-en-heading)}
.ui-footer :focus-visible{outline-color:var(--accent-light)}
.e-img-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:start}
@media (max-width:767px){.e-img-grid{grid-template-columns:1fr}}
"""

def cover():
    return """<!-- @dsCard height=300 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Concept E · Modern Practice</title>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;height:100%}
  body{background:var(--background);color:var(--text-primary);font-family:var(--font-en-heading);overflow:hidden}
  .cover{position:relative;width:960px;height:300px;overflow:hidden}
  .art{position:absolute;top:0;left:480px;width:480px;height:300px}
  .navy{fill:var(--primary)} .stone{fill:var(--secondary)} .brass{fill:var(--accent)} .pale{fill:var(--accent-light)}
  .rule{stroke:var(--accent-light);stroke-width:1}
  .words{position:absolute;left:48px;bottom:44px;max-width:440px}
  .name{margin:0;font-size:52px;line-height:1;font-weight:500;letter-spacing:-.01em;color:var(--primary)}
  .tag{margin:14px 0 0 2px;font-size:14px;line-height:20px;color:var(--text-secondary);font-family:var(--font-en-body)}
</style>
</head>
<body>
<div class="cover">
<svg class="art" viewBox="0 0 480 300" aria-hidden="true">
<!--
  blocks      primary (midnight navy) 336×300 slab bleeding off top, right and bottom · secondary (stone) 144×200 · accent (brass) 48×2 section rule ×1 and a 96×48 pale-brass button — ~45% of the cover
  arrangement one tall navy slab with a stone panel overlapping its left edge, like the appointment card over the hero photo
  pattern     editorial hairlines: four 1px pale-brass rules on the navy slab at a space-6 (48px) baseline pitch — "borders, not shadows"
  scales      sides in space-2 multiples; corners radius-sm 2 / radius-lg 4; rule = the 48 × 2 section rule
-->
<rect class="navy" x="144" y="-10" width="346" height="320" rx="0"/>
<path class="rule" d="M240 96H464M240 144H464M240 192H464M240 240H464"/>
<rect class="stone" x="48" y="64" width="160" height="192" rx="4"/>
<rect class="brass" x="72" y="96" width="48" height="2"/>
<rect class="pale" x="72" y="200" width="112" height="32" rx="2"/>
</svg>
<div class="words">
<h1 class="name">Concept E ·<br>Modern Practice</h1>
<p class="tag">The familiar practice website, done with restraint: navy, stone, a touch of brass.</p>
</div>
</div>
</body>
</html>
"""
