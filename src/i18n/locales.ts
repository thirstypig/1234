export const LOCALES = ['en', 'zh-hans', 'zh-hant'] as const;
export type Lang = (typeof LOCALES)[number];
export const LEGAL = ['privacy', 'notice-of-privacy-practices', 'accessibility', 'terms', 'nondiscrimination'] as const;
export type LegalId = (typeof LEGAL)[number];
export const PAGES = ['home', 'about', 'ortho-k', 'contact', 'testimonials', 'community', 'eye-exams', 'eye-surface', ...LEGAL] as const;
export type PageId = (typeof PAGES)[number];
export const HTML_LANG: Record<Lang, string> = { en: 'en', 'zh-hans': 'zh-Hans', 'zh-hant': 'zh-Hant' };
export const SWITCHER_LABEL: Record<Lang, string> = { en: 'EN', 'zh-hans': '简体', 'zh-hant': '繁體' };

/** Pages that live under another page in the URL and the menu. */
export const PARENT: Partial<Record<PageId, PageId>> = { 'eye-exams': 'ortho-k', 'eye-surface': 'ortho-k' };

export function pathFor(lang: Lang, page: PageId): string {
  if (page === 'home') return `/${lang}/`;
  const parent = PARENT[page];
  return parent ? `/${lang}/${parent}/${page}/` : `/${lang}/${page}/`;
}

export function getLangStaticPaths() {
  return LOCALES.map((lang) => ({ params: { lang } }));
}
