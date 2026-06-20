async function loadFeed() {
  const target = document.querySelector('#feed-list');
  try {
    const response = await fetch('feed.json', { cache: 'no-store' });
    const feed = await response.json();
    target.innerHTML = feed.items.map(item => `
      <article class="feed-item">
        <time>${new Date(item.ts).toLocaleString()}</time>
        <p>${escapeHtml(item.text)}</p>
      </article>
    `).join('');
  } catch (error) {
    target.textContent = 'The chapel feed is quiet. Try again soon.';
  }
}
function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}
document.querySelectorAll('.copy-box').forEach(box => {
  const button = box.querySelector('button');
  button.addEventListener('click', async () => {
    await navigator.clipboard.writeText(box.dataset.copy);
    button.textContent = 'Copied';
    setTimeout(() => button.textContent = 'Copy', 1200);
  });
});
loadFeed();
