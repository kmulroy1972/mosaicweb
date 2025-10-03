(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('is-open');
    });
  }

  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.dataset.reveal = 'visible';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 }) : null;

  document.querySelectorAll('[data-reveal]').forEach(el => {
    if (observer) {
      observer.observe(el);
    } else {
      el.dataset.reveal = 'visible';
    }
  });
})();
