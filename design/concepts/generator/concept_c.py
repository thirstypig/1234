"""Concept C — Picture-Book. Leads with ILLUSTRATION. The scroll tells a story: night → morning → school."""
from base import PATHS, EN, ZH

KEY="C"; NAME="Picture-Book"; NAMESPACE="PictureBookC"
TITLE="Concept C · Picture-Book"
FONT_URL="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Chiron+GoRound+TC:wght@400;500;700&display=swap"
SECTION={"hero":"c-night","how":"c-dawn","doctor":"c-paper","visit":"c-paper","faq":"c-paper","locations":"c-paper","problem":"c-paper","band":"c-paper"}

def icon(name, cls="ui-ico"):
    return (f'<svg class="{cls} c-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{PATHS[name]}</svg>')

# ---------------- illustrations (original; 3px ink line, flat pastel fills) ----------------
INK="#16264A"; NIGHT="#1F3563"; NIGHT2="#2A4478"; SKY="#CFE6F5"; PEACH="#FBD3BC"; BUTTER="#FCEBA8"; CREAM="#FFF8EE"; SKIN="#F5D3BC"; HAIR="#3A3350"; CHEEK="#F4A98E"
S=f'stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
def star(x,y,r=7,fill=BUTTER):
    return f'<path d="M{x} {y-r}Q{x+r*.18} {y-r*.18} {x+r} {y}Q{x+r*.18} {y+r*.18} {x} {y+r}Q{x-r*.18} {y+r*.18} {x-r} {y}Q{x-r*.18} {y-r*.18} {x} {y-r}Z" fill="{fill}"/>'

def scene_night(label):
    return f'''<svg class="c-scene" viewBox="0 0 480 360" role="img" aria-label="{label}">
<rect x="0" y="0" width="480" height="360" rx="40" fill="{NIGHT2}"/>
<rect x="286" y="36" width="156" height="128" rx="22" fill="{NIGHT}" {S}/>
<path d="M364 36v128M286 100h156" {S} fill="none" opacity=".55"/>
<path d="M410 58a26 26 0 1 0 18 40 20 20 0 1 1-18-40z" fill="{BUTTER}"/>
{star(318,66,6)}{star(338,134,5)}{star(392,138,4)}{star(80,52,6)}{star(150,34,4)}{star(214,72,5)}
<rect x="30" y="170" width="46" height="138" rx="20" fill="{SKY}" {S}/>
<rect x="44" y="236" width="300" height="72" rx="26" fill="{PEACH}" {S}/>
<path d="M58 308v22M330 308v22" {S}/>
<ellipse cx="116" cy="226" rx="46" ry="20" fill="{CREAM}" {S}/>
<circle cx="122" cy="206" r="27" fill="{SKIN}" {S}/>
<path d="M96 200c2-18 18-28 34-24 12 3 20 12 19 22-9-8-24-9-36-3-6 3-12 5-17 5z" fill="{HAIR}"/>
<path d="M112 210q5 4 10 0M130 210q5 4 10 0" {S} fill="none" stroke-width="2.6"/>
<circle cx="112" cy="219" r="4.5" fill="{CHEEK}"/><circle cx="142" cy="219" r="4.5" fill="{CHEEK}"/>
<path d="M146 214c30-10 70-12 110-8 40 4 76 14 86 28 4 6 2 14-6 16H150c-10 0-16-10-14-20 1-6 5-12 10-16z" fill="{SKY}" {S}/>
<circle cx="200" cy="232" r="4" fill="{CREAM}"/><circle cx="246" cy="226" r="4" fill="{CREAM}"/><circle cx="290" cy="236" r="4" fill="{CREAM}"/><circle cx="226" cy="246" r="3" fill="{CREAM}"/><circle cx="270" cy="250" r="3" fill="{CREAM}"/>
<rect x="362" y="238" width="86" height="80" rx="14" fill="{BUTTER}" {S}/>
<path d="M376 276h58" {S}/><circle cx="405" cy="296" r="4" fill="{INK}"/>
<rect x="380" y="214" width="50" height="24" rx="12" fill="{CREAM}" {S}/>
<circle cx="396" cy="226" r="6" fill="{SKY}" stroke="{INK}" stroke-width="2"/><circle cx="414" cy="226" r="6" fill="{SKY}" stroke="{INK}" stroke-width="2"/>
<path d="M170 160c6-3 12-3 16 0M190 140c6-3 12-3 16 0M214 120c6-3 12-3 16 0" stroke="{CREAM}" stroke-width="3" stroke-linecap="round" fill="none" opacity=".8"/>
</svg>'''

def scene_morning(label):
    return f'''<svg class="c-scene" viewBox="0 0 480 360" role="img" aria-label="{label}">
<rect x="0" y="0" width="480" height="360" rx="40" fill="#E4F1FA"/>
<rect x="286" y="36" width="156" height="128" rx="22" fill="{SKY}" {S}/>
<circle cx="404" cy="84" r="22" fill="{BUTTER}" stroke="{INK}" stroke-width="2.5"/>
<path d="M404 50v-8M404 126v-8M370 84h-8M446 84h-8M380 60l-6-6M428 108l6 6M380 108l-6 6M428 60l6-6" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>
<path d="M290 140c24-8 48-10 70-2" stroke="{INK}" stroke-width="3" stroke-linecap="round" fill="none"/>
<ellipse cx="326" cy="126" rx="13" ry="10" fill="{PEACH}" {S}/><circle cx="334" cy="116" r="7" fill="{PEACH}" {S}/><path d="M340 116l7 2-7 3" fill="{BUTTER}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/><circle cx="335" cy="115" r="1.6" fill="{INK}"/>
<path d="M364 36v128M286 100h156" {S} fill="none" opacity=".35"/>
<rect x="30" y="170" width="46" height="138" rx="20" fill="{SKY}" {S}/>
<rect x="44" y="236" width="300" height="72" rx="26" fill="{PEACH}" {S}/>
<path d="M58 308v22M330 308v22" {S}/>
<path d="M150 240c40-10 110-12 170-2 14 2 22 10 20 18l-2 8H146c-8 0-12-10-8-16 3-4 7-7 12-8z" fill="{SKY}" {S}/>
<path d="M112 244v-54c0-14 10-24 24-24h14c14 0 24 10 24 24v54z" fill="{BUTTER}" {S}/>
<path d="M116 186c-10-14-16-30-14-48M170 186c10-14 16-30 14-48" {S} fill="none"/>
<circle cx="100" cy="134" r="8" fill="{SKIN}" {S}/><circle cx="186" cy="134" r="8" fill="{SKIN}" {S}/>
<circle cx="143" cy="140" r="28" fill="{SKIN}" {S}/>
<path d="M116 134c2-18 18-28 34-24 12 3 20 12 19 22-9-8-24-9-36-3-6 3-12 5-17 5z" fill="{HAIR}"/>
<circle cx="133" cy="143" r="3.4" fill="{INK}"/><circle cx="153" cy="143" r="3.4" fill="{INK}"/>
<path d="M134 155q9 7 18 0" {S} fill="none" stroke-width="2.6"/>
<circle cx="126" cy="153" r="4.5" fill="{CHEEK}"/><circle cx="161" cy="153" r="4.5" fill="{CHEEK}"/>
{star(200,120,8)}{star(214,150,5)}{star(86,104,6)}
<rect x="362" y="238" width="86" height="80" rx="14" fill="{BUTTER}" {S}/>
<path d="M376 276h58" {S}/><circle cx="405" cy="296" r="4" fill="{INK}"/>
<rect x="374" y="214" width="62" height="24" rx="12" fill="{CREAM}" {S}/>
<path d="M378 214c4-14 22-18 30-10" {S} fill="none"/>
<circle cx="394" cy="226" r="6" fill="{SKY}" stroke="{INK}" stroke-width="2"/><circle cx="414" cy="226" r="6" fill="{SKY}" stroke="{INK}" stroke-width="2"/>
</svg>'''

def scene_school(label):
    return f'''<svg class="c-scene" viewBox="0 0 480 360" role="img" aria-label="{label}">
<rect x="0" y="0" width="480" height="360" rx="40" fill="{BUTTER}"/>
<path d="M60 70c0-12 12-20 24-16 4-12 22-16 30-4 12-2 20 8 16 18H64c-3 0-4-1-4 2z" fill="{CREAM}" {S}/>
<path d="M330 56c0-10 10-16 20-13 4-10 18-12 24-3 10-2 17 6 14 14H334c-3 0-4 0-4 2z" fill="{CREAM}" {S}/>
<rect x="250" y="130" width="190" height="150" rx="16" fill="{SKY}" {S}/>
<path d="M238 136l107-58 107 58z" fill="{PEACH}" {S}/>
<path d="M345 78V36" {S}/><path d="M345 38h34l-8 10 8 10h-34z" fill="{PEACH}" {S}/>
<rect x="320" y="206" width="50" height="74" rx="12" fill="{CREAM}" {S}/>
<rect x="270" y="160" width="36" height="30" rx="8" fill="{CREAM}" {S}/><rect x="384" y="160" width="36" height="30" rx="8" fill="{CREAM}" {S}/>
<circle cx="345" cy="112" r="12" fill="{CREAM}" {S}/><path d="M345 105v7l5 3" stroke="{INK}" stroke-width="2" stroke-linecap="round" fill="none"/>
<path d="M0 290c80-14 170-18 250-10 80 8 160 6 230-4v44c0 22-18 40-40 40H40c-22 0-40-18-40-40z" fill="{PEACH}"/>
<path d="M20 292c90-12 180-14 250-6 70 8 140 6 200-2" {S} fill="none"/>
<rect x="100" y="176" width="46" height="62" rx="14" fill="{PEACH}" {S}/>
<path d="M126 196h58c10 0 16 6 16 16v18c0 8-6 14-14 14h-56z" fill="{SKY}" {S}/>
<rect x="132" y="186" width="56" height="68" rx="22" fill="{SKY}" {S}/>
<path d="M146 254l-14 38M172 254l12 38" {S}/>
<path d="M124 292h14M178 292h14" {S}/>
<path d="M186 204c14-8 22-22 24-36" {S} fill="none"/><circle cx="212" cy="164" r="8" fill="{SKIN}" {S}/>
<circle cx="164" cy="152" r="28" fill="{SKIN}" {S}/>
<path d="M137 146c2-18 18-28 34-24 12 3 20 12 19 22-9-8-24-9-36-3-6 3-12 5-17 5z" fill="{HAIR}"/>
<circle cx="164" cy="156" r="3.4" fill="{INK}"/><circle cx="182" cy="156" r="3.4" fill="{INK}"/>
<path d="M165 168q8 6 16 0" {S} fill="none" stroke-width="2.6"/>
<circle cx="157" cy="165" r="4.5" fill="{CHEEK}"/><circle cx="189" cy="165" r="4.5" fill="{CHEEK}"/>
{star(222,122,7,CREAM)}{star(60,150,6,CREAM)}
</svg>'''

def labels(c):
    zh=c["lang"]=="zh"
    return (("插畫：孩子戴著鏡片安心睡覺，鏡片盒放在床頭櫃上。" if zh else "Illustration: a child asleep; the lens case waits on the nightstand."),
            ("插畫：早上醒來，孩子看得清清楚楚。" if zh else "Illustration: morning — the child wakes up and sees clearly."),
            ("插畫：孩子不用戴眼鏡，開心上學去。" if zh else "Illustration: off to school, no glasses."))

def hero_aside(B,c): return f'<div class="c-hero-art">{scene_night(labels(c)[0])}<p class="c-story-cap">{icon("moon")}<span>{"晚上" if c["lang"]=="zh" else "Night"}</span></p></div>'
def hero_trust(B,c):
    return f'<p class="c-trust-chip">{icon("eye")}<span>{c["trust"][0][1]} · {c["trust"][1][1]}</span></p>'
def hero_after(B,c): return '<div class="c-hills" aria-hidden="true"></div>'
def step_marker(B,c,i,ic): return f'<span class="c-stepnum" aria-hidden="true">{i}</span><span class="c-stepico">{icon(ic)}</span>'
def how_art(B,c): return f'<div class="c-how-art">{scene_morning(labels(c)[1])}<p class="c-story-cap">{icon("sun")}<span>{"早上" if c["lang"]=="zh" else "Morning"}</span></p></div>'
def doctor_photo(B,c):
    return f'''<figure class="c-frame"><div class="ui-photo" role="img" aria-label="{c['photo']}">{icon("camera")}<span>{c["photo"]}<small>{"真實照片・自然光" if c["lang"]=="zh" else "Real photo, natural light"}</small></span></div>
<svg class="c-frame-doodle c-frame-doodle--tl" viewBox="0 0 60 60" aria-hidden="true"><path d="M40 8a20 20 0 1 0 14 30 15 15 0 1 1-14-30z" fill="{BUTTER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></svg>
<svg class="c-frame-doodle c-frame-doodle--br" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="12" fill="{BUTTER}" stroke="{INK}" stroke-width="3"/><path d="M30 6v6M30 48v6M6 30h6M48 30h6M13 13l4 4M43 43l4 4M13 47l4-4M43 17l4-4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></svg>
<svg class="c-frame-doodle c-frame-doodle--tr" viewBox="0 0 40 40" aria-hidden="true">{star(20,20,14,PEACH)}</svg></figure>'''
def loc_media(B,c,key,soon):
    lab = c["map_soon"] if soon else c["map"]
    return f'<div class="ui-map c-map" role="img" aria-label="{lab}">{icon("map")}<span>{lab}</span></div>'
def band_art(B,c): return f'<div class="c-band-art">{scene_school(labels(c)[2])}</div>'

def extras(B):
    lab=B.lab
    scenes=f'''<div class="ui-spec"><div class="c-scenes">
<figure>{lab("1 · Night — hero")}{scene_night("Night")}<figcaption class="ui-small">Asleep with lenses in; the lens case on the nightstand; moon and stars.</figcaption></figure>
<figure>{lab("2 · Morning — How it works")}{scene_morning("Morning")}<figcaption class="ui-small">Awake, lenses out, seeing clearly: open eyes, a bird at the window.</figcaption></figure>
<figure>{lab("3 · School — booking band")}{scene_school("School")}<figcaption class="ui-small">Off to school, no glasses, backpack on.</figcaption></figure></div></div>'''
    frame=f'<div class="ui-spec"><div style="max-width:360px">{doctor_photo(B,EN)}</div></div>'
    return [("Story scenes",560,f'<div class="ui-page">{scenes}</div>',"# Story scenes\n\nThree original spot illustrations that carry the scroll from night to morning to school: hero (night band), How it works (dawn band), booking band (day). Always in this order, one per band, never repeated on a page.",1200),
            ("Illustrated photo frame",560,f'<div class="ui-page">{frame}</div>',"# Illustrated photo frame\n\nA real photo (Dr. Woo, the clinics) inside a soft sky-blue frame with three hand-drawn doodles — moon, sun, star — tucked on its corners. The photo itself is never drawn over.",700)]

ROLES=[("primary","Primary"),("secondary","Secondary"),("accent","Accent"),("background","Background"),("surface","Surface (cards)"),("text-primary","Text Primary"),("text-secondary","Text Secondary"),("border","Border"),("success","Success"),("error","Error")]
CONTRAST_FGS=[("text-primary","Text Primary"),("text-secondary","Text Secondary"),("primary","Night blue (as text)"),("success","Success"),("error","Error"),("on-primary","On-primary (white)"),("on-night","Cream (on night)")]
CONTRAST_BGS=[("background","Cream"),("surface","White"),("secondary","Sky"),("accent","Peach"),("butter","Butter"),("primary","Night blue")]
CONTRAST_SKIP={(f,"primary") for f,_ in CONTRAST_FGS if f not in ("on-primary","on-night")}|{(f,b) for f in ("on-primary","on-night") for b in ("background","surface","secondary","accent","butter")}
CONTRAST_NOTE="Every text color passes on every pastel. Pastels are grounds, never text colors. On the night band text is cream (11.4:1) or <code>on-night-muted</code> (8.1:1) and the primary button turns butter with night-blue text (10:1). Control edges use <code>border-strong</code> (3.3:1+). Focus ring = <code>primary</code>, 11:1 on cream; cream on the night band."

COLORS=[
("primary","#1F3563","PRIMARY · Night blue. Primary button fill, headings' deep accent, icons, the night band. White on it 12:1. As text on every pastel (8.7:1+)."),
("primary-hover","#2B4680","Primary button hover (lifts lighter, like dawn). White 9.2:1."),
("primary-pressed","#172850","Primary button pressed. White 14:1."),
("on-primary","#FFFFFF","Text on `primary`."),
("secondary","#CFE6F5","SECONDARY · Sky blue. The dawn band, secondary fills, the photo frame, step discs. A ground only."),
("accent","#FBD3BC","ACCENT · Peach. Step-number discs, blankets and warm details in illustrations, the hills under the hero. A ground only."),
("butter","#FCEBA8","Soft yellow. Moon, sun, the day band, and the primary button on the night band. A ground only."),
("background","#FFF8EE","BACKGROUND · Cream paper with a light paper texture."),
("surface","#FFFFFF","SURFACE · Cards: steps, FAQ, locations, fields."),
("wash","#F6EDDF","Hover wash for secondary controls."),
("wash-strong","#EFE2CD","Pressed wash; the open FAQ row."),
("text-primary","#22304A","TEXT PRIMARY · Ink blue. Headlines and body on cream, white and every pastel (9.5:1+)."),
("text-secondary","#4F5B72","TEXT SECONDARY. Captions, hours, hints on cream, white and every pastel (4.9:1+)."),
("border","#EADCC8","BORDER · Soft card edges (decorative)."),
("border-strong","#8A8797","Control edges: fields and chips (3.3:1+)."),
("on-night","#FFF8EE","Headlines and body on the night band (11.4:1)."),
("on-night-muted","#C9D5EC","Secondary text on the night band (8.1:1)."),
("success","#2D6A4F","SUCCESS · With a check icon and words. 4.6:1+ on every ground."),
("error","#B03A2E","ERROR · With an alert icon and a sentence. 5.7:1 on cream, 6:1 on white."),
]
FAMILY_STACKS={"en-heading":"Quicksand, \"Varela Round\", ui-rounded, system-ui, sans-serif","en-body":"Quicksand, \"Varela Round\", ui-rounded, system-ui, sans-serif",
 "zh-heading":"\"Chiron GoRound TC\", \"jf-openhuninn\", \"PingFang TC\", \"Noto Sans TC\", sans-serif","zh-body":"\"Chiron GoRound TC\", \"PingFang TC\", \"Noto Sans TC\", sans-serif"}
FAMILIES=[("English heading","en-heading","Quicksand 700",700,"Google Fonts · OFL · soft, rounded"),("English body","en-body","Quicksand 500",500,"Google Fonts · OFL · 500 for body, never 300"),("Chinese heading","zh-heading","昭源圓體 700",700,"Chiron GoRound TC · OFL · 圓體"),("Chinese body","zh-body","昭源圓體 400",400,"Chiron GoRound TC · ≥17px, line height 1.85")]
TYPE=[("display",54,38,1.12,700,50,34,1.35,700,"Clear vision all day.","白天看得清楚，"),("h1",40,32,1.18,700,38,30,1.4,700,"Book a visit at either clinic","兩間診所，歡迎預約"),("h2",30,26,1.25,700,30,24,1.45,700,"How ortho-k works","角膜塑型怎麼進行"),("h3",22,20,1.35,700,22,20,1.55,700,"Custom lenses made for your child","為孩子量身訂製鏡片"),("body",18,17,1.7,500,18,17,1.85,400,"Your child wears special lenses while they sleep.","孩子晚上睡覺時戴上特製鏡片，早上取下就能看清楚。"),("small",15,14,1.55,500,15,15,1.75,400,"Tue & Fri 12–6 pm, Sat 12–4 pm","週二及週五 中午12點至下午6點"),("button",17,17,1.0,700,17,17,1.0,500,"Book a consultation","預約諮詢")]
RADIUS=[("radius-sm","10px","SMALL: chips, language tab."),("radius-md","18px","MEDIUM: buttons, fields, FAQ rows."),("radius-lg","32px","LARGE: cards, illustrations, bands, menu sheet."),("radius-xl","48px","Story bands' inner corners and the photo frame.")]
SHADOWS=[("shadow-soft","0 6px 18px rgba(31, 53, 99, 0.08)","Cards on cream — a soft, low lift."),("shadow-float","0 14px 34px rgba(31, 53, 99, 0.18)","Mobile menu sheet and sticky bar only.")]
SECTION_RHYTHM="Sections: 80px top and bottom on desktop (<code>space-10</code>), 64px on mobile. No rules between sections: story bands change color (night → dawn → cream → day) and the hero ends in a soft hill line."
SHAPE_BORDERS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;border-radius:24px"><b>Soft edge</b><p class="ui-small">1px <code>border</code> on cards</p></div><div class="ui-fam" style="width:220px;border:1.5px solid var(--border-strong);border-radius:24px"><b>Control</b><p class="ui-small">1.5px <code>border-strong</code> — fields, chips</p></div><div class="ui-fam" style="width:220px;border:1px dashed var(--border-strong);border-radius:24px"><b>Placeholder</b><p class="ui-small">Dashed — coming soon, draft copy</p></div><div class="ui-fam c-paperdemo" style="width:220px;border-radius:24px"><b>Paper texture</b><p class="ui-small">A faint grain on cream grounds only</p></div></div>'''
SHAPE_SHADOWS='''<div class="ui-row-wrap"><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-soft);border-radius:24px"><b>shadow-soft</b><p class="ui-small">Cards on cream</p></div><div class="ui-fam" style="width:220px;box-shadow:var(--shadow-float);border-radius:24px"><b>shadow-float</b><p class="ui-small">Menu sheet, sticky bar</p></div></div>'''
IMAGERY_H=760
def imagery(B):
    return f'''<div class="c-img-grid"><div>{scene_morning("Example: morning scene")}</div>
<div class="ui-stack-lg"><p class="ui-body">Original illustrations in one hand: a 3px ink-blue line (<code>#16264A</code>) with round caps, flat pastel fills (sky, peach, butter, cream) — no gradients, no textures inside shapes. Children are drawn simply: round head, dark hair, dot eyes, rosy cheeks, small smile; always calm and safe, never crying, never at the doctor's in a scary way. Lenses appear only as a tidy case on the nightstand. Real photos only for Dr. Woo and the clinics, inside the illustrated frame.</p>
<div class="ui-dodont"><ul class="ok"><li>{icon("check")}<span>The night → morning → school story, one scene per band</span></li><li>{icon("check")}<span>Round, soft shapes and generous empty space</span></li><li>{icon("check")}<span>Real photos of Dr. Woo and the clinics in the frame</span></li></ul>
<ul class="no"><li>{icon("alert")}<span>Stock photography or AI-generated images</span></li><li>{icon("alert")}<span>Copying any real artist's or book's style or characters</span></li><li>{icon("alert")}<span>Eyes being touched, lenses on fingertips, needles, anything clinical-scary</span></li><li>{icon("alert")}<span>Grid-paper patterns, emoji</span></li></ul></div></div></div>'''
VOICE=dict(words=["Gentle","Reassuring","A little storybook"],
  right_en="Tonight, your child puts in the lenses and drifts off to sleep. In the morning, the world looks clear.", right_zh="今晚，孩子戴上鏡片安心入睡；明天早上，世界清清楚楚。", right_why="A tiny story in the child's day. Calm, concrete, no pressure.",
  wrong_en="Act now! Don't let myopia ruin your child's future.", wrong_zh="立即行動！別讓近視毀了孩子的未來！", wrong_why="Fear and urgency. We never scare parents into booking.")
INTRO="**Leads with: illustration.** Soft, hand-drawn scenes like a gentle Taiwanese picture book (an original style). The scroll tells a small story — asleep with lenses on the nightstand, waking up and seeing clearly, off to school — in soft pastels with a deep night blue for contrast."
COLOR_RULES="""- Pastels (sky, peach, butter) are grounds only. `text-primary`, `text-secondary` and night-blue `primary` pass on every one of them (4.9:1+).
- On the night band: headlines and body in `on-night` cream (11.4:1), secondary text in `on-night-muted` (8.1:1); the primary button turns butter with night-blue text (10:1).
- `success` and `error` pass on cream, white and every pastel (4.3:1+ on peach for error: use error on white/cream only).
- `border-strong` for control edges (3.3:1+)."""
TYPE_RULES="""- 圓體 throughout: Chiron GoRound TC (昭源圓體) — a free, open-source Traditional Chinese rounded face with real weights (400/500/700), so Chinese headlines are truly bold, not faux bold.
- Generous spacing: Chinese body line height 1.85, headings 1.35–1.55, `letter-spacing` .03em.
- English Quicksand 500 for body (never the 300/400 weights — too thin to read at 17px).
- **Simplified pages:** Chiron GoRound TC has no Simplified glyphs. Use Chiron GoRound's SC sibling if released, otherwise Resource Han Rounded SC or a rounded SC face; fallback PingFang SC."""
SHAPE_RULES="Borders: 1px `border` on cards, 1.5px `border-strong` on controls. Soft shapes everywhere; cream grounds carry a faint paper grain. Shadows: `shadow-soft` on cards, `shadow-float` on the mobile menu and sticky bar."
IMAGERY_RULES="""Original illustrations: 3px ink-blue line, round caps, flat pastel fills, no gradients. Children drawn simply and calmly (round head, dark hair, dot eyes, rosy cheeks). Lenses appear only as a tidy case on the nightstand. Real photos only for Dr. Woo and the clinics, inside the illustrated frame.

- Do: the night → morning → school story, one scene per band · round soft shapes · lots of empty space.
- Don't: stock or AI-generated images · copying any real artist's or book's style or characters · clinical-scary moments (eyes touched, lenses on fingertips) · grid-paper patterns · emoji."""
README_COLOR="# Color\n\nSoft pastels — sky blue, peach, soft yellow — on cream paper, with a deep night blue for contrast and action."
README_TYPE="# Typography\n\nQuicksand for English, 昭源圓體 Chiron GoRound TC for Chinese — both rounded and soft, with generous spacing."
README_SPACING="# Spacing & Layout\n\n8px steps, generous room. The page is a sequence of story bands."
README_SHAPE="# Shape\n\nLarge radii, soft shapes, a light paper texture on cream grounds."
README_ICONS="# Icons\n\nHand-drawn, soft line icons: 1.9px round stroke, round joins, drawn to sit beside the illustrations. Color `primary` (night blue); on the night band, cream. Never emoji."
README_IMAGERY="# Imagery\n\nOriginal illustrations carry the story; real photos only for Dr. Woo and the clinics."
README_VOICE="# Voice & Tone\n\nGentle, reassuring, a little storybook-like — small scenes from the child's day, never pressure."
README_COMP={
 "Primary button":"# Primary button\n\nNight-blue pill-soft button with white text; on the night band it turns butter with night-blue text, like the moon. Booking only.",
 "Secondary button":"# Secondary button\n\nWhite with a 1.5px night-blue outline; on the night band, transparent with a cream outline. Messaging and every non-booking action.",
 "Language switcher":"# Language switcher\n\nEN / 简体 / 繁體 in the soft top bar and in the footer; each is its own page. Current = ink with a peach underline.",
 "Top navigation + mobile menu":"# Top navigation + mobile menu\n\nCream bar, plain-text name in Quicksand (no logo), five links, small Book button. Mobile: Menu opens a soft white sheet.",
 "Hero block":"# Hero block\n\nThe night band: cream headline on night blue, the night scene on the right, a butter Book button, and a soft trust chip (Dr. Woo · 30 years). Ends in a peach hill line.",
 "3-step How it works block":"# 3-step How it works block\n\nOn the dawn (sky) band with the morning scene: three soft white cards, each with a peach number disc and a soft line icon.",
 "Doctor card":"# Doctor card\n\nA real photo of Dr. Woo with a child inside the illustrated frame (sky border + moon, sun, star doodles), then name, lines, languages and Book.",
 "FAQ accordion":"# FAQ accordion\n\nSoft white rows with large radius, a line question icon and a soft +/−.",
 "Booking call-to-action band":"# Booking call-to-action band\n\nThe day band: butter ground with the school scene, the heading and Book + Message. Last stop of the story.",
 "Location card":"# Location card\n\nSoft white card with a pastel map placeholder, name, address, hours, phones, Book here + Directions; Walnut shows coming soon.",
 "Contact row":"# Contact row\n\nSoft outlined chips: Call, Book online, WeChat, LINE, WhatsApp (dashed placeholders for the official marks).",
 "Form field set":"# Form field set\n\nSoft 18px-radius fields, labels above, night-blue focus ring; errors with an alert icon and a sentence.",
 "Footer":"# Footer\n\nBack to night: night-blue footer with cream text, a few stars. Name, languages, clinics, phones, legal links.",
}
PAPER="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .35 0 0 0 0 .2 0 0 0 .07 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E\")"
CSS=r"""
/* ===== SKIN · Concept C · Picture-Book ===== */
:root{--w-head:700;--w-label:700;--w-zh-head:700;--w-zh-label:500;
 --radius-btn:var(--radius-md);--radius-input:var(--radius-md);--focus:var(--primary);
 --btn-bg:var(--primary);--btn-fg:var(--on-primary);--btn-bg-hover:var(--primary-hover);--btn-bg-pressed:var(--primary-pressed);
 --btn2-bg:var(--surface);--btn2-fg:var(--primary);--btn2-border:var(--primary);
 --lang-mark:var(--accent);--utility-bg:var(--background);--header-bg:var(--background);--brand-ink:var(--primary);
 --icon:var(--primary);--numeral:var(--primary);--photo-bg:var(--secondary);--photo-fg:var(--text-primary);
 --band-bg:var(--butter);--band-fg:var(--text-primary);
 --footer-bg:var(--primary);--footer-fg:var(--on-night);--footer-muted:var(--on-night-muted);--footer-rule:#3E5584}
.ui-page{background-color:var(--background);background-image:PAPER;font-weight:500}
.ui-page:lang(zh),[lang|="zh"] .ui-page{font-weight:400;line-height:1.85;letter-spacing:.03em}
.ui-display,.ui-h1,.ui-h2,.ui-h3{letter-spacing:0}
:lang(zh) .ui-body{line-height:1.85}
.ui-mark{background:none;color:inherit}
.ui-step,.ui-faq details,.ui-loc{box-shadow:var(--shadow-soft)}
.ui-step{border-radius:var(--radius-lg)}
.ui-loc{border-radius:var(--radius-lg)}
.ui-faq details{border-radius:var(--radius-md)}
/* night band */
.c-night{background:var(--primary);color:var(--on-night);padding-bottom:var(--space-12)!important;
 --btn-bg:var(--butter);--btn-fg:var(--primary);--btn-bg-hover:#FFF4C9;--btn-bg-pressed:#F3DD86;--btn2-bg:transparent;--btn2-fg:var(--on-night);--btn2-border:var(--on-night);
 --wash:rgba(255,248,238,.12);--wash-strong:rgba(255,248,238,.2);--focus:var(--on-night);--icon:var(--butter)}
.c-night .ui-display{color:var(--on-night)}.c-night .ui-lead{color:var(--on-night)}.c-night .ui-eyebrow{color:var(--on-night-muted)}
.c-night .ui-display .ui-mark{color:var(--butter)}
.c-hills{position:absolute;left:0;right:0;bottom:-2px;height:64px;background:var(--background);background-image:PAPER;
 -webkit-mask:radial-gradient(120% 90px at 25% 100%,#000 60%,transparent 61%),radial-gradient(90% 80px at 80% 100%,#000 60%,transparent 61%);mask:radial-gradient(120% 90px at 25% 100%,#000 60%,transparent 61%),radial-gradient(90% 80px at 80% 100%,#000 60%,transparent 61%)}
.c-trust-chip{display:inline-flex;align-items:center;gap:10px;margin-top:var(--space-3);padding:10px 16px;border-radius:var(--radius-pill,999px);background:rgba(255,248,238,.1);border:1px solid rgba(255,248,238,.35);color:var(--on-night);font-weight:600;font-size:16px}
:lang(zh) .c-trust-chip{font-weight:500}
.c-trust-chip .ui-ico{color:var(--butter)}
.c-scene{display:block;width:100%;height:auto}
.c-hero-art{position:relative}
.c-story-cap{display:inline-flex;align-items:center;gap:8px;margin-top:10px;font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--on-night-muted)}
:lang(zh) .c-story-cap{letter-spacing:.2em}
/* dawn band */
.c-dawn{background:var(--secondary);border-radius:var(--radius-xl) var(--radius-xl) 0 0}
.c-dawn .c-story-cap{color:var(--text-secondary)}
.ui-how-head{display:grid;grid-template-columns:1fr minmax(0,360px);align-items:center;gap:var(--space-4)}
.ui-step{align-items:flex-start}
.c-stepnum{display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;border-radius:50%;background:var(--accent);color:var(--primary);font-family:var(--font-en-heading);font-weight:700;font-size:24px}
.c-stepico{position:absolute;top:var(--space-4);right:var(--space-4);color:var(--primary)}
.c-stepico .ui-ico{width:30px;height:30px}
.ui-step.is-current{background:var(--butter)}
@media (max-width:767px){.ui-how-head{grid-template-columns:1fr}.c-how-art{max-width:320px}.c-stepico{display:none}.c-stepnum{flex:none;width:44px;height:44px;font-size:20px}}
/* doctor frame */
.c-frame{position:relative;margin:0;padding:14px;background:var(--secondary);border-radius:var(--radius-xl);max-width:440px}
.c-frame .ui-photo{border-radius:calc(var(--radius-xl) - 12px);background:#E4F1FA}
.c-frame-doodle{position:absolute;width:64px;height:64px}
.c-frame-doodle--tl{top:-22px;left:-18px}.c-frame-doodle--br{bottom:-24px;right:-20px}.c-frame-doodle--tr{top:24px;right:-18px;width:40px;height:40px}
.c-paper{background:transparent}
.ui-n{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--secondary);font-size:18px}
/* band = day */
.ui-band{grid-template-columns:260px 1fr auto;background:var(--butter);border-radius:var(--radius-xl)}
.c-band-art{margin:-8px 0}
@media (max-width:1023px){.ui-band{grid-template-columns:1fr}.c-band-art{max-width:280px}}
.c-map{background:var(--secondary)}
.ui-footer{border-radius:var(--radius-xl) var(--radius-xl) 0 0;background-image:radial-gradient(circle at 12% 30%,rgba(252,235,168,.9) 0 2px,transparent 3px),radial-gradient(circle at 78% 18%,rgba(252,235,168,.9) 0 2px,transparent 3px),radial-gradient(circle at 60% 70%,rgba(252,235,168,.7) 0 1.5px,transparent 2.5px)}
.ui-footer .ui-brand{color:var(--on-night)}
.ui-footer :focus-visible{outline-color:var(--on-night)}
.c-scenes{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.c-scenes figure{margin:0;display:grid;gap:8px}
.c-img-grid{display:grid;grid-template-columns:minmax(260px,380px) 1fr;gap:32px;align-items:start}
.c-paperdemo{background-color:var(--background);background-image:PAPER}
@media (max-width:767px){.c-scenes,.c-img-grid{grid-template-columns:1fr}}
""".replace("PAPER",PAPER)

def cover():
    return """<!-- @dsCard height=300 -->
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Concept C · Picture-Book</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@700&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;height:100%}
  body{background:var(--background);color:var(--text-primary);font-family:var(--font-en-heading);overflow:hidden}
  .cover{position:relative;width:960px;height:300px;overflow:hidden}
  .art{position:absolute;top:0;left:480px;width:480px;height:300px}
  .night{fill:var(--primary)} .sky{fill:var(--secondary)} .peach{fill:var(--accent)} .butter{fill:var(--butter)} .cream{fill:var(--background)}
  .words{position:absolute;left:48px;bottom:44px;max-width:440px}
  .name{margin:0;font-size:60px;line-height:.98;font-weight:700;color:var(--primary)}
  .tag{margin:14px 0 0 2px;font-size:14px;line-height:20px;color:var(--text-secondary)}
</style>
</head>
<body>
<div class="cover">
<svg class="art" viewBox="0 0 480 300" aria-hidden="true">
<!--
  blocks      primary (night blue) 256×300 slab bleeding off top, bottom and right · secondary (sky) 176×176 disc · accent (peach) half-round hill 288×96 · butter moon disc r40 — ~40% of the cover
  arrangement one tall night slab with satellites: the sky disc rising behind it, a peach hill across the bottom, the moon on the slab
  pattern     discs and half-rounds, from "large radii, soft shapes": a few small butter dots (stars) at a space-4 pitch on the night slab
  scales      sides in space-2 multiples; radius-xl 48 on the slab's open corner; discs = half their side
-->
<rect class="night" x="224" y="-40" width="296" height="380" rx="48"/>
<circle class="sky" cx="160" cy="150" r="88"/>
<circle class="butter" cx="336" cy="96" r="40"/>
<circle class="night" cx="356" cy="84" r="34"/>
<path class="peach" d="M0 300c40-64 120-96 208-96s168 32 208 96z"/>
<circle class="butter" cx="272" cy="176" r="4"/><circle class="butter" cx="432" cy="144" r="4"/><circle class="butter" cx="400" cy="208" r="3"/><circle class="butter" cx="304" cy="48" r="3"/><circle class="butter" cx="448" cy="64" r="4"/>
</svg>
<div class="words">
<h1 class="name">Concept C ·<br>Picture-Book</h1>
<p class="tag">Night, morning, school — a gentle story for worried parents.</p>
</div>
</div>
</body>
</html>
"""
