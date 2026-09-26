import approved from '../content/approved-claims.json';

/** Flagged old-site claims (docs/copy-review.md ids) render only after the client approves them. */
export function isApproved(id: string, list: string[] = approved as string[]): boolean {
  return list.includes(id);
}
