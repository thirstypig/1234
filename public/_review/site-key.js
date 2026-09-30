// Which comment thread a page of the preview site belongs to.
//
// The Worker stores comments under `<concept>:<page>` and only accepts a concept that
// starts with A–E (workers/comments/src/index.ts), so every site thread uses the
// concept `C-site` — distinct from the Concept C mockup's own `C-picture-book` threads.
//
// pathname examples: '/en/', '/zh-hant/ortho-k/eye-exams/', '/zh-hans/faq/'
// Returns { concept: 'C-site', page: <string> }.
export const SITE_CONCEPT = 'C-site';

// Each language gets its own thread (owner decision, 2026-09-29): the Chinese pages lay
// out differently, so pins only line up within one language.
// '/zh-hant/ortho-k/eye-exams/' -> 'zh-hant/ortho-k/eye-exams'; '/en/' -> 'en'.
export function commentKeyFor(pathname) {
  const page = pathname
    .replace(/index\.html$/, '')
    .replace(/^\/+|\/+$/g, '')
    .replace(/:/g, '-');
  return { concept: SITE_CONCEPT, page: page || 'root' };
}
