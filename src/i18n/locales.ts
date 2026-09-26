export const LOCALES = ['en', 'zh-hans', 'zh-hant'] as const;
export type Lang = (typeof LOCALES)[number];
export const PAGES = ['home', 'about', 'ortho-k', 'contact', 'testimonials'] as const;
export type PageId = (typeof PAGES)[number];
export const HTML_LANG: Record<Lang, string> = { en: 'en', 'zh-hans': 'zh-Hans', 'zh-hant': 'zh-Hant' };
export const SWITCHER_LABEL: Record<Lang, string> = { en: 'EN', 'zh-hans': '简体', 'zh-hant': '繁體' };

export function pathFor(lang: Lang, page: PageId): string {
  return page === 'home' ? `/${lang}/` : `/${lang}/${page}/`;
}

export function getLangStaticPaths() {
  return LOCALES.map((lang) => ({ params: { lang } }));
}
