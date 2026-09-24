**1234 Ortho-K Vision Care · 1234兒童視力矯正中心** — website design concept B of four. **Leads with: pattern.** Built around the 田字格 / 作文簿 exercise-book grid that parents from Taiwan, Hong Kong and mainland China grew up writing in. White paper, grid green, red pen, pencil yellow; stickers, red-pen checks and pasted-in photos. Plenty of white keeps it trustworthy.

No logo is designed here. The header shows the plain text **1234 Ortho-K Vision Care** in the English heading font; Chinese pages add **1234兒童視力矯正中心** beneath it. Logo and identity are a separate project.

## 1. Color

White paper with three school-supply accents: grid green (actions), red pen (checks and marks), pencil yellow (stickers). Lots of white keeps it trustworthy.

| Role | Token | Hex | Use |
|---|---|---|---|
| Primary | `primary` | #1D6A48 | Primary button fill, links, step numerals. White on it 6.6:1. As text: on `background`, `paper`, `wash` (5.9:1+). Not on `accent`. |
| Secondary | `secondary` | #C2272D | Check marks, the current-language underline, tag stickers, the first-visit numerals. As text 5.5:1+ on white and paper — short labels only. White on it 5.8:1. |
| Accent | `accent` | #F7CB46 | Round stickers, the highlighted line of the hero headline boxes. Only `text-primary` (10.4:1) and `text-secondary` (4.7:1) on it. |
| Background | `background` | #FFFFFF | Most of the page stays plain white so it reads trustworthy. |
| Surface (cards) | `surface` | #FFFFFF | White cards with a `border` edge; body copy always sits on these, never on the grid. |
| Text Primary | `text-primary` | #18241E | Headlines and body on every ground (13:1+). |
| Text Secondary | `text-secondary` | #4B5A52 | Captions, hours, hints, footer on white/paper/wash (5.9:1+). |
| Border | `border` | #D3DDD6 | BORDER · Card edges and dividers (decorative). |
| Success | `success` | #1D6A48 | SUCCESS · Same grid green, always with a check icon and words. |
| Error | `error` | #A3171C | ERROR · Darker than red pen (7.8:1 on white) and always with an alert icon and a sentence. |

- `text-primary` and `text-secondary` pass on every ground: white, `paper`, `wash`, and pencil-yellow `accent` (4.7:1+).
- `primary` (green) text passes on white, `paper` and `wash` (5.3:1+) — **never on yellow** (4.2:1).
- Red pen (`secondary`) is for check marks, the language underline and tag stickers; as text only for short labels on white (5.8:1). **Never on yellow** (3.8:1).
- White on `primary` 6.6:1, on `secondary` 5.8:1.
- `grid-line` and `grid-line-strong` are decorative and never sit under body text.
- `error` (#A3171C) is darker than red pen so an error never reads as a check mark; always with an alert icon and a sentence.

## 2. Typography

| Role | Family | Notes |
|---|---|---|
| English heading | **Fredoka 600** | Google Fonts · OFL · bold, rounded |
| English body | **Atkinson Hyperlegible** | Google Fonts · OFL · made for legibility |
| Chinese heading | **霞鶩文楷 TC** | LXGW WenKai TC · OFL · 楷書, handwriting-practice feel |
| Chinese body | **思源黑體 Noto Sans TC** | Google Fonts · OFL · plain and clear |

Type scale — desktop / mobile (mobile below 768px):

| Level | English px | 繁體中文 px | Line height EN · 中 |
|---|---|---|---|
| Display | 56 / 40 | 52 / 36 | 1.1 · 1.3 |
| H1 | 40 / 32 | 38 / 30 | 1.15 · 1.35 |
| H2 | 30 / 26 | 30 / 24 | 1.2 · 1.4 |
| H3 | 22 / 20 | 22 / 20 | 1.3 · 1.5 |
| Body | 18 / 17 | 18 / 17 | 1.6 · 1.8 |
| Small | 15 / 14 | 15 / 15 | 1.5 · 1.7 |
| Button | 17 / 17 | 17 / 17 | 1.0 · 1.0 |

- Chinese display and H2 headlines are written into **田字格 boxes**, one character per box (punctuation too), box = 1.25em. The hero's second line fills its boxes with pencil yellow. H1, H3 and long headlines are set plain.
- Chinese buttons, nav and labels use Noto Sans TC 500 (a 楷書 face is too delicate at 17px).
- Chinese body ≥17px, line height 1.8. English headlines never go in boxes.
- **Simplified pages:** swap to LXGW WenKai (SC) and Noto Sans SC — both free on Google Fonts, same look.

## 3. Spacing & Layout

- Spacing steps on 8px: `space-0-5` 4 · `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-10` 80 · `space-12` 96.
- Page max width **1120px** (`page-max`); paragraphs and FAQ answers max **680px** (`reading-max`).
- Desktop ≥1024px: **12 columns**, 24px gutter. Tablet: 8 columns. Mobile <768px: **4 columns**, 16px gutter, 20px side margins.
- Sections: 80px top and bottom on desktop (`space-10`), 64px on mobile. Sections are separated by a 2px `grid-line-strong` rule, like the margin line of an exercise book.

## 4. Shape

- Radius: `radius-sm` 3px · `radius-md` 6px · `radius-lg` 8px · `radius-sticker` 999px.
- Borders: 1px `border` for cards; 1.5px `border-strong` for controls; a 2px `grid-line-strong` rule between sections, like an exercise-book margin line. Shadows: none on cards; `shadow-sticker` only on stickers and pasted photos; `shadow-float` on the mobile menu and sticky bar.

## 5. Components

In this order: **Primary button · Secondary button · Language switcher · Top navigation + mobile menu · Hero block · 3-step How it works block · Doctor card · FAQ accordion · Booking call-to-action band · Location card · Contact row · Form field set · Footer.** Concept B extras: **Grid pattern · Sticker badge · Checked list.**

- Every interactive component shows default, hover and pressed; keyboard focus is always a solid 3px ring.
- Booking is the only primary action; Message us is always the secondary button beside it.
- Mobile keeps **Book a consultation** and **Message us** in a sticky bottom bar, because the clinic is open only a few days a week.
- Placeholders look like placeholders: dashed boxes for app icons, "Placeholder copy" tags, "coming soon" for Walnut.

## 6. Icons

Simple drawn line icons in a felt-marker style: 2.3px round stroke with a faint offset bleed underneath. Color `text-primary` or `primary`; red-pen `secondary` only for check marks. Never emoji. The six sample icons: eye · moon · sun · calendar · phone · question. The same set also covers message, pin, lens, clock, map, camera, check, alert, menu, close, arrow. WeChat, LINE and WhatsApp use each company's official mark (dashed placeholders until then).

## 7. Imagery

Real photos only, framed like prints pasted into an exercise book: 10px white border, translucent yellow tape, a tilt of −2° to +2°, `shadow-sticker`. Homepage photos: a child at school without glasses (hero), Dr. Woo with a child patient (doctor card).

- Do: real patients and the real clinic with written parental consent · natural light · everyday moments · max two pasted photos per screen.
- Don't: stock photos · watercolor or storybook illustration · photos on the grid behind body text · close-ups of lenses on fingertips.

## 8. Voice & Tone

**Encouraging · Clear · Patient** — Encouraging, clear, patient — a good teacher who praises the question and explains in small steps.

- Right: "Great question. Here's how it works, one step at a time." / 「問得好！我們一步一步來說明。」
- Wrong: "Failure to comply with the lens-care protocol may result in adverse outcomes." / 「若未遵守鏡片護理規範，可能導致不良後果。」

Never add statistics, success rates, patient counts, or "best" / "most effective" claims.

## Homepage

Four live cards at the end: desktop (1280px) and mobile (390px), in English and Traditional Chinese, built only from these components. Section order is identical in all four concepts: header → hero → the problem → how ortho-k works → meet the doctor → first visit → parent questions → book + locations → booking band → footer.
