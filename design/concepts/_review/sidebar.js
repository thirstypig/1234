export function formatDate(iso) {
  return new Date(iso).toLocaleString();
}

function clampPercent(value) {
  return Math.min(100, Math.max(0, value));
}

export function positionFromClick({ pageX, pageY, fullWidth, fullHeight }) {
  return {
    xPercent: clampPercent(Math.round((pageX / fullWidth) * 100)),
    yPercent: clampPercent(Math.round((pageY / fullHeight) * 100)),
  };
}

export function renderPins(container, comments, onPinClick) {
  container.innerHTML = '';
  for (const comment of comments) {
    if (comment.xPercent === undefined || comment.yPercent === undefined) continue;
    const pin = document.createElement('div');
    pin.className = 'review-pin';
    pin.title = `${comment.text} — ${formatDate(comment.createdAt)}`;
    pin.style.cssText = `position:absolute;left:${comment.xPercent}%;top:${comment.yPercent}%;width:20px;height:20px;border-radius:50% 50% 50% 0;background:#e0524d;transform:translate(-50%,-100%) rotate(-45deg);border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.4);cursor:pointer;z-index:9997;pointer-events:auto;`;
    if (onPinClick) {
      pin.addEventListener('click', () => onPinClick(comment));
    }
    container.appendChild(pin);
  }
}

export function createPinComposer({ xPercent, yPercent }, { onSubmit, onCancel }) {
  const composer = document.createElement('div');
  composer.className = 'review-pin-composer';
  composer.style.cssText = `position:absolute;left:${xPercent}%;top:${yPercent}%;transform:translate(-10px,10px);background:#fff;border:1px solid #ccc;border-radius:6px;padding:10px;box-shadow:0 2px 8px rgba(0,0,0,0.3);z-index:10000;width:220px;font-family:sans-serif;pointer-events:auto;`;

  const textarea = document.createElement('textarea');
  textarea.style.cssText = 'width:100%;height:60px;box-sizing:border-box;';
  textarea.placeholder = 'Comment for this spot...';

  const saveButton = document.createElement('button');
  saveButton.className = 'review-pin-composer-save';
  saveButton.textContent = 'Save';
  saveButton.style.cssText = 'margin-top:6px;';
  saveButton.addEventListener('click', () => {
    const text = textarea.value.trim();
    if (!text) return;
    onSubmit(text);
  });

  const cancelButton = document.createElement('button');
  cancelButton.className = 'review-pin-composer-cancel';
  cancelButton.textContent = 'Cancel';
  cancelButton.style.cssText = 'margin-top:6px;margin-left:6px;';
  cancelButton.addEventListener('click', () => onCancel());

  composer.append(textarea, saveButton, cancelButton);
  return composer;
}

export function createPinViewer(comment, { onClose }) {
  const viewer = document.createElement('div');
  viewer.className = 'review-pin-viewer';
  viewer.style.cssText = `position:absolute;left:${comment.xPercent}%;top:${comment.yPercent}%;transform:translate(-10px,10px);background:#fff;border:1px solid #ccc;border-radius:6px;padding:10px;box-shadow:0 2px 8px rgba(0,0,0,0.3);z-index:10000;width:220px;font-family:sans-serif;pointer-events:auto;`;

  const date = document.createElement('div');
  date.style.cssText = 'font-size:12px;color:#777;';
  date.textContent = formatDate(comment.createdAt);

  const text = document.createElement('div');
  text.style.cssText = 'margin-top:4px;';
  text.textContent = comment.text;

  const closeButton = document.createElement('button');
  closeButton.className = 'review-pin-viewer-close';
  closeButton.textContent = 'Close';
  closeButton.style.cssText = 'margin-top:6px;';
  closeButton.addEventListener('click', () => onClose());

  viewer.append(date, text, closeButton);
  return viewer;
}

export function renderSidebar(container, comments) {
  container.innerHTML = '';
  if (comments.length === 0) {
    const empty = document.createElement('p');
    empty.textContent = 'No comments yet.';
    container.appendChild(empty);
    return;
  }
  for (const comment of comments) {
    const item = document.createElement('div');
    item.className = 'review-comment';
    const date = document.createElement('div');
    date.className = 'review-comment-date';
    date.textContent = formatDate(comment.createdAt);
    if (comment.xPercent !== undefined && comment.yPercent !== undefined) {
      const badge = document.createElement('span');
      badge.className = 'review-comment-pin-badge';
      badge.textContent = ' 📍 pinned';
      date.appendChild(badge);
    }
    const text = document.createElement('div');
    text.className = 'review-comment-text';
    text.textContent = comment.text;
    item.appendChild(date);
    item.appendChild(text);
    container.appendChild(item);
  }
}
