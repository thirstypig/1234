# 1234 Ortho-K Vision Care

New website for 1234 Ortho-K Vision Care (Dr. Paul T. Woo, OD; Alhambra
and Walnut, CA), built from design Concept C ("Picture Book"). Preview:
<https://1234.pasadenaworks.com/en/> (password-protected, not indexed).

## Commands

| Command | Action |
| :-- | :-- |
| `npm install` | Install dependencies (Node ≥ 22.12) |
| `npm run dev` | Dev server at `localhost:4321` |
| `npm run build` | Build the site to `dist/` |
| `bash scripts/assemble.sh` | Build the full GitHub Pages output (site + concepts + catalog) |
| `npm test` | Unit tests, then Playwright + axe on all 39 pages |
| `npm run test:deploy` | Check the assembled Pages layout |
| `npm run harvest` | Re-download images from the old 1234orthok.com |

## Layout

```text
src/pages/[lang]/        13 pages × en / zh-hans / zh-hant
src/features/<page>/     page compositions
src/components/          one component per Concept C component
src/content/copy/        all page text, one JSON file per language
assets/legacy/           old-site image catalog (originals stay local)
design/concepts/         the five design concepts (never edited)
workers/comments/        Cloudflare Worker: review comments + booking requests
docs/copy-review.md      old-site claims and copy changes awaiting client sign-off
```

See `CLAUDE.md` for the project rules.
