/* ============================================================
   Portfólio Paulo Ambrosi — comportamento
   Vanilla, sem dependências. Cada módulo sai silenciosamente
   se os elementos que ele controla não existirem na página.
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---------- Tema ---------- */
  (function theme() {
    var btn = $('#theme-toggle');
    if (!btn) return;

    function stored() {
      try { return localStorage.getItem('pa-theme'); } catch (e) { return null; }
    }
    function persist(value) {
      try { localStorage.setItem('pa-theme', value); } catch (e) { /* modo privado */ }
    }
    function isDark() {
      var attr = root.getAttribute('data-theme');
      if (attr) return attr === 'dark';
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    function sync() {
      btn.setAttribute('aria-pressed', String(isDark()));
    }

    if (stored()) root.setAttribute('data-theme', stored());
    sync();

    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      persist(next);
      sync();
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      if (!stored()) sync();
    });
  }());

  /* ---------- Menu mobile ---------- */
  (function mobileNav() {
    var toggle = $('#nav-toggle');
    var nav = $('#nav');
    if (!toggle || !nav) return;

    function open() {
      nav.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Fechar menu de navegação');
      document.addEventListener('keydown', onKey);
      document.addEventListener('click', onOutside, true);
    }
    function close(refocus) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Abrir menu de navegação');
      document.removeEventListener('keydown', onKey);
      document.removeEventListener('click', onOutside, true);
      if (refocus) toggle.focus();
    }
    function isOpen() { return nav.classList.contains('is-open'); }

    function onKey(e) {
      if (e.key === 'Escape') { close(true); return; }
      if (e.key !== 'Tab') return;
      var items = [toggle].concat($$('a', nav));
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    function onOutside(e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) close(false);
    }

    toggle.addEventListener('click', function () { isOpen() ? close(false) : open(); });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && isOpen()) close(false);
    });
    window.matchMedia('(min-width: 769px)').addEventListener('change', function (e) {
      if (e.matches && isOpen()) close(false);
    });
  }());

  /* ---------- Sombra do header ao rolar ---------- */
  (function stickyHeader() {
    var header = $('#header');
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle('is-stuck', window.scrollY > 8);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }());

  /* ---------- Scrollspy ---------- */
  (function scrollspy() {
    var links = $$('.nav__link[href^="#"], .toc a[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;

    var map = {};
    var targets = [];
    links.forEach(function (link) {
      var id = link.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (!el) return;
      map[id] = (map[id] || []).concat(link);
      targets.push(el);
    });
    if (!targets.length) return;

    var visible = new Set();
    function paint() {
      var current = targets.filter(function (t) { return visible.has(t.id); })[0];
      links.forEach(function (l) { l.removeAttribute('aria-current'); });
      if (current && map[current.id]) {
        map[current.id].forEach(function (l) { l.setAttribute('aria-current', 'true'); });
      }
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) visible.add(en.target.id);
        else visible.delete(en.target.id);
      });
      paint();
    }, { rootMargin: '-72px 0px -62% 0px', threshold: 0 });

    targets.forEach(function (t) { io.observe(t); });
  }());

  /* ---------- Reveal ao rolar ---------- */
  (function reveal() {
    var items = $$('[data-reveal]');
    if (!items.length) return;

    if (reduced.matches || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-visible');
        obs.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

    items.forEach(function (el) { io.observe(el); });
  }());

  /* ---------- Contadores ---------- */
  (function counters() {
    var nums = $$('[data-count]');
    if (!nums.length) return;

    function render(el, value) {
      var prefix = el.getAttribute('data-prefix') || '';
      var suffix = el.getAttribute('data-suffix') || '';
      el.textContent = prefix + value + suffix;
    }

    function run(el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      if (isNaN(target)) return;
      if (reduced.matches) { render(el, target); return; }

      var duration = 1100;
      var start = null;
      function step(ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        render(el, Math.round(target * eased));
        if (p < 1) window.requestAnimationFrame(step);
      }
      render(el, 0);
      window.requestAnimationFrame(step);
    }

    if (!('IntersectionObserver' in window)) { nums.forEach(function (el) { run(el); }); return; }

    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        obs.unobserve(en.target);
      });
    }, { threshold: 0.4 });

    nums.forEach(function (el) { io.observe(el); });
  }());

  /* ---------- Filtro de habilidades ---------- */
  (function skillFilter() {
    var group = $('[data-filter-group]');
    var chips = $$('#chips .chip');
    var status = $('#filter-count');
    if (!group || !chips.length) return;

    var buttons = $$('[data-filter]', group);
    var total = chips.length;

    function say(shown, label) {
      if (!status) return;
      status.textContent = shown === total
        ? total + ' habilidades'
        : shown + ' de ' + total + ' habilidades · ' + label;
    }

    function apply(key, label) {
      var shown = 0;
      chips.forEach(function (chip) {
        var tags = (chip.getAttribute('data-tags') || '').split(/\s+/);
        var match = key === 'all' || tags.indexOf(key) !== -1;
        if (match) shown++;

        if (reduced.matches) {
          chip.hidden = !match;
          chip.classList.toggle('is-dimmed', false);
          return;
        }

        if (match) {
          chip.hidden = false;
          window.requestAnimationFrame(function () { chip.classList.remove('is-dimmed'); });
        } else {
          chip.classList.add('is-dimmed');
          window.setTimeout(function () {
            if (chip.classList.contains('is-dimmed')) chip.hidden = true;
          }, 280);
        }
      });
      say(shown, label);
    }

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        apply(btn.getAttribute('data-filter'), btn.textContent.trim());
      });
    });

    say(total, '');
  }());

  /* ---------- Ano no rodapé ---------- */
  (function year() {
    var el = $('#year');
    if (el) el.textContent = String(new Date().getFullYear());
  }());
}());
