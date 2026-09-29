**1234 Ortho-K Vision Care · 1234兒童視力矯正中心** — website design concept A of four. **Leads with: voice.** The site reads like a warm, plain note from Dr. Woo to a worried parent: paper, ink, one tomato accent, big friendly headlines, emoji markers, one real photo. Concepts A–D share this exact structure; only the style changes.

No logo is designed here. The header shows the plain text **1234 Ortho-K Vision Care** in Nunito 800 (`en-heading`); Chinese pages add **1234兒童視力矯正中心** beneath it in `zh-heading`. Logo and identity are a separate project.

## 1. Color

Ink on paper, plus **one** warm accent (tomato). Two full palettes: **Day** (default) and **Night**. Every token is defined in both.

| Role | Token | Day | Night | Use |
|---|---|---|---|---|
| Primary | `primary` | #C23B1C | #FF8A66 | Primary button fill, current-language underline, First-visit numerals. Label on it: `on-primary` (#FFFFFF / #1B130E). |
| Secondary | `secondary` | #1E1A16 | #F3EDE4 | Ink. Secondary button outline + label, focus ring. |
| Accent | `accent` | #FFE1D2 | #4A2518 | Highlighter behind a few words (hero line 2). Only `text-primary` on it. Once per screen. |
| Background | `background` | #FAF6EF | #16130F | The page (paper). |
| Surface (cards) | `surface` | #FFFDF8 | #201C17 | Note cards, FAQ rows, location cards, fields, menu sheet. |
| Text Primary | `text-primary` | #1E1A16 | #F3EDE4 | Headlines and body. |
| Text Secondary | `text-secondary` | #5A5249 | #BFB5A8 | Captions, hours, "coming soon", footer. |
| Border | `border` | #E4DDD1 | #3A332B | 1px dividers and card outlines (decorative). |
| Success | `success` | #2E6B45 | #86CFA0 | Confirmation text, always with ✅ + words. |
| Error | `error` | #A8251A | #FF9285 | Field errors, always with ❗ + a sentence. |

State tokens: `primary-hover`, `primary-pressed`, `secondary-hover` (wash), `secondary-pressed`, `surface-muted` (photo/map placeholders, footer), `border-strong` (control edges, 3:1+).

**Contrast (WCAG AA, checked in both themes):**

- `text-primary` passes on every ground: `background`, `surface`, `surface-muted`, `accent`, both washes (11:1+).
- `text-secondary` passes on every ground (5.7:1+).
- `primary` as text passes on `background` and `surface` only (4.9:1 day). **Never on `accent`** (4.3:1 — fails).
- `on-primary` on `primary`, `primary-hover`, `primary-pressed`: 5.3 / 6.7 / 8.4 day; 7.9 / 9.4 / 6.4 night.
- `success` and `error` pass on `background`, `surface`, `accent` in both themes. `error` is darker than `primary` by day so a red-pen error never reads as a button.
- `border-strong` (control edges) is 3.6:1+ on every surface; the focus ring (`secondary`, 3px solid, 3px offset) is 11:1+.
- Night mode follows the device's `prefers-color-scheme` until the parent taps 🌙; the choice is remembered per browser.

## 2. Typography

| | Family | Notes |
|---|---|---|
| English heading | **Nunito 800** | Google Fonts, OFL. Rounded terminals. |
| English body | **Nunito 400 / 600** | Same family, calm weight. |
| Chinese heading | **jf open 粉圓** | justfont, OFL. Rounded, Traditional Chinese, one weight — hierarchy comes from size and space, never faux bold. |
| Chinese body | **jf open 粉圓** | ≥17px, line height 1.8 (spec asks ≥1.7). |

Type scale — desktop / mobile (break at 768px):

| Level | English | 繁體中文 | Line height EN · 中 |
|---|---|---|---|
| Display | 56 / 40 | 52 / 36 | 1.08 · 1.3 |
| H1 | 40 / 32 | 38 / 30 | 1.15 · 1.35 |
| H2 | 30 / 26 | 30 / 24 | 1.2 · 1.4 |
| H3 | 22 / 20 | 22 / 20 | 1.3 · 1.5 |
| Body | 18 / 17 | 18 / 17 | 1.6 · 1.8 |
| Small | 15 / 14 | 15 / 15 | 1.5 · 1.7 |
| Button | 17 / 17 | 17 / 17 | 1.0 · 1.0 |

Rules: set Chinese with `letter-spacing: .02em` (buttons and labels .06em). Chinese headlines are set slightly smaller than English because every glyph is a full square. Put the `lang` attribute on every page and every mixed-language snippet (`zh-Hant`, `zh-Hans`, `en`) — the CSS switches fonts on it.

**Simplified Chinese caution:** jf open 粉圓 covers Traditional only (it has no 简, 视, 矫, 预, 约, 询). For 简体 pages use a rounded SC face such as Resource Han Rounded SC (源样圆体, OFL); until it's installed the stack falls back to PingFang SC / Noto Sans SC. Self-host fonts and subset per page at build time — the full 粉圓 file is 4.9 MB; the subset used here is 70 KB.

## 3. Spacing & Layout

- Spacing steps on 8px: `space-0-5` 4 · `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-10` 80 · `space-12` 96.
- Page max width **1120px** content (`page-max`), 24px side padding. Paragraphs and FAQ never wider than **680px** (`reading-max`) — the notebook stays narrow.
- Desktop ≥1024px: **12 columns**, 24px gutter. Tablet 768–1023: 8 columns, 24px gutter. Mobile <768: **4 columns**, 16px gutter, 20px side margins.
- Sections: 80px top and bottom on desktop (`space-10`), 64px on mobile (`space-8`), separated by a single 1px `border` rule.

## 4. Shape

- Radius: `radius-sm` 6px (chips, language tab), `radius-md` 12px (buttons, fields, FAQ rows, cards on mobile), `radius-lg` 20px (note cards, photo, booking band, menu sheet), `radius-pill` (night toggle, sticky bar).
- Borders: 1px `border` for cards and dividers; 1.5px `border-strong` for controls; 1px dashed for placeholders and "coming soon".
- Shadow: **none** by default. `shadow-sheet` only on things that float — the mobile menu sheet and the sticky booking bar.

## 5. Components

In this order (see each card below): **Primary button · Secondary button · Language switcher · Top navigation + mobile menu · Hero block · 3-step How it works block · Doctor card · FAQ accordion · Booking call-to-action band · Location card · Contact row · Form field set · Footer.** Concept A extra: **Light-night toggle.**

- Interactive components show default, hover and pressed; keyboard focus is always the 3px ink ring.
- Booking is the only primary (tomato) action. Messaging is always the secondary button right beside it.
- Mobile: a sticky bottom bar keeps **📅 Book a consultation** and **💬 Message us** one tap away while scrolling, because the clinic is open only a few days a week and the phone often goes unanswered.
- Placeholders are visibly placeholders: dashed outlines for app icons, "Placeholder copy" tags on draft text, "coming soon" in `text-secondary` for Walnut.

## 6. Icons

Emoji, not drawn icons. Core six: 👀 eye · 🌙 moon · ☀️ sun · 📅 calendar · 📞 phone · ❓ question. Allowed extras: 💬 message · 📍 address/map · 📏 custom fit · 📷 photo placeholder · ✅ done · ❗ error. No others.

- Always beside words, always `aria-hidden`. Sizes 18 / 22 / 36 / 44px.
- Never in headlines, never as decoration on their own.
- WeChat, LINE and WhatsApp are **not** emoji — use each company's official mark from its brand kit (dashed placeholders until then).

## 7. Imagery

One real photograph on the homepage: **Dr. Woo with a child patient**, 4:5, `radius-lg`. Everything else is words.

- ✅ Do: natural window light, warm and soft · Dr. Woo at the child's eye level, both relaxed · no filters · written parental consent.
- ❗ Don't: stock or AI-generated people · close-ups of lenses on fingertips or eyes being touched · illustrations, gradients, overlays · text on photos.

## 8. Voice & Tone

**Kind · Plain · Conversational** — like a friend who happens to be an eye doctor, explaining over tea. Talk to the parent ("your child"), short sentences, no jargon, no claims.

- ✅ Right: "Not sure if ortho-k is right for your child? Let's talk it through." / 「不確定角膜塑型適不適合孩子？我們一起慢慢聊。」
- ❗ Wrong: "Orthokeratology utilizes reverse-geometry rigid gas-permeable lenses to induce controlled corneal reshaping." / 「本中心採用逆幾何高透氧硬式鏡片，誘導角膜可控性重塑。」

Never add statistics, success rates, patient counts, or "best" / "most effective" claims.

## Homepage

Four live cards at the end: desktop (1280px) and mobile (390px), in English and Traditional Chinese, built only from the components above. Section order: header → hero → the problem → how ortho-k works → meet the doctor → first visit → parent questions → book + locations → booking band → footer.
