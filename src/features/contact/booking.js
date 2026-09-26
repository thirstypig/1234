// Booking request form: posts to the review Worker, shows inline status (never alert()).
const API = 'https://1234-review-comments.jimmyc316.workers.dev'; // same Worker as inject.js API_BASE

const form = document.querySelector('[data-booking]');
if (form) {
  const btn = form.querySelector('[type=submit]');
  const btnLabel = btn.querySelector('span');
  const idleLabel = btnLabel.textContent;
  const status = form.querySelector('[role=status]');
  const alertBox = form.querySelector('[role=alert]');
  let sending = false;

  form.querySelectorAll('.ui-radio input').forEach((input) => {
    input.addEventListener('change', () => {
      form.querySelectorAll('.ui-radio').forEach((l) => l.classList.toggle('is-checked', l.querySelector('input').checked));
    });
  });

  const clearErrors = () => {
    form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
    form.querySelectorAll('.ui-field.is-error').forEach((el) => el.classList.remove('is-error'));
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (sending) return;
    sending = true;
    btn.disabled = true;
    btnLabel.textContent = form.dataset.sending;
    alertBox.hidden = true;
    status.textContent = '';
    clearErrors();
    const data = Object.fromEntries(new FormData(form));
    try {
      const res = await fetch(`${API}/booking`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const body = await res.json().catch(() => ({}));
      if (res.ok) {
        form.reset();
        form.querySelectorAll('.ui-radio').forEach((l) => l.classList.toggle('is-checked', l.querySelector('input').checked));
        status.textContent = form.dataset.success;
        return;
      }
      (body.fields || []).forEach((f) => {
        const el = form.querySelector(`[name="${f}"]`);
        el?.setAttribute('aria-invalid', 'true');
        el?.closest('.ui-field')?.classList.add('is-error');
      });
      const msg = res.status === 400 ? 'invalid' : res.status === 429 ? 'ratelimited' : 'network';
      alertBox.querySelector('span').textContent = form.dataset[msg];
      alertBox.hidden = false;
    } catch {
      alertBox.querySelector('span').textContent = form.dataset.network;
      alertBox.hidden = false;
    } finally {
      sending = false;
      btn.disabled = false;
      btnLabel.textContent = idleLabel;
    }
  });
}
