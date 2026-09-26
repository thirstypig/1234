const RULES = [
  ['statistic', /\d+(\.\d+)?\s*%|\bpercent\b/i],
  ['success-rate', /success\s+rate|effective(ness)?\s+rate|\bcure[sd]?\b/i],
  ['superlative', /\b(best|finest|first|most\s+\w+|leading|top|#\s?1|number\s+one|premier|unmatched)\b/i],
  ['patient-count', /\b\d[\d,]*\+?\s+(patients|children|kids|families|cases|eyes)\b|\b(thousands|hundreds)\s+of\s+(patients|children|families)/i],
  ['guarantee', /\bguarantee[sd]?\b|\bpermanent(ly)?\b|\b100\s*%/i],
  ['number', /\d/],
];

export function flagClaims(sentence) {
  return RULES.filter(([, re]) => re.test(sentence)).map(([name]) => name);
}

const TITLES = /\b(Dr|Mr|Mrs|Ms|St|Ave|Blvd|No)\.$/;

export function splitSentences(text) {
  const out = [];
  for (const line of text.split('\n')) {
    let buf = '';
    for (const part of line.split(/(?<=[.!?])\s+/)) {
      buf = buf ? `${buf} ${part}` : part;
      if (!TITLES.test(buf)) { out.push(buf); buf = ''; }
    }
    if (buf) out.push(buf);
  }
  return out.map((s) => s.replace(/\s+/g, ' ').trim()).filter(Boolean);
}
