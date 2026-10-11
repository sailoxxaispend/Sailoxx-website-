/* Sailoxx — site.js
   Shared behaviour. Every block checks that its markup exists, so this file is safe on any page. */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header: scrolled state, mobile menu ---------- */
  var header = $('.site-header');
  var menuBtn = $('.menu-btn');
  var menu = $('#mobile-menu');

  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 4); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  function setMenu(open) {
    if (!menuBtn || !menu) return;
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  }
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); menuBtn.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1100) setMenu(false); });
  }

  /* ---------- Products mega-menu (hover or focus on desktop, button toggles for keyboard and touch) ---------- */
  var megaItem = $('.has-mega');
  if (megaItem) {
    var megaBtn = $('.mega-toggle', megaItem), closeT = null, pinned = false;
    var canHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;
    var setMega = function (open) {
      if (!open) pinned = false;
      megaItem.classList.toggle('is-open', open);
      megaBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      megaBtn.setAttribute('aria-label', open ? 'Hide products menu' : 'Show products menu');
    };
    if (canHover) {
      megaItem.addEventListener('mouseenter', function () { clearTimeout(closeT); setMega(true); });
      megaItem.addEventListener('mouseleave', function () { if (pinned) return; closeT = setTimeout(function () { setMega(false); }, 160); });
    }
    megaBtn.addEventListener('click', function () {
      var open = megaItem.classList.contains('is-open');
      if (open && pinned) { setMega(false); }
      else { setMega(true); pinned = true; }
    });
    document.addEventListener('click', function (e) { if (!megaItem.contains(e.target)) setMega(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && megaItem.classList.contains('is-open')) { setMega(false); megaBtn.focus(); }
    });
    megaItem.addEventListener('focusout', function (e) { if (e.relatedTarget && !megaItem.contains(e.relatedTarget)) setMega(false); });
    window.addEventListener('scroll', function () { if (megaItem.classList.contains('is-open') && !megaItem.matches(':hover')) setMega(false); }, { passive: true });
  }

  /* ---------- Currency (INR / USD) ---------- */
  var currency = 'INR';
  function setCurrency(cur, remember) {
    currency = cur;
    if (remember) { try { localStorage.setItem('sx-currency', cur); } catch (e) {} }
    $$('[data-inr]').forEach(function (el) { el.textContent = cur === 'INR' ? el.getAttribute('data-inr') : el.getAttribute('data-usd'); });
    $$('.seg button[data-currency]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-currency') === cur ? 'true' : 'false'); });
    var note = $('#currency-note');
    if (note) note.textContent = cur === 'INR' ? 'Prices exclude applicable taxes.' : 'USD shown for international visitors. Prices exclude applicable taxes.';
  }
  if ($$('[data-inr]').length) {
    $$('.seg button[data-currency]').forEach(function (b) { b.addEventListener('click', function () { setCurrency(b.getAttribute('data-currency'), true); }); });
    var stored = null;
    try { stored = localStorage.getItem('sx-currency'); } catch (e) {}
    if (stored === 'INR' || stored === 'USD') { setCurrency(stored); } else try {
      var tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || '').toLowerCase();
      var inIndia = tz.indexOf('calcutta') > -1 || tz.indexOf('kolkata') > -1;
      setCurrency(inIndia || !tz ? 'INR' : 'USD');
    } catch (e) { setCurrency('INR'); }
  }

  /* ---------- Pricing tabs ---------- */
  var tablist = $('[role="tablist"]');
  if (tablist) {
    var tabs = $$('[role="tab"]', tablist);
    var activate = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { activate(t, false); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        else if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === 'Home') n = tabs[0];
        else if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); activate(n, true); }
      });
    });
  }

  /* ---------- Sample report coverflow ---------- */
  var cf = $('.cf');
  if (cf) {
    var cfStage = $('.cf-stage', cf), cfSlides = $$('.cf-slide', cf), n = cfSlides.length;
    var cfCount = $('#cf-count'), cfRange = $('#cf-range'), cfPlay = $('#cf-play');
    var cur = 0, timer = null, userPaused = false, hovering = false, inView = true;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var DELAY = 2800;
    var render = function () {
      cfSlides.forEach(function (s, i) {
        var d = ((i - cur) % n + n) % n; if (d > n / 2) d -= n;
        s.setAttribute('data-pos', Math.abs(d) <= 2 ? String(d) : 'x');
        s.setAttribute('aria-hidden', d === 0 ? 'false' : 'true');
        if (Math.abs(d) <= 2) { var img = $('img', s); if (img && img.loading === 'lazy') img.loading = 'eager'; }
      });
      if (cfCount) cfCount.textContent = (cur + 1) + ' of ' + n;
      if (cfRange) { cfRange.value = cur + 1; cfRange.style.setProperty('--fill', (cur / (n - 1) * 100).toFixed(1) + '%'); }
    };
    var go = function (k) { cur = (k % n + n) % n; render(); };
    var stop = function () { if (timer) { clearInterval(timer); timer = null; } };
    var start = function () { stop(); if (reduce || userPaused || hovering || !inView || document.hidden) return; timer = setInterval(function () { go(cur + 1); }, DELAY); };
    var manual = function (k) { go(k); start(); };
    $('#cf-prev').addEventListener('click', function () { manual(cur - 1); });
    $('#cf-next').addEventListener('click', function () { manual(cur + 1); });
    if (cfRange) cfRange.addEventListener('input', function () { manual(+cfRange.value - 1); });
    if (cfPlay) cfPlay.addEventListener('click', function () {
      userPaused = !userPaused;
      cfPlay.setAttribute('aria-pressed', userPaused ? 'true' : 'false');
      cfPlay.setAttribute('aria-label', userPaused ? 'Play automatic slideshow' : 'Pause automatic slideshow');
      start();
    });
    cfSlides.forEach(function (s, i) { s.addEventListener('click', function () { if (i !== cur) manual(i); }); });
    cfStage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); manual(cur - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); manual(cur + 1); }
    });
    cfStage.addEventListener('mouseenter', function () { hovering = true; stop(); });
    cfStage.addEventListener('mouseleave', function () { hovering = false; start(); });
    var tx = null;
    cfStage.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    cfStage.addEventListener('touchend', function (e) {
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx;
      if (Math.abs(dx) > 40) manual(dx < 0 ? cur + 1 : cur - 1);
      tx = null;
    }, { passive: true });
    document.addEventListener('visibilitychange', start);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { inView = en[0].isIntersecting; start(); }, { threshold: 0.25 }).observe(cf);
    }
    render(); start();
    if (reduce && cfPlay) { userPaused = true; cfPlay.setAttribute('aria-pressed', 'true'); }
  }

  /* ---------- Estimator ---------- */
  var estTools = $('#est-tools');
  if (estTools) {
    var estCost = $('#est-cost'), estShare = $('#est-share');
    var fmt = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };
    var update = function () {
      var t = +estTools.value, c = +estCost.value, s = +estShare.value;
      var monthly = t * c;
      $('#est-tools-out').textContent = t;
      $('#est-cost-out').textContent = fmt(c);
      $('#est-share-out').textContent = s + '%';
      $('#est-monthly').textContent = fmt(monthly);
      $('#est-annual').textContent = fmt(monthly * 12);
      $('#est-unused').textContent = fmt(monthly * 12 * s / 100);
    };
    [estTools, estCost, estShare].forEach(function (el) { el.addEventListener('input', update); });
    $$('.chip input').forEach(function (cb) {
      cb.addEventListener('change', function () {
        var n = $$('.chip input:checked').length;
        if (n > 0) { estTools.value = Math.min(n, +estTools.max); update(); }
      });
    });
    update();
  }

  /* ---------- Reveal (hero only; respects reduced motion via CSS) ---------- */

  /* ---------- Consultation form ---------- */
  var form = $('#consult-form');
  if (form) {
    var svcBoxes = $$('input[type="checkbox"][name^="svc_"]', form);
    var hidden = $('#selected-services');
    var list = $('#selected-list');
    var empty = $('#selected-empty');
    var primary = null;

    var selectedNames = function () { return svcBoxes.filter(function (b) { return b.checked; }).map(function (b) { return b.value; }); };

    var refresh = function () {
      var names = selectedNames();
      hidden.value = names.length ? names.join(', ') : 'No service selected';
      list.innerHTML = '';
      names.forEach(function (n) { var li = document.createElement('li'); li.textContent = n; list.appendChild(li); });
      empty.hidden = names.length > 0;
      svcBoxes.forEach(function (b) {
        var label = b.closest('.check');
        if (label) label.classList.toggle('is-primary', b === primary);
      });
    };

    svcBoxes.forEach(function (b) {
      b.addEventListener('change', function () {
        if (b === primary && !b.checked) b.checked = true;
        refresh();
      });
    });

    $$('[data-service]').forEach(function (el) {
      el.addEventListener('click', function () {
        var name = el.getAttribute('data-service');
        svcBoxes.forEach(function (b) { b.checked = false; });
        primary = null;
        svcBoxes.forEach(function (b) { if (b.value === name) { b.checked = true; primary = b; } });
        refresh();
      });
    });

    try {
      var wanted = new URLSearchParams(window.location.search).get('service');
      if (wanted) svcBoxes.forEach(function (b) { if (b.getAttribute('data-slug') === wanted) { b.checked = true; primary = b; } });
    } catch (e) {}

    var email = $('#f-email'), replyTo = $('#reply-to');
    if (email && replyTo) email.addEventListener('input', function () { replyTo.value = email.value; });

    var btn = $('#submit-btn'), err = $('#form-error'), ok = $('#form-success');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      refresh();
      if (replyTo && email) replyTo.value = email.value;
      var label = btn.textContent;
      btn.textContent = 'Sending…'; btn.disabled = true; err.classList.remove('is-visible');
      fetch(form.getAttribute('action'), { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error('bad status');
          var names = selectedNames();
          var ul = $('#success-services');
          ul.innerHTML = '';
          names.forEach(function (n) { var li = document.createElement('li'); li.textContent = n; ul.appendChild(li); });
          $('#success-services-wrap').hidden = names.length === 0;
          form.hidden = true;
          ok.classList.add('is-visible');
          var h = $('h3', ok); if (h) { h.setAttribute('tabindex', '-1'); h.focus(); }
        })
        .catch(function () {
          btn.textContent = label; btn.disabled = false; err.classList.add('is-visible');
        });
    });
    refresh();
  }
})();
