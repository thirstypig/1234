export function formatDate(iso) {
  return new Date(iso).toLocaleString();
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
    const text = document.createElement('div');
    text.className = 'review-comment-text';
    text.textContent = comment.text;
    item.appendChild(date);
    item.appendChild(text);
    container.appendChild(item);
  }
}
