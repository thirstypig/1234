import { pathFor, type Lang } from '../i18n/locales';

export const bookHref = (lang: Lang) => `${pathFor(lang, 'contact')}#book`;

// Message goes to a phone call until the client confirms the office number accepts texts (then sms:).
export const MESSAGE_HREF = 'tel:+18009918881';
