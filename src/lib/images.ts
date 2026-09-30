import type { ImageMetadata } from 'astro';
import catalog from '../../assets/legacy/catalog.json';
import practice from '../../assets/practice/photos.json';
import patients from '../../assets/patients/photos.json';
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

/** Client-supplied photos of staff or the office (patient photos go through patientPhoto()). */
export function practicePhoto(file: string): ImageMetadata {
  const e = (practice as { file: string; subject: string }[]).find((p) => p.file === file);
  if (!e) throw new Error(`Photo "${file}" is not listed in assets/practice/photos.json`);
  if (!['staff', 'office'].includes(e.subject)) throw new Error(`Photo "${file}" has subject "${e.subject}"; only staff or office photos may be published`);
  const mod = practiceFiles[`../../assets/practice/${file}`];
  if (!mod) throw new Error(`Photo "${file}" is listed but missing from assets/practice`);
  return mod.default;
}

const patientFiles = import.meta.glob<{ default: ImageMetadata }>('../../assets/patients/*.jpg', { eager: true });

/** Patient and event photos the owner cleared for publication (2026-09-29, P-01 to P-26); each must be listed in assets/patients/photos.json. */
export function patientPhoto(file: string): ImageMetadata {
  if (!(patients as { file: string }[]).some((p) => p.file === file)) throw new Error(`Photo "${file}" is not listed in assets/patients/photos.json`);
  const mod = patientFiles[`../../assets/patients/${file}`];
  if (!mod) throw new Error(`Photo "${file}" is listed but missing from assets/patients`);
  return mod.default;
}
