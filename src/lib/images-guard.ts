export interface Entry {
  file: string;
  tag: string | null;
  approved: boolean;
}

/** Throws unless the image is a practice photo or has been explicitly approved. */
export function assertUsable(file: string, catalog: Entry[]): void {
  const e = catalog.find((c) => c.file === file);
  if (!e) throw new Error(`Image "${file}" is not in the legacy catalog`);
  if (e.tag !== 'practice-photo' && !e.approved) {
    throw new Error(`Image "${file}" is tagged ${e.tag} and not approved — set approved:true in assets/legacy/catalog.json after sign-off`);
  }
}
