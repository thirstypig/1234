# Prompt for Claude Code

Unzip `orthok-design-concepts.zip` somewhere on your machine first (e.g. `~/Downloads/orthok-design-concepts`), then `cd` into your repo and paste everything below the line into Claude Code. Replace the two ALL-CAPS placeholders.

---

I'm moving five website design concepts for a client into this repo. They were built in Claude (Cowork) as claude.ai Design System artifacts. I have the full export as a folder at PATH_TO_UNZIPPED_FOLDER (it contains README.md, index.html, concepts/, generator/). The GitHub repo is thirstypig/REPO_NAME.

**Context (read before doing anything):**
- Client: 1234 Ortho-K Vision Care (1234兒童視力矯正中心), Dr. Paul T. Woo, OD — ortho-k for kids, clinics in Alhambra and Walnut, CA. I'm the consultant (Pasadena Works). The site will be trilingual: English, Simplified Chinese, Traditional Chinese as separate URL paths.
- Five concepts: A Friendly Notebook, B Grid-Paper Classroom, C Picture-Book, D Calm Clinical, E Modern Practice. Same structure, different style. The client hasn't picked yet.
- Read the export's README.md first — it explains the folder layout, how to regenerate, the rules every concept follows, and the open issues.
- I'm a PM, not an engineer. Explain what you're doing in plain language, keep changes small, and ask before anything irreversible.

**Do this, in order. Stop and show me after step 3.**

1. **Branch.** Check `git status` is clean, pull main, then create branch `design/concepts-import`.

2. **Copy in, unchanged.** Copy the whole export folder into `design/concepts/` in the repo (so the repo has `design/concepts/README.md`, `design/concepts/index.html`, `design/concepts/concepts/…`, `design/concepts/generator/…`). Do not edit any design values, tokens, CSS or copy while importing. Add a `.gitignore` inside `design/concepts/generator/` for `out/`, `shots/`, `__pycache__/` and any `*.ttf`.

3. **Verify it works.** Serve `design/concepts/` locally (e.g. `npx serve design/concepts`) and use Playwright to screenshot, at 1280px and 390px wide, each concept's `preview/Homepage desktop EN/preview.html` and `preview/Homepage Traditional Chinese mobile/preview.html` (20 screenshots). Save them to `design/concepts/_qa/` (gitignored). Tell me if any page has broken CSS, missing fonts, horizontal scrolling, or overlapping elements. Don't fix anything yet — just report. **Stop here and show me.**

4. **Document it for future sessions.** Add a short section to the repo's `CLAUDE.md` (create it if missing) that says:
   - Design concepts live in `design/concepts/`; each concept's source of truth is `concepts/<X>/project/` (`tokens.json`, `README.md`, `components/bundle.css`, component READMEs).
   - The rules: EN / 简体 / 繁體 as separate pages with the switcher always visible; Chinese body ≥17px, line height ≥1.7; no logo (plain-text name); use only client-provided copy; never add statistics, success rates, patient counts, or "best/most effective" claims; all text WCAG AA; Book a consultation in the first screen and at the bottom; mobile sticky Book/Message bar.
   - Treat everything in `design/concepts/` as reference until the client picks a direction. Don't build pages from it without asking me.

5. **Track the open issues.** Using `gh`, create one GitHub issue per item in the export README's "Open issues" list, labeled `design` (create the label if needed). Keep titles short and bodies plain-English.

6. **Commit and open a PR.** Commit in two logical commits (import; docs + gitignore), push, and open a PR to main titled "Import website design concepts A–E" with a short summary: what's in it, how to view it locally, and links to the issues you created. Don't merge it.

**Don't:** redesign anything, rename concept folders, reformat the generated HTML/CSS, install new dependencies in the main app, or touch any existing app code.

**When the client picks a concept (later, not now):** the next job will be turning that concept's `tokens.json` + `bundle.css` into the real site's theme (CSS variables / Tailwind theme in our Next.js app) and rebuilding the homepage as components, with `/en`, `/zh-hans`, `/zh-hant` routes. Don't start this until I say so.
