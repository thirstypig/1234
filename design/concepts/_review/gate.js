const STORAGE_KEY = '1234-review-unlocked';
const PASSPHRASE = 'purplelantern';

export function isUnlocked() {
  return localStorage.getItem(STORAGE_KEY) === 'true';
}

export function tryUnlock(phrase) {
  const normalized = phrase.trim().toLowerCase().replace(/\s+/g, '');
  if (normalized === PASSPHRASE) {
    localStorage.setItem(STORAGE_KEY, 'true');
    return true;
  }
  return false;
}

export function installGate(rootDocument) {
  if (isUnlocked()) return;

  const overlay = rootDocument.createElement('div');
  overlay.id = 'review-gate-overlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:#111;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;font-family:sans-serif;gap:12px;';
  overlay.innerHTML = `
    <p>Enter the review password</p>
    <input type="password" id="review-gate-input" style="padding:8px;font-size:16px;" />
    <button id="review-gate-submit" style="padding:8px 16px;">Enter</button>
    <p id="review-gate-error" style="color:#f88;display:none;">Incorrect password.</p>
  `;
  rootDocument.body.style.overflow = 'hidden';
  rootDocument.body.appendChild(overlay);

  const submit = () => {
    const input = rootDocument.getElementById('review-gate-input');
    if (tryUnlock(input.value)) {
      overlay.remove();
      rootDocument.body.style.overflow = '';
    } else {
      rootDocument.getElementById('review-gate-error').style.display = 'block';
    }
  };

  rootDocument.getElementById('review-gate-submit').addEventListener('click', submit);
  rootDocument.getElementById('review-gate-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') submit();
  });
}
