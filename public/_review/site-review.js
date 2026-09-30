// Review overlay for the Concept C preview site: the password gate plus a collapsible
// feedback sidebar with page pins. Reuses the concept mockups' gate and sidebar helpers,
// which scripts/assemble.sh copies into /_review/ next to this file. Comments go to the
// same Worker as the mockups (workers/comments/), keyed by commentKeyFor().
import { installGate } from './gate.js';
import { renderSidebar, renderPins, positionFromClick, createPinComposer, createPinViewer } from './sidebar.js';
import { commentKeyFor } from './site-key.js';

const API_BASE = 'https://1234-review-comments.jimmyc316.workers.dev';
const OPEN_KEY = '1234-review-sidebar-open';

async function loadComments({ concept, page }) {
  try {
    const res = await fetch(`${API_BASE}/comments?concept=${encodeURIComponent(concept)}&page=${encodeURIComponent(page)}`);
    if (!res.ok) return [];
    return (await res.json()).comments ?? [];
  } catch {
    return [];
  }
}

async function submitComment({ concept, page }, text, position) {
  try {
    await fetch(`${API_BASE}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concept, page, text, ...position }),
    });
  } catch {
    // Backend unavailable: drop the comment rather than break the page for the reviewer.
  }
}

function readOpen() {
  try { return localStorage.getItem(OPEN_KEY) === 'true'; } catch { return false; }
}
function writeOpen(open) {
  try { localStorage.setItem(OPEN_KEY, String(open)); } catch { /* private mode */ }
}

function buildToggle() {
  const toggle = document.createElement('button');
  toggle.id = 'review-sidebar-toggle';
  toggle.type = 'button';
  toggle.textContent = 'Feedback';
  toggle.setAttribute('aria-controls', 'review-sidebar');
  // Vertical tab on the right edge, mid-height: clear of the header and of the mobile sticky Book bar.
  toggle.style.cssText = 'position:fixed;right:0;top:50%;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;padding:14px 8px;background:#5b2a86;color:#fff;border:0;border-radius:0 8px 8px 0;font:600 14px/1 sans-serif;letter-spacing:.05em;cursor:pointer;z-index:9998;box-shadow:0 2px 8px rgba(0,0,0,.3);';
  document.body.appendChild(toggle);
  return toggle;
}

function buildSidebarShell() {
  const aside = document.createElement('aside');
  aside.id = 'review-sidebar';
  aside.setAttribute('aria-label', 'Review feedback');
  aside.style.cssText = 'position:fixed;top:0;right:0;width:min(340px,100vw);height:100vh;overflow-y:auto;background:#fafafa;color:#222;border-left:1px solid #ccc;padding:16px;box-sizing:border-box;font:15px/1.5 sans-serif;z-index:9999;box-shadow:-2px 0 12px rgba(0,0,0,.15);';

  aside.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
      <p style="margin:0;font-weight:700;font-size:17px;">Feedback on this page</p>
      <button type="button" id="review-sidebar-close" aria-label="Close feedback">✕</button>
    </div>
    <p style="font-size:13px;color:#444;background:#fff;border:1px solid #ddd;border-radius:6px;padding:10px;">
      Comment on <strong>this page</strong>: wording, photos, layout, anything that looks wrong.
      Use <strong>Pin on page</strong> to point at a spot. Everyone reviewing the site
      can see comments, and they are timestamped automatically.
    </p>
    <div id="review-comment-list"></div>
    <label for="review-comment-input" style="display:block;margin-top:12px;font-weight:600;">Your comment</label>
    <textarea id="review-comment-input" style="width:100%;height:90px;box-sizing:border-box;font:inherit;"></textarea>
    <button type="button" id="review-comment-submit" style="margin-top:8px;">Add comment</button>
    <button type="button" id="review-pin-button" style="margin-top:8px;margin-left:8px;">Pin on page</button>
    <p id="review-pin-hint" style="display:none;font-size:13px;color:#5b2a86;">Click anywhere on the page to place your pin (Esc to cancel).</p>
  `;
  document.body.appendChild(aside);
  return aside;
}

function buildPinLayer() {
  const layer = document.createElement('div');
  layer.id = 'review-pin-layer';
  layer.style.cssText = 'position:absolute;top:0;left:0;width:100%;pointer-events:none;z-index:9996;';
  document.body.appendChild(layer);
  return layer;
}

function enablePinPlacementMode(aside, onPick) {
  const hint = aside.querySelector('#review-pin-hint');
  hint.style.display = 'block';
  document.body.style.cursor = 'crosshair';
  const stop = () => {
    hint.style.display = 'none';
    document.body.style.cursor = '';
    document.removeEventListener('click', onClick, true);
    document.removeEventListener('keydown', onKey, true);
  };
  const onClick = (event) => {
    if (aside.contains(event.target)) return; // clicks inside the sidebar don't place pins
    // Capture phase, and cancel the click: on the real site it would otherwise follow a link.
    event.preventDefault();
    event.stopPropagation();
    stop();
    onPick(event);
  };
  const onKey = (event) => { if (event.key === 'Escape') stop(); };
  document.addEventListener('click', onClick, true);
  document.addEventListener('keydown', onKey, true);
}

async function init() {
  installGate(document);

  const key = commentKeyFor(window.location.pathname);
  const toggle = buildToggle();
  const aside = buildSidebarShell();
  const list = aside.querySelector('#review-comment-list');
  const pinLayer = buildPinLayer();

  const setOpen = (open) => {
    aside.hidden = !open;
    toggle.hidden = open;
    toggle.setAttribute('aria-expanded', String(open));
    writeOpen(open);
  };
  setOpen(readOpen());
  toggle.addEventListener('click', () => setOpen(true));
  aside.querySelector('#review-sidebar-close').addEventListener('click', () => setOpen(false));

  let openOverlay = null;
  const closeOverlay = () => { openOverlay?.remove(); openOverlay = null; };

  const refresh = async () => {
    const comments = await loadComments(key);
    // Images load lazily, so size the pin layer to the page each time it's redrawn.
    pinLayer.style.height = `${document.documentElement.scrollHeight}px`;
    renderSidebar(list, comments);
    renderPins(pinLayer, comments, (comment) => {
      closeOverlay();
      openOverlay = createPinViewer(comment, { onClose: closeOverlay });
      pinLayer.appendChild(openOverlay);
    });
    toggle.textContent = comments.length ? `Feedback (${comments.length})` : 'Feedback';
  };
  await refresh();

  aside.querySelector('#review-comment-submit').addEventListener('click', async () => {
    const input = aside.querySelector('#review-comment-input');
    if (!input.value.trim()) return;
    await submitComment(key, input.value);
    input.value = '';
    await refresh();
  });

  aside.querySelector('#review-pin-button').addEventListener('click', () => {
    enablePinPlacementMode(aside, (event) => {
      closeOverlay();
      const position = positionFromClick({
        pageX: event.pageX,
        pageY: event.pageY,
        fullWidth: document.documentElement.scrollWidth,
        fullHeight: document.documentElement.scrollHeight,
      });
      openOverlay = createPinComposer(position, {
        onSubmit: async (text) => {
          closeOverlay();
          await submitComment(key, text, position);
          await refresh();
        },
        onCancel: closeOverlay,
      });
      pinLayer.appendChild(openOverlay);
    });
  });
}

init();
