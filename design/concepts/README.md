# 1234 Ortho-K Vision Care — website design concepts

Five website design concepts for **1234 Ortho-K Vision Care / 1234兒童視力矯正中心** (Dr. Paul T. Woo, OD — ortho-k for children, Alhambra + Walnut, CA). Every concept has the same structure — design system sections 1–8, the same 13 components, the same homepage — so the client can compare them side by side and pick and choose. Only the style changes.

| Concept | Leads with | Look | Design system on claude.ai |
|---|---|---|---|
| A · Friendly Notebook | Voice | Paper, ink, one tomato accent, emoji markers, day + night themes | https://claude.ai/artifact/7oLPr1PECEb7y2PCXHhS9j |
| B · Grid-Paper Classroom | Pattern | 田字格 exercise-book grid, green / red pen / pencil yellow, stickers | https://claude.ai/artifact/KrtDA1WNqnnneqGND6ai68 |
| C · Picture-Book | Illustration | Pastels + night blue, night → morning → school story | https://claude.ai/artifact/NqbVqHyU6u3ACyY5rNNHh5 |
| D · Calm Clinical | Photography | White, deep teal, apricot buttons, large photos, trust strip | https://claude.ai/artifact/TSKVbBp12KaunwtAvyfAgn |
| E · Modern Practice | Convention | Navy, stone, brass, serif headlines, full-width hero photo | https://claude.ai/artifact/2z9r4TkVFdLERNpjRmRJy8 |

The claude.ai links are private until shared from each page's Share menu.

## Folder layout

```
index.html                     gallery: every concept, every preview card, both homepages
concepts/<X-name>/
  project/                     the design system, exactly as published
    README.md                  brand book: sections 1–8 (color, type, spacing, shape, components, icons, imagery, voice)
    tokens.json                all tokens (colors with contrast notes, type scale EN + 繁中, spacing, radius, shadow)
    design-system.json         index for the claude.ai Design System viewer — don't hand-edit
    components/bundle.css      ALL component CSS (A: .nb-* classes; B–E: shared .ui-* structure + concept skin)
    components/<Name>/         README.md (usage rules) + preview.html (live card; line 1 is a viewer marker)
    fonts/                     A only: jf open 粉圓 subset (woff2, OFL)
  preview/<Name>/preview.html  same cards wired to local CSS — open these in a browser
  tokens.local.css             tokens compiled to CSS custom properties (what the viewer generates)
  Concept*-homepage-*.html     standalone, self-contained homepages (EN, 繁體) — send to a phone
generator/                     Python scripts that produced everything (see below)
```

## Viewing locally

Serve the folder (relative CSS and Google Fonts need http, not file://): `npx serve .` then open `index.html`.

## Regenerating

Python 3.11+. `pip install fonttools brotli playwright`.

- Concepts B–E: `cd generator && python3 make_concept.py B C D E` → writes `generator/out/<X>/`. Structure lives in `base.py` + `base.css`; each concept is one `concept_<x>.py` (tokens, skin CSS, art, README text). Copy is in `content.py`.
- Concept A was built earlier with its own script: `tokens_gen.py` + `gen.py` (writes `project/` and `local/` in the working dir); `subset.py` re-subsets the Chinese font (needs the full `jf-openhuninn-2.1.ttf` from github.com/justfont/open-huninn-font).
- `contrast.py` = WCAG contrast helper; `shot2.py` / `tile.py` = Playwright screenshot QA.

## Rules every concept follows

- Languages: EN / 简体 / 繁體 as separate pages, switcher always visible. Chinese body ≥17px, line height ≥1.7.
- No logo — the header is the plain text "1234 Ortho-K Vision Care".
- Only the client's copy. No statistics, success rates, patient counts, "best" / "most effective".
- All text passes WCAG AA (each Color card has the contrast table).
- Book a consultation in the first screen and at the bottom; mobile has a sticky Book / Message bar.

## Open issues (carry these into the tracker)

1. Copy conflict: EN "30 years of ortho-k experience" vs 繁中 「近30年」 ("nearly 30"). Dr. Woo to confirm one.
2. Simplified Chinese fonts: A (jf open 粉圓) and C (Chiron GoRound TC) have no SC glyphs — need a rounded SC face. B, D, E have Google SC equivalents.
3. All photos, maps and the WeChat / LINE / WhatsApp icons are placeholders. D and E depend on a real photo shoot (shot briefs are in each photo slot and the Imagery card).
4. Concept C illustrations are a first pass, not final art.
5. Walnut address and hours: "coming soon" everywhere.
6. Placeholder copy: First-visit lines, FAQ answers, UI labels (nav, buttons, form labels) and all 繁中 UI translations were written by Claude — needs client/native review.
7. Concept A self-hosts a 70 KB font subset; production should subset per page at build time.
