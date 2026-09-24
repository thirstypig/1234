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
