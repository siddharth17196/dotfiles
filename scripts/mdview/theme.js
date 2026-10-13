(() => {
  const system = window.matchMedia('(prefers-color-scheme: dark)');

  function apply(theme) {
    document.documentElement.dataset.theme = theme;
    window.dispatchEvent(new Event('mdview-theme-change'));
  }

  function sync() {
    let saved;
    try { saved = localStorage.getItem('mdview-theme'); } catch (_) {}
    apply(saved === 'light' || saved === 'dark' ? saved : system.matches ? 'dark' : 'light');
  }

  window.mdviewTheme = {
    apply,
    toggle() {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('mdview-theme', theme); } catch (_) {}
      apply(theme);
    }
  };
  window.addEventListener('storage', event => { if (event.key === 'mdview-theme') sync(); });
  system.addEventListener('change', sync);
  sync();
})();
