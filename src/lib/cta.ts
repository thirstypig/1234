import { pathFor, type Lang } from '../i18n/locales';

// The booking form is hidden until requests reach the office through a service
// covered by a BAA (owner, 2026-11-07, N-24). While it is off, every "Book" link
// goes to the Call section of the contact page. Turning it back on restores the
// form, its tests (tests/e2e/booking.spec.ts) and the "Book online" links.
export const BOOKING_FORM_ENABLED = false;

export const bookHref = (lang: Lang) => `${pathFor(lang, 'contact')}${BOOKING_FORM_ENABLED ? '#book' : '#call'}`;

// Message goes to a phone call until the client confirms the office number accepts texts (then sms:).
export const MESSAGE_HREF = 'tel:+18009918881';
