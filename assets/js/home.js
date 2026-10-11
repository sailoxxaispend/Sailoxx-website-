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
})();
