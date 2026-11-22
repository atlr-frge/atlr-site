(function () {
  var nav = document.getElementById('nav');
  var toggle = document.getElementById('navToggle');
  var body = document.body;

  function onScroll() {
    if (window.scrollY > 24) nav.classList.add('scrolled'); else nav.classList.remove('scrolled');
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (toggle) {
    // iOS Safari ignores overflow:hidden on body, so the open menu pins the body and restores the scroll position on close.
    var lockY = 0;
    function openMenu() {
      lockY = window.scrollY;
      body.style.top = -lockY + 'px';
      body.classList.add('menu-open');
      toggle.setAttribute('aria-expanded', 'true');
    }
    function closeMenu() {
      if (!body.classList.contains('menu-open')) return;
      body.classList.remove('menu-open');
      body.style.top = '';
      window.scrollTo(0, lockY);
      toggle.setAttribute('aria-expanded', 'false');
    }
    toggle.addEventListener('click', function () {
      if (body.classList.contains('menu-open')) closeMenu(); else openMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) { closeMenu(); toggle.focus(); }
    });
    document.querySelectorAll('#navLinks a').forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });
  }

  // Reveal on entry. Elements carry .reveal (or .stagger-children for a group).
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.reveal, .stagger-children');
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
  }

  // Terminal: types its lines once it is on screen, then loops.
  var term = document.getElementById('terminal-output');
  if (term && !reduce) {
    var lines = Array.prototype.slice.call(term.querySelectorAll('.t-line'));
    lines.forEach(function (l) { l.style.opacity = 0; });
    var started = false;
    function run() {
      var i = 0;
      function step() {
        if (i >= lines.length) { return; }
        lines[i].style.transition = 'opacity 0.25s'; lines[i].style.opacity = 1; i++;
        setTimeout(step, i === 1 ? 300 : 420);
      }
      step();
    }
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting && !started) { started = true; run(); tio.disconnect(); } });
    }, { threshold: 0.3 });
    tio.observe(term);
  }
  // Episode players: the cover stays clean until the first play.
  Array.prototype.forEach.call(document.querySelectorAll('.ep-frame video[controls]'), function (v) {
    v.removeAttribute('controls');
    var b = document.createElement('button'); b.type = 'button'; b.className = 'ep-play';
    b.setAttribute('aria-label', 'Play ' + (v.getAttribute('aria-label') || 'the episode'));
    v.parentNode.appendChild(b);
    b.addEventListener('click', function () { v.controls = true; b.remove(); v.play(); });
  });
})();
