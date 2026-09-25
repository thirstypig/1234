import { installGate } from './gate.js';
import { renderSidebar, renderPins, positionFromClick, createPinComposer, createPinViewer } from './sidebar.js';

const API_BASE = 'https://1234-review-comments.jimmyc316.workers.dev';

function currentConceptAndPage() {
  const previewMatch = window.location.pathname.match(/\/concepts\/([A-E][^/]*)\/preview\/([^/]+)\//);
  if (previewMatch) return { concept: previewMatch[1], page: previewMatch[2] };

  const homepageMatch = window.location.pathname.match(/\/concepts\/([A-E][^/]*)\/Concept[^/]*-homepage-([^/.]+)\.html/);
  if (homepageMatch) return { concept: homepageMatch[1], page: `homepage-${homepageMatch[2]}` };

  return { concept: 'unknown', page: 'unknown' };
}

async function loadComments(concept, page) {
  try {
    const res = await fetch(`${API_BASE}/comments?concept=${encodeURIComponent(concept)}&page=${encodeURIComponent(page)}`);
    if (!res.ok) return [];
    const body = await res.json();
    return body.comments ?? [];
  } catch {
    return [];
  }
}

async function submitComment(concept, page, text, position) {
  try {
    await fetch(`${API_BASE}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concept, page, text, ...position }),
    });
  } catch {
    // Network/backend unavailable — comment is silently dropped rather than
    // breaking the review page for the person leaving feedback.
  }
}

function buildPinLayer() {
  const layer = document.createElement('div');
  layer.id = 'review-pin-layer';
  layer.style.cssText = `position:absolute;top:0;left:0;width:100%;height:${document.documentElement.scrollHeight}px;pointer-events:none;z-index:9996;`;
  document.body.appendChild(layer);
  return layer;
}

function buildSidebarShell() {
  const aside = document.createElement('aside');
  aside.id = 'review-sidebar';
  aside.style.cssText = 'position:fixed;top:0;right:0;width:320px;height:100vh;overflow-y:auto;background:#fafafa;border-left:1px solid #ddd;padding:16px;box-sizing:border-box;font-family:sans-serif;z-index:9998;';

  const heading = document.createElement('h3');
  heading.textContent = 'Leave feedback on this homepage';
  heading.style.cssText = 'margin-top:0;';

  const instructions = document.createElement('p');
  instructions.style.cssText = 'font-size:13px;color:#555;line-height:1.5;background:#fff;border:1px solid #ddd;border-radius:6px;padding:10px;';
  instructions.innerHTML =
    'Comment here on <strong>this concept\'s look and feel</strong> — colors, ' +
    'layout, tone, imagery, whether it feels right for the practice. ' +
    'Be as specific as you can (e.g. "the hero photo feels too clinical" ' +
    'rather than just "not a fan"). Comments are visible to everyone ' +
    'reviewing this page and are timestamped automatically.';

  const list = document.createElement('div');
  list.id = 'review-comment-list';
  const textarea = document.createElement('textarea');
  textarea.id = 'review-comment-input';
  textarea.placeholder = 'What do you think of this concept?';
  textarea.style.cssText = 'width:100%;height:80px;margin-top:12px;box-sizing:border-box;';
  const submit = document.createElement('button');
  submit.id = 'review-comment-submit';
  submit.style.cssText = 'margin-top:8px;';
  submit.textContent = 'Add comment';

  const pinButton = document.createElement('button');
  pinButton.id = 'review-pin-button';
  pinButton.style.cssText = 'margin-top:8px;margin-left:8px;';
  pinButton.textContent = 'Pin on page instead';
  pinButton.title = 'Click, then click anywhere on the page to attach your comment to that spot';

  aside.append(heading, instructions, list, textarea, submit, pinButton);
  document.body.appendChild(aside);
  return aside;
}

function enablePinPlacementMode(onPick) {
  document.body.style.cursor = 'crosshair';
  const handler = (event) => {
    document.body.style.cursor = '';
    document.removeEventListener('click', handler, true);
    onPick(event);
  };
  // Capture phase so this fires before any click handler on the page's own content.
  document.addEventListener('click', handler, true);
}

async function init() {
  installGate(document);
  const { concept, page } = currentConceptAndPage();
  const aside = buildSidebarShell();
  const list = aside.querySelector('#review-comment-list');
  const pinLayer = buildPinLayer();

  let comments = [];
  let openOverlay = null;

  const closeOverlay = () => {
    if (openOverlay) {
      openOverlay.remove();
      openOverlay = null;
    }
  };

  const refresh = async () => {
    comments = await loadComments(concept, page);
    renderSidebar(list, comments);
    renderPins(pinLayer, comments, (comment) => {
      closeOverlay();
      openOverlay = createPinViewer(comment, { onClose: closeOverlay });
      pinLayer.appendChild(openOverlay);
    });
  };
  await refresh();

  aside.querySelector('#review-comment-submit').addEventListener('click', async () => {
    const input = aside.querySelector('#review-comment-input');
    if (!input.value.trim()) return;
    await submitComment(concept, page, input.value);
    input.value = '';
    await refresh();
  });

  aside.querySelector('#review-pin-button').addEventListener('click', () => {
    enablePinPlacementMode((event) => {
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
          await submitComment(concept, page, text, position);
          await refresh();
        },
        onCancel: closeOverlay,
      });
      pinLayer.appendChild(openOverlay);
    });
  });
}

init();
