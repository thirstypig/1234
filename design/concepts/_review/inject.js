import { installGate } from './gate.js';
import { renderSidebar } from './sidebar.js';

const API_BASE = 'https://1234-review-comments.pasadenaworks.workers.dev';

function currentConceptAndPage() {
  const match = window.location.pathname.match(/\/concepts\/([A-E][^/]*)\/preview\/([^/]+)\//);
  return match ? { concept: match[1], page: match[2] } : { concept: 'unknown', page: 'unknown' };
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

async function submitComment(concept, page, text) {
  try {
    await fetch(`${API_BASE}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concept, page, text }),
    });
  } catch {
    // Network/backend unavailable — comment is silently dropped rather than
    // breaking the review page for the person leaving feedback.
  }
}

function buildSidebarShell() {
  const aside = document.createElement('aside');
  aside.id = 'review-sidebar';
  aside.style.cssText = 'position:fixed;top:0;right:0;width:320px;height:100vh;overflow-y:auto;background:#fafafa;border-left:1px solid #ddd;padding:16px;box-sizing:border-box;font-family:sans-serif;z-index:9998;';

  const heading = document.createElement('h3');
  heading.textContent = 'Feedback';
  const list = document.createElement('div');
  list.id = 'review-comment-list';
  const textarea = document.createElement('textarea');
  textarea.id = 'review-comment-input';
  textarea.style.cssText = 'width:100%;height:80px;margin-top:12px;';
  const submit = document.createElement('button');
  submit.id = 'review-comment-submit';
  submit.style.cssText = 'margin-top:8px;';
  submit.textContent = 'Add comment';

  aside.append(heading, list, textarea, submit);
  document.body.appendChild(aside);
  return aside;
}

async function init() {
  installGate(document);
  const { concept, page } = currentConceptAndPage();
  const aside = buildSidebarShell();
  const list = aside.querySelector('#review-comment-list');

  const refresh = async () => renderSidebar(list, await loadComments(concept, page));
  await refresh();

  aside.querySelector('#review-comment-submit').addEventListener('click', async () => {
    const input = aside.querySelector('#review-comment-input');
    if (!input.value.trim()) return;
    await submitComment(concept, page, input.value);
    input.value = '';
    await refresh();
  });
}

init();
