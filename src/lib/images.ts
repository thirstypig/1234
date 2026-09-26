import type { ImageMetadata } from 'astro';
import catalog from '../../assets/legacy/catalog.json';
import { assertUsable, type Entry } from './images-guard';

const files = import.meta.glob<{ default: ImageMetadata }>('../../assets/legacy/site/*.{png,jpg,jpeg,webp,gif}', { eager: true });

/** The only way pages may use a legacy image; fails the build for unapproved ones. */
export function legacyImage(file: string): ImageMetadata {
  assertUsable(file, catalog as Entry[]);
  const mod = files[`../../assets/legacy/site/${file}`];
  if (!mod) throw new Error(`Image "${file}" is catalogued but missing from assets/legacy/site (run node scripts/harvest/review-page.mjs)`);
  return mod.default;
}
