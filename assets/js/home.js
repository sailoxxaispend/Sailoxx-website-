/* Sailoxx homepage: scale fixed-size design boxes to their container, pause loops when off screen. */
(function () {
  'use strict';
  var fits = [].slice.call(document.querySelectorAll('.fit'));
  function apply(f) {
    var inner = f.firstElementChild;
    var w = +f.getAttribute('data-fit-w'), h = +f.getAttribute('data-fit-h'), min = +(f.getAttribute('data-fit-min') || 0);
    if (min && window.innerWidth < min) { f.style.height = ''; inner.style.removeProperty('--s'); return; }
    var s = Math.min(f.clientWidth / w, 1.12);
    inner.style.setProperty('--s', s.toFixed(4));
    f.style.height = (h * s).toFixed(1) + 'px';
  }
  fits.forEach(apply);
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function (entries) { entries.forEach(function (e) { apply(e.target); }); });
    fits.forEach(function (f) { ro.observe(f); });
  } else { window.addEventListener('resize', function () { fits.forEach(apply); }); }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.target.classList.toggle('is-paused', !e.isIntersecting); });
    }, { threshold: 0.05 });
    [].slice.call(document.querySelectorAll('.dg, .pages')).forEach(function (el) { io.observe(el); });
  }

  var spv = document.querySelector('.spv');
  if (spv) {
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) spv.classList.add('in');
          spv.classList.toggle('is-paused', !e.isIntersecting);
        });
      }, { threshold: 0.2 });
      io2.observe(spv);
    } else { spv.classList.add('in'); }
  }
    /* Search bar: types each question, holds it, erases it, then moves to the next (loops) */
  var typeEl = document.querySelector('.ask-type-text');
  if (typeEl) {
    var caret = document.querySelector('.ask-caret');
    var QUESTIONS = [
      'Are you paying for AI tools that do the same job?',
      'Do you know which AI tools are actually worth their cost?',
      'Can you prove your AI spending is delivering real business value?',
      'Do you know which AI tools your employees are using?',
      'Do you know what to keep, cut, fix, or replace before your next AI renewal?'
    ];
    var qi = 0, ci = 0, erasing = false, tTimer = null, tVisible = true;
    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var later = function (fn, ms) { tTimer = setTimeout(fn, ms); };
    var step = function () {
      if (!tVisible || document.hidden) { later(step, 400); return; }
      var q = QUESTIONS[qi];
      if (calm) { typeEl.textContent = q; qi = (qi + 1) % QUESTIONS.length; later(step, 4500); return; }
      if (!erasing) {
        ci++; typeEl.textContent = q.slice(0, ci);
        if (caret) caret.classList.add('is-typing');
        if (ci >= q.length) { erasing = true; if (caret) caret.classList.remove('is-typing'); later(step, 2200); }
        else later(step, 34 + Math.random() * 36);
      } else {
        ci--; typeEl.textContent = q.slice(0, ci);
        if (caret) caret.classList.add('is-typing');
        if (ci <= 0) { erasing = false; qi = (qi + 1) % QUESTIONS.length; if (caret) caret.classList.remove('is-typing'); later(step, 450); }
        else later(step, 16);
      }
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { tVisible = en[0].isIntersecting; }, { threshold: 0.05 }).observe(typeEl);
    }
    later(step, 1800);
  }
})();
