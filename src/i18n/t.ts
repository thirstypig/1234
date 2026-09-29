import en from '../content/copy/en.json';
import zhHans from '../content/copy/zh-hans.json';
import zhHant from '../content/copy/zh-hant.json';
import type { Lang } from './locales';

type Dict = { [k: string]: string | Dict };
const DICTS: Record<Lang, Dict> = { en, 'zh-hans': zhHans, 'zh-hant': zhHant };

function lookup(d: Dict, key: string): string | undefined {
  const v = key.split('.').reduce<unknown>((o, k) => (o && typeof o === 'object' ? (o as Dict)[k] : undefined), d);
  return typeof v === 'string' ? v : undefined;
}

function keys(d: Dict, prefix = ''): string[] {
  return Object.entries(d).flatMap(([k, v]) => (typeof v === 'string' ? [prefix + k] : keys(v, `${prefix}${k}.`)));
}

export function makeT(lang: Lang) {
  return (key: string): string => {
    const v = lookup(DICTS[lang], key);
    if (v === undefined) throw new Error(`Missing copy key "${key}" for ${lang}`);
    return v;
  };
}

/** Every en key missing from another locale, and every key only that locale has. */
export function checkParity(): string[] {
  const base = new Set(keys(DICTS.en));
  const out: string[] = [];
  for (const lang of ['zh-hans', 'zh-hant'] as const) {
    const ks = new Set(keys(DICTS[lang]));
    for (const k of base) if (!ks.has(k)) out.push(`${lang}: missing ${k}`);
    for (const k of ks) if (!base.has(k)) out.push(`${lang}: extra ${k}`);
  }
  return out;
}
