**1234 Ortho-K Vision Care · 1234兒童視力矯正中心** — website design concept D of four. **Leads with: photography.** Premium, calm and specialist-led. Lots of white, one deep teal, one soft apricot for booking buttons, a clean sans, precise alignment and large real photographs. Friendly through warm words, not cartoons.

No logo is designed here. The header shows the plain text **1234 Ortho-K Vision Care** in the English heading font; Chinese pages add **1234兒童視力矯正中心** beneath it. Logo and identity are a separate project.

## 1. Color

White, one deep calm teal, and one soft apricot reserved for booking buttons.

| Role | Token | Hex | Use |
|---|---|---|---|
| Primary | `primary` | #0E4A56 | The calm color: headings' accent, icons, links, secondary button outline, the booking band and footer. White on it 9.8:1; as text 8.4:1+ on white, alt and tint. |
| Secondary | `secondary` | #E3EFF0 | The trust strip, step icon discs, hover washes. A ground only. |
| Accent | `accent` | #F4B183 | The primary (booking) button fill only; label `text-primary` 8.6:1. |
| Background | `background` | #FFFFFF | Lots of it. |
| Surface (cards) | `surface` | #FFFFFF | SURFACE · Cards on white, set apart by `shadow-sm` and a hairline. |
| Text Primary | `text-primary` | #13262B | Headlines and body on white, alt, tint and apricot (8.6:1+). |
| Text Secondary | `text-secondary` | #4A5C61 | Captions, labels, hours on white, alt and tint (6:1+). Not on apricot. |
| Border | `border` | #DCE4E5 | BORDER · Hairlines (decorative). |
| Success | `success` | #1F6B50 | 5.4:1+ on white, alt, tint. |
| Error | `error` | #B3372B | 5.1:1+ on white, alt, tint. |

- Lots of white. Deep teal `primary` is the one calm color; apricot `accent` is only the booking button's fill.
- `text-primary` passes everywhere, including apricot (8.6:1). `text-secondary`, success and error pass on white, `surface-alt` and teal tint (5.1:1+) — never on apricot.
- On deep teal (booking band, footer): white (9.8:1) and teal tint (8.4:1).
- `border-strong` (3:1+) for control edges. No bright primary colors anywhere.

## 2. Typography

| Role | Family | Notes |
|---|---|---|
| English heading | **Plus Jakarta Sans 700** | Google Fonts · OFL · modern, clean |
| English body | **Plus Jakarta Sans 400** | Google Fonts · OFL |
| Chinese heading | **思源黑體 Noto Sans TC 700** | Google Fonts · OFL · clean 黑體 |
| Chinese body | **思源黑體 Noto Sans TC 400** | ≥17px · line height 1.8 |

Type scale — desktop / mobile (mobile below 768px):

| Level | English px | 繁體中文 px | Line height EN · 中 |
|---|---|---|---|
| Display | 56 / 38 | 50 / 34 | 1.08 · 1.3 |
| H1 | 40 / 32 | 38 / 30 | 1.15 · 1.35 |
| H2 | 32 / 26 | 30 / 24 | 1.2 · 1.4 |
| H3 | 20 / 19 | 20 / 19 | 1.35 · 1.5 |
| Body | 18 / 17 | 18 / 17 | 1.65 · 1.8 |
| Small | 14 / 14 | 15 / 15 | 1.5 · 1.7 |
| Button | 16 / 16 | 17 / 17 | 1.0 · 1.0 |

- One family per script for a clean, strong hierarchy: Plus Jakarta Sans and Noto Sans TC, weights 400 / 500 / 700.
- Chinese body ≥17px, line height 1.8; Chinese headings 700, never tracked tight.
- **Simplified pages:** Noto Sans SC — same family, same weights, free on Google Fonts.

## 3. Spacing & Layout

- Spacing steps on 8px: `space-0-5` 4 · `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-10` 80 · `space-12` 96.
- Page max width **1120px** (`page-max`); paragraphs and FAQ answers max **680px** (`reading-max`).
- Desktop ≥1024px: **12 columns**, 24px gutter. Tablet: 8 columns. Mobile <768px: **4 columns**, 16px gutter, 20px side margins.
- Sections: 80px top and bottom on desktop (`space-10`), 64px on mobile. Sections alternate white and `surface-alt`; no rules, no decoration.

## 4. Shape

- Radius: `radius-sm` 4px · `radius-md` 6px · `radius-lg` 10px.
- Small radii (4 / 6 / 10px), precise alignment to the 12-column grid. Borders: 1px `border` hairlines; 1.5px `border-strong` on controls. Shadows: `shadow-sm` on cards and photos; `shadow-float` on the mobile menu and sticky bar.

## 5. Components

In this order: **Primary button · Secondary button · Language switcher · Top navigation + mobile menu · Hero block · 3-step How it works block · Doctor card · FAQ accordion · Booking call-to-action band · Location card · Contact row · Form field set · Footer.** Concept D extras: **Trust strip · Photo block.**

- Every interactive component shows default, hover and pressed; keyboard focus is always a solid 3px ring.
- Booking is the only primary action; Message us is always the secondary button beside it.
- Mobile keeps **Book a consultation** and **Message us** in a sticky bottom bar, because the clinic is open only a few days a week.
- Placeholders look like placeholders: dashed boxes for app icons, "Placeholder copy" tags, "coming soon" for Walnut.

## 6. Icons

Thin, clean line icons: 1.4px stroke, round caps, 24px grid, drawn in `primary` teal. Never emoji or filled icons. The six sample icons: eye · moon · sun · calendar · phone · question. The same set also covers message, pin, lens, clock, map, camera, check, alert, menu, close, arrow. WeChat, LINE and WhatsApp use each company's official mark (dashed placeholders until then).

## 7. Imagery

Large real photographs lead: Dr. Woo, the clinic, the eye-measurement equipment, a relaxed child patient. One photographer, one session: natural window light, warm tones, real people at ease. Fixed ratios: 4:5 people, 16:9 equipment, 4:3 spaces. Until photos exist, each slot shows its shot brief.

- Do: natural light · warm white balance · real patients with written parental consent · equipment shown in use · Dr. Woo at the child's eye level.
- Don't: stock or AI images · illustrations or emoji · cold blue clinical light · masks and gloves in the foreground · eyes being touched · text on photos.

## 8. Voice & Tone

**Confident · Calm · Expert, still gentle** — Confident, calm, expert — and still gentle with nervous kids.

- Right: "Dr. Woo will examine your child's eyes, map the front of each eye, and explain what he sees. Your child can ask questions too." / 「胡醫師會為孩子檢查眼睛、拍攝角膜地圖，並說明檢查結果。孩子也可以隨時發問。」
- Wrong: "Our world-class, state-of-the-art clinic delivers unmatched results." / 「本中心擁有世界級頂尖設備，效果無人能及。」

Never add statistics, success rates, patient counts, or "best" / "most effective" claims.

## Homepage

Four live cards at the end: desktop (1280px) and mobile (390px), in English and Traditional Chinese, built only from these components. Section order is identical in all four concepts: header → hero → the problem → how ortho-k works → meet the doctor → first visit → parent questions → book + locations → booking band → footer.
