const filterButtons = document.querySelectorAll('[data-filter]');
const cards = document.querySelectorAll('[data-category]');
const counter = document.querySelector('.project-counter');
filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    filterButtons.forEach(item => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    let visible = 0;
    cards.forEach(card => {
      card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter;
      if (!card.hidden) visible++;
    });
    counter.textContent = `${visible} ${visible === 1 ? 'projeto' : 'projetos'}`;
  });
});

// Content stays readable without JavaScript or when motion is disabled.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const sections = [...document.querySelectorAll('main section[id]')];
const chapterLinks = [...document.querySelectorAll('.chapter-nav a, .header nav a')];
const timeline = document.querySelector('.timeline');
const hero = document.querySelector('.hero');
const root = document.documentElement;

if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const reveal = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const element = entry.target;
      if (typeof element.animate === 'function' && !reducedMotion.matches) {
        const siblings = [...element.parentElement.children];
        const delay = element.matches('.project-card, .skill-group')
          ? (siblings.indexOf(element) % 3) * 90 : 0;
        element.animate([
          { opacity: 0, transform: 'translateY(38px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], { duration: 750, delay, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
      }
      reveal.unobserve(element);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  document.querySelectorAll('.hero-content, .section-heading, .about-copy, .project-card, .case, .skill-group, .experience, .education, .contact-grid > div')
    .forEach(element => reveal.observe(element));
}

let framePending = false;
function updateScrollScene() {
  framePending = false;
  const scrollable = root.scrollHeight - window.innerHeight;
  root.style.setProperty('--scroll-progress', scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0);
  document.body.classList.toggle('is-scrolled', window.scrollY > 40);
  const marker = window.innerHeight * 0.4;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= marker) current = section;
  }
  chapterLinks.forEach(link => {
    if (link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  if (timeline) {
    const rect = timeline.getBoundingClientRect();
    root.style.setProperty('--journey', Math.max(0, Math.min(1, (window.innerHeight * 0.65 - rect.top) / rect.height)));
  }
  if (!reducedMotion.matches && window.innerWidth > 740 && hero) {
    const distance = Math.max(0, Math.min(hero.offsetHeight, -hero.getBoundingClientRect().top));
    root.style.setProperty('--hero-shift', `${distance * 0.075}px`);
    root.style.setProperty('--hero-turn', `${distance * 0.002}deg`);
  } else {
    root.style.setProperty('--hero-shift', '0px');
    root.style.setProperty('--hero-turn', '0deg');
  }
}
function queueSceneUpdate() {
  if (!framePending) {
    framePending = true;
    window.requestAnimationFrame(updateScrollScene);
  }
}
window.addEventListener('scroll', queueSceneUpdate, { passive: true });
window.addEventListener('resize', queueSceneUpdate);
reducedMotion.addEventListener('change', () => {
  if (reducedMotion.matches) document.getAnimations().forEach(animation => animation.cancel());
  queueSceneUpdate();
});
document.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', queueSceneUpdate));
filterButtons.forEach(button => button.addEventListener('click', queueSceneUpdate));
window.addEventListener('load', queueSceneUpdate);
queueSceneUpdate();
