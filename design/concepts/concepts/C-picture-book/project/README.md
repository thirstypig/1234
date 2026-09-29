**1234 Ortho-K Vision Care · 1234兒童視力矯正中心** — website design concept C of four. **Leads with: illustration.** Soft, hand-drawn scenes like a gentle Taiwanese picture book (an original style). The scroll tells a small story — asleep with lenses on the nightstand, waking up and seeing clearly, off to school — in soft pastels with a deep night blue for contrast.

No logo is designed here. The header shows the plain text **1234 Ortho-K Vision Care** in the English heading font; Chinese pages add **1234兒童視力矯正中心** beneath it. Logo and identity are a separate project.

## 1. Color

Soft pastels — sky blue, peach, soft yellow — on cream paper, with a deep night blue for contrast and action.

| Role | Token | Hex | Use |
|---|---|---|---|
| Primary | `primary` | #1F3563 | Primary button fill, headings' deep accent, icons, the night band. White on it 12:1. As text on every pastel (8.7:1+). |
| Secondary | `secondary` | #CFE6F5 | The dawn band, secondary fills, the photo frame, step discs. A ground only. |
| Accent | `accent` | #FBD3BC | Step-number discs, blankets and warm details in illustrations, the hills under the hero. A ground only. |
| Background | `background` | #FFF8EE | BACKGROUND · Cream paper with a light paper texture. |
| Surface (cards) | `surface` | #FFFFFF | SURFACE · Cards: steps, FAQ, locations, fields. |
| Text Primary | `text-primary` | #22304A | Headlines and body on cream, white and every pastel (9.5:1+). |
| Text Secondary | `text-secondary` | #4F5B72 | Captions, hours, hints on cream, white and every pastel (4.9:1+). |
| Border | `border` | #EADCC8 | BORDER · Soft card edges (decorative). |
| Success | `success` | #2D6A4F | 4.6:1+ on every ground. |
| Error | `error` | #B03A2E | 5.7:1 on cream, 6:1 on white. |

- Pastels (sky, peach, butter) are grounds only. `text-primary`, `text-secondary` and night-blue `primary` pass on every one of them (4.9:1+).
- On the night band: headlines and body in `on-night` cream (11.4:1), secondary text in `on-night-muted` (8.1:1); the primary button turns butter with night-blue text (10:1).
- `success` and `error` pass on cream, white and every pastel (4.3:1+ on peach for error: use error on white/cream only).
- `border-strong` for control edges (3.3:1+).

## 2. Typography

| Role | Family | Notes |
|---|---|---|
| English heading | **Quicksand 700** | Google Fonts · OFL · soft, rounded |
| English body | **Quicksand 500** | Google Fonts · OFL · 500 for body, never 300 |
| Chinese heading | **昭源圓體 700** | Chiron GoRound TC · OFL · 圓體 |
| Chinese body | **昭源圓體 400** | Chiron GoRound TC · ≥17px, line height 1.85 |

Type scale — desktop / mobile (mobile below 768px):

| Level | English px | 繁體中文 px | Line height EN · 中 |
|---|---|---|---|
| Display | 54 / 38 | 50 / 34 | 1.12 · 1.35 |
| H1 | 40 / 32 | 38 / 30 | 1.18 · 1.4 |
| H2 | 30 / 26 | 30 / 24 | 1.25 · 1.45 |
| H3 | 22 / 20 | 22 / 20 | 1.35 · 1.55 |
| Body | 18 / 17 | 18 / 17 | 1.7 · 1.85 |
| Small | 15 / 14 | 15 / 15 | 1.55 · 1.75 |
| Button | 17 / 17 | 17 / 17 | 1.0 · 1.0 |

- 圓體 throughout: Chiron GoRound TC (昭源圓體) — a free, open-source Traditional Chinese rounded face with real weights (400/500/700), so Chinese headlines are truly bold, not faux bold.
- Generous spacing: Chinese body line height 1.85, headings 1.35–1.55, `letter-spacing` .03em.
- English Quicksand 500 for body (never the 300/400 weights — too thin to read at 17px).
- **Simplified pages:** Chiron GoRound TC has no Simplified glyphs. Use Chiron GoRound's SC sibling if released, otherwise Resource Han Rounded SC or a rounded SC face; fallback PingFang SC.

## 3. Spacing & Layout

- Spacing steps on 8px: `space-0-5` 4 · `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-10` 80 · `space-12` 96.
- Page max width **1120px** (`page-max`); paragraphs and FAQ answers max **680px** (`reading-max`).
- Desktop ≥1024px: **12 columns**, 24px gutter. Tablet: 8 columns. Mobile <768px: **4 columns**, 16px gutter, 20px side margins.
- Sections: 80px top and bottom on desktop (`space-10`), 64px on mobile. No rules between sections: story bands change color (night → dawn → cream → day) and the hero ends in a soft hill line.

## 4. Shape

- Radius: `radius-sm` 10px · `radius-md` 18px · `radius-lg` 32px · `radius-xl` 48px.
- Borders: 1px `border` on cards, 1.5px `border-strong` on controls. Soft shapes everywhere; cream grounds carry a faint paper grain. Shadows: `shadow-soft` on cards, `shadow-float` on the mobile menu and sticky bar.

## 5. Components

In this order: **Primary button · Secondary button · Language switcher · Top navigation + mobile menu · Hero block · 3-step How it works block · Doctor card · FAQ accordion · Booking call-to-action band · Location card · Contact row · Form field set · Footer.** Concept C extras: **Story scenes · Illustrated photo frame.**

- Every interactive component shows default, hover and pressed; keyboard focus is always a solid 3px ring.
- Booking is the only primary action; Message us is always the secondary button beside it.
- Mobile keeps **Book a consultation** and **Message us** in a sticky bottom bar, because the clinic is open only a few days a week.
- Placeholders look like placeholders: dashed boxes for app icons, "Placeholder copy" tags, "coming soon" for Walnut.

## 6. Icons

Hand-drawn, soft line icons: 1.9px round stroke, round joins, drawn to sit beside the illustrations. Color `primary` (night blue); on the night band, cream. Never emoji. The six sample icons: eye · moon · sun · calendar · phone · question. The same set also covers message, pin, lens, clock, map, camera, check, alert, menu, close, arrow. WeChat, LINE and WhatsApp use each company's official mark (dashed placeholders until then).

## 7. Imagery

Original illustrations: 3px ink-blue line, round caps, flat pastel fills, no gradients. Children drawn simply and calmly (round head, dark hair, dot eyes, rosy cheeks). Lenses appear only as a tidy case on the nightstand. Real photos only for Dr. Woo and the clinics, inside the illustrated frame.

- Do: the night → morning → school story, one scene per band · round soft shapes · lots of empty space.
- Don't: stock or AI-generated images · copying any real artist's or book's style or characters · clinical-scary moments (eyes touched, lenses on fingertips) · grid-paper patterns · emoji.

## 8. Voice & Tone

**Gentle · Reassuring · A little storybook** — Gentle, reassuring, a little storybook-like — small scenes from the child's day, never pressure.

- Right: "Tonight, your child puts in the lenses and drifts off to sleep. In the morning, the world looks clear." / 「今晚，孩子戴上鏡片安心入睡；明天早上，世界清清楚楚。」
- Wrong: "Act now! Don't let myopia ruin your child's future." / 「立即行動！別讓近視毀了孩子的未來！」

Never add statistics, success rates, patient counts, or "best" / "most effective" claims.

## Homepage

Four live cards at the end: desktop (1280px) and mobile (390px), in English and Traditional Chinese, built only from these components. Section order is identical in all four concepts: header → hero → the problem → how ortho-k works → meet the doctor → first visit → parent questions → book + locations → booking band → footer.
