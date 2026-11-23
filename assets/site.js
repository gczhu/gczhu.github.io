(() => {
  const root = document.documentElement;
  const switcher = document.querySelector('.view-switch');
  const buttons = Array.from(document.querySelectorAll('[data-view-button]'));
  const papers = Array.from(document.querySelectorAll('.paper'));
  const status = document.getElementById('view-status');
  const heading = document.getElementById('publications-heading');
  function setView(view, announce = false) {
    root.dataset.view = view;
    heading.textContent = view === 'all' ? 'All publications' : 'Selected publications';
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.viewButton === view));
    if (announce) {
      const count = view === 'all' ? papers.length : papers.filter(p => p.dataset.selected === 'true').length;
      status.textContent = `Showing ${count} ${view === 'all' ? 'publications' : 'selected publications'}.`;
    }
  }
  switcher.hidden = false;
  for (const button of buttons) button.addEventListener('click', () => setView(button.dataset.viewButton, true));
  // Direct links to an unselected paper should reveal it.
  function revealAnchor() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.matches('.paper[data-selected="false"]')) {
      setView('all');
      target.scrollIntoView();
    }
  }
  setView('selected');
  revealAnchor();
  window.addEventListener('hashchange', revealAnchor);
  if (navigator.clipboard && window.isSecureContext) {
    for (const button of document.querySelectorAll('.copy-citation')) {
      button.hidden = false;
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);
          button.textContent = 'Copied';
        } catch {
          button.textContent = 'Please select and copy the text';
        }
        window.setTimeout(() => { button.textContent = 'Copy citation'; }, 2500);
      });
    }
  }
})();
