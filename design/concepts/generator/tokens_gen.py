import json
C=[
("primary","#C23B1C","#FF8A66","PRIMARY · Tomato. The one warm accent. Fills the primary button and marks the current language. Text on it is `on-primary` (5.3:1 day, 7.9:1 night). As text it reads on `background` and `surface` only (4.9:1+) — never on `accent`."),
("primary-hover","#A8321A","#FFA285","Primary button hover. `on-primary` on it: 6.7:1 day, 9.4:1 night."),
("primary-pressed","#8E2A15","#F07350","Primary button pressed. `on-primary` on it: 8.4:1 day, 6.4:1 night."),
("on-primary","#FFFFFF","#1B130E","Label and emoji on any `primary` fill. White by day, near-black at night (the night tomato is light)."),
("secondary","#1E1A16","#F3EDE4","SECONDARY · Ink. Outline and label of the secondary button, the focus ring, the language underline on hover. Same value as `text-primary`: the notebook is ink + one accent."),
("secondary-hover","#F1EBE1","#2B261F","Wash behind the secondary button, nav links and FAQ rows on hover. `text-primary` on it 14.6:1 / 12.9:1."),
("secondary-pressed","#E6DDD0","#373028","Wash for pressed secondary controls and the open FAQ row. `text-primary` 12.9:1 / 11.2:1; `text-secondary` 5.7:1 / 6.4:1."),
("accent","#FFE1D2","#4A2518","ACCENT · Marker. A highlighter stroke behind a few words (the hero's second line) and the selected-step tint. Only `text-primary` sits on it (14.0:1 / 11.5:1). Use at most once per screen."),
("background","#FAF6EF","#16130F","BACKGROUND · Paper. The page."),
("surface","#FFFDF8","#201C17","SURFACE · Card. Note cards, FAQ, location cards, form fields, the mobile menu sheet."),
("surface-muted","#EDE6DA","#2A251F","Photo and map placeholders; the footer ground. `text-secondary` on it 6.2:1 / 7.5:1."),
("text-primary","#1E1A16","#F3EDE4","TEXT PRIMARY · Ink. Headlines and body on `background`, `surface`, `surface-muted`, `accent` and both washes — 11:1 or better in both themes."),
("text-secondary","#5A5249","#BFB5A8","TEXT SECONDARY · Pencil. Captions, hours, placeholders, footer text, on `background`, `surface`, `surface-muted` and washes — 5.7:1 or better in both themes."),
("border","#E4DDD1","#3A332B","BORDER · Hairline. 1px dividers and card outlines. Decorative only — never the only edge of a control."),
("border-strong","#8A8075","#857A6D","Control edge: form fields, the theme toggle, contact chips. 3.6:1 on `background`, 3.8:1 on `surface` by day; 4.4:1 / 4.0:1 at night."),
("success","#2E6B45","#86CFA0","SUCCESS · Leaf. \"Sent\" confirmations, always with ✅ and words. 5.9:1+ on `background`/`surface` in both themes."),
("error","#A8251A","#FF9285","ERROR · Red pen. Field errors, always with a ❗ and a sentence, never color alone. Darker than `primary` by day (6.6:1 vs 4.9:1) so the two don't read as the same red."),
]
tokens={"name":"1234 Ortho-K · Concept A · Friendly Notebook","version":1,
"color":{"themes":[{"id":"day","name":"Day"},{"id":"night","name":"Night"}],
 "tokens":[{"name":n,"value":{"day":d,"night":ni},"usage":u} for n,d,ni,u in C]},
"type":{
 "fonts":[{"family":"jf openhuninn","file":"fonts/jf-openhuninn-2.1-subset.woff2","weight":"400","style":"normal"}],
 "families":{
  "en-heading":"Nunito, \"Varela Round\", ui-rounded, system-ui, sans-serif",
  "en-body":"Nunito, \"Varela Round\", ui-rounded, system-ui, sans-serif",
  "zh-heading":"\"jf openhuninn\", \"PingFang TC\", \"Noto Sans TC\", \"Microsoft JhengHei\", sans-serif",
  "zh-body":"\"jf openhuninn\", \"PingFang TC\", \"Noto Sans TC\", \"Microsoft JhengHei\", sans-serif"},
 "groups":[]}}
S=[ # name, en desk, en mob, en lh, en wt, zh desk, zh mob, zh lh, sampleEN, sampleZH
("display",56,40,1.08,800,52,36,1.3,"Clear vision all day.","白天看得清楚，"),
("h1",40,32,1.15,800,38,30,1.35,"Book a visit at either clinic","兩間診所，歡迎預約"),
("h2",30,26,1.2,800,30,24,1.4,"Is your child's prescription going up every year?","孩子的近視度數每年都在增加嗎？"),
("h3",22,20,1.3,800,22,20,1.5,"Custom lenses made for your child","為孩子量身訂製鏡片"),
("body",18,17,1.6,400,18,17,1.8,"Your child wears special lenses while they sleep.","孩子晚上睡覺時戴上特製鏡片，早上取下就能看清楚。"),
("small",15,14,1.5,600,15,15,1.7,"Tue & Fri 12–6 pm, Sat 12–4 pm","週二及週五 中午12點至下午6點"),
("button",17,17,1.0,800,17,17,1.0,"Book a consultation","預約諮詢"),
]
g=lambda name,fam,rows: {"name":name,"family":fam,"styles":rows}
en_d,en_m,zh_d,zh_m=[],[],[],[]
for n,ed,em,el,ew,zd,zm,zl,se,sz in S:
  fam_en="en-heading" if n in("display","h1","h2","h3","button") else "en-body"
  fam_zh="zh-heading" if n in("display","h1","h2","h3","button") else "zh-body"
  en_d.append({"name":f"en-{n}","family":fam_en,"fontSize":f"{ed}px","lineHeight":el,"fontWeight":ew,"sample":se,"usage":f"English {n}, desktop (≥768px). Mobile: `en-{n}-m` ({em}px)."})
  en_m.append({"name":f"en-{n}-m","family":fam_en,"fontSize":f"{em}px","lineHeight":el,"fontWeight":ew,"sample":se,"usage":f"English {n}, mobile (<768px)."})
  zw=400
  zh_d.append({"name":f"zh-{n}","family":fam_zh,"fontSize":f"{zd}px","lineHeight":zl,"fontWeight":zw,"letterSpacing":"0.02em","sample":sz,"usage":f"Traditional Chinese {n}, desktop. Mobile: `zh-{n}-m` ({zm}px). jf open 粉圓 has one weight: hierarchy comes from size and space, never faux bold."})
  zh_m.append({"name":f"zh-{n}-m","family":fam_zh,"fontSize":f"{zm}px","lineHeight":zl,"fontWeight":zw,"letterSpacing":"0.02em","sample":sz,"usage":f"Traditional Chinese {n}, mobile (<768px)."})
tokens["type"]["groups"]=[g("English · desktop","en-heading",en_d),g("English · mobile","en-heading",en_m),g("繁體中文 · desktop","zh-heading",zh_d),g("繁體中文 · mobile","zh-heading",zh_m)]
sp=[("space-0-5","4px","Hairline gaps: emoji to label inside a chip."),("space-1","8px","Base unit. Gap between stacked small text; icon to text."),("space-2","16px","Inside chips and inputs (horizontal); gap between buttons."),("space-3","24px","Card padding on mobile; button horizontal padding; grid gutter desktop."),("space-4","32px","Card padding on desktop; gap between cards."),("space-6","48px","Gap between a section heading and its content on desktop."),("space-8","64px","Section padding on mobile."),("space-10","80px","Section padding on desktop (top and bottom)."),("space-12","96px","Hero top padding on desktop."),
("page-max","1120px","Page max width (content box). Centered, `space-3` side padding desktop."),("reading-max","680px","Max width of any paragraph or FAQ column — the notebook stays narrow."),("gutter-mobile","20px","Side margin on phones."),("grid-desktop","12","Desktop columns (≥1024px): 12 × 1fr, 24px gutter inside `page-max`."),("grid-tablet","8","Tablet columns (768–1023px): 8 × 1fr, 24px gutter."),("grid-mobile","4","Mobile columns (<768px): 4 × 1fr, 16px gutter, `gutter-mobile` margins.")]
tokens["spacing"]={"tokens":[{"name":a,"value":b,"usage":c} for a,b,c in sp[:9]]}
tokens["layout"]={"note":"Page width and column grid.","tokens":[{"name":a,"value":b,"usage":c} for a,b,c in sp[9:]]}
tokens["radius"]={"tokens":[{"name":"radius-sm","value":"6px","usage":"SMALL: chips, contact-row icons, language underline caps, inputs' inner elements."},{"name":"radius-md","value":"12px","usage":"MEDIUM (default): buttons, inputs, FAQ rows, note cards on mobile."},{"name":"radius-lg","value":"20px","usage":"LARGE: note cards on desktop, photo frame, booking band, mobile menu sheet."},{"name":"radius-pill","value":"999px","usage":"The light/night toggle and the mobile sticky bar only."}]}
tokens["border"]={"tokens":[{"name":"border-hairline","value":"1px","usage":"Width of every divider and card outline (`border` color)."},{"name":"border-control","value":"1.5px","usage":"Width of control edges: secondary button, inputs, toggle (`border-strong` / `secondary`)."},{"name":"focus-width","value":"3px","usage":"Keyboard focus: a solid 3px `secondary` outline, 3px offset. ≥ 11:1 on every surface."}]}
tokens["shadow"]={"note":"Almost none. Paper sits flat; edges come from 1px borders.","tokens":[{"name":"shadow-none","value":"none","usage":"Default for every card, button and field."},{"name":"shadow-sheet","value":{"day":"0 12px 32px rgba(30, 26, 22, 0.12)","night":"0 12px 32px rgba(0, 0, 0, 0.5)"},"usage":"ONLY the mobile menu sheet and the mobile sticky booking bar — things that float over the page."}]}
json.dump(tokens,open('project/tokens.json','w'),ensure_ascii=False,indent=1)
# compile a tokens.css for local rendering
css=[]
th=lambda t:":root, [data-theme=\"day\"]" if t=="day" else "[data-theme=\"night\"]"
for t in ("day","night"):
  css.append(th(t)+"{"+";".join(f"--{n}:{d if t=='day' else ni}" for n,d,ni,u in C)+";--shadow-none:none;--shadow-sheet:"+tokens["shadow"]["tokens"][1]["value"][t]+"}")
css.append(":root{"+";".join(f"--{x['name']}:{x['value']}" for fam in ("spacing","layout","radius","border") for x in tokens[fam]["tokens"])+";"+";".join(f"--font-{k}:{v}" for k,v in tokens["type"]["families"].items())+"}")
css.append("@font-face{font-family:'jf openhuninn';src:url(project/fonts/jf-openhuninn-2.1-subset.woff2) format('woff2');font-weight:400;font-display:swap}")
open('tokens.local.css','w').write("\n".join(css))
print("ok", len(C))
