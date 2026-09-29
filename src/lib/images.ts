import type { ImageMetadata } from 'astro';
import catalog from '../../assets/legacy/catalog.json';
import practice from '../../assets/practice/photos.json';
import { assertUsable, type Entry } from './images-guard';

const files = import.meta.glob<{ default: ImageMetadata }>('../../assets/legacy/site/*.{png,jpg,jpeg,webp,gif}', { eager: true });

/** The only way pages may use a legacy image; fails the build for unapproved ones. */
export function legacyImage(file: string): ImageMetadata {
  assertUsable(file, catalog as Entry[]);
  const mod = files[`../../assets/legacy/site/${file}`];
  if (!mod) throw new Error(`Image "${file}" is catalogued but missing from assets/legacy/site (run node scripts/harvest/review-page.mjs)`);
  return mod.default;
}

const practiceFiles = import.meta.glob<{ default: ImageMetadata }>('../../assets/practice/*.{png,jpg,jpeg,webp}', { eager: true });

/** Client-supplied photos; only staff or office shots may be listed (patient photos never go in this public repo). */
export function practicePhoto(file: string): ImageMetadata {
  const e = (practice as { file: string; subject: string }[]).find((p) => p.file === file);
  if (!e) throw new Error(`Photo "${file}" is not listed in assets/practice/photos.json`);
  if (!['staff', 'office'].includes(e.subject)) throw new Error(`Photo "${file}" has subject "${e.subject}"; only staff or office photos may be published`);
  const mod = practiceFiles[`../../assets/practice/${file}`];
  if (!mod) throw new Error(`Photo "${file}" is listed but missing from assets/practice`);
  return mod.default;
}
