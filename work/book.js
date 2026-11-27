// Flipbook: two-page spreads on wide screens, one page on phones.
(function () {
  const book = document.getElementById('book');
  if (!book) return;
  const pages = JSON.parse(book.dataset.pages);
  const N = pages.length;
  const L = book.querySelector('.slot.l img'), R = book.querySelector('.slot.r img');
  const leaf = book.querySelector('.leaf'), lf = leaf.querySelector('.f'), lb = leaf.querySelector('.b');
  const count = document.querySelector('.bcount');
  const thumbs = [...document.querySelectorAll('.book-thumbs button')];
  const wide = matchMedia('(min-width: 860px)');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 0, busy = false; // i = index of the page on the right (wide) or the only page (narrow)

  // Wide layout: spread k shows [left, right]. Spread 0 is the cover on the right.
  const spreadOf = p => (p === 0 ? 0 : Math.floor((p + 1) / 2));
  const spreadPages = k => (k === 0 ? [null, 0] : [2 * k - 1, 2 * k < N ? 2 * k : null]);
  const lastSpread = () => spreadOf(N - 1);
  let k = 0;

  function set(img, p) {
    if (p === null || p === undefined) { img.removeAttribute('src'); img.parentElement.classList.add('empty'); return; }
    img.parentElement.classList.remove('empty');
    img.src = pages[p]; img.alt = 'Page ' + (p + 1) + ' of ' + N;
  }
  function render() {
    book.classList.toggle('wide', wide.matches);
    if (wide.matches) {
      const [a, b] = spreadPages(k);
      set(L, a); set(R, b);
      book.classList.toggle('closed', a === null);
      book.classList.toggle('closed-end', b === null);
      const shown = [a, b].filter(x => x !== null).map(x => x + 1);
      count.textContent = (shown.length === 2 ? shown.join('–') : shown[0]) + ' / ' + N;
      thumbs.forEach((t, j) => t.classList.toggle('on', j === a || j === b));
    } else {
      book.classList.remove('closed', 'closed-end');
      set(R, i); set(L, null);
      count.textContent = (i + 1) + ' / ' + N;
      thumbs.forEach((t, j) => t.classList.toggle('on', j === i));
    }
    const atStart = wide.matches ? k === 0 : i === 0;
    const atEnd = wide.matches ? k === lastSpread() : i === N - 1;
    document.querySelectorAll('.bprev, .edge.prev').forEach(b => (b.disabled = atStart));
    document.querySelectorAll('.bnext, .edge.next').forEach(b => (b.disabled = atEnd));
  }

  function turn(dir) {
    if (busy) return;
    if (!wide.matches) {
      const n = i + dir; if (n < 0 || n >= N) return;
      i = n;
      if (reduce) return render();
      book.classList.remove('slide-l', 'slide-r'); void book.offsetWidth;
      book.classList.add(dir > 0 ? 'slide-l' : 'slide-r');
      return render();
    }
    const n = k + dir; if (n < 0 || n > lastSpread()) return;
    if (reduce) { k = n; return render(); }
    busy = true;
    const [ca, cb] = spreadPages(k), [na, nb] = spreadPages(n);
    // The leaf carries the page being turned: forward = current right -> next left; back = current left -> previous right.
    if (dir > 0) { lf.src = pages[cb]; lb.src = pages[na]; set(R, nb); }
    else { lf.src = pages[ca]; lb.src = pages[nb]; set(L, na); }
    leaf.className = 'leaf ' + (dir > 0 ? 'fwd' : 'bwd');
    void leaf.offsetWidth;
    leaf.classList.add('go');
    leaf.addEventListener('transitionend', function done() {
      leaf.removeEventListener('transitionend', done);
      k = n; leaf.className = 'leaf'; busy = false; render();
    });
  }
  function goTo(p) {
    if (wide.matches) { k = spreadOf(p); } else { i = p; }
    render();
  }

  document.querySelectorAll('.bnext, .edge.next').forEach(b => b.addEventListener('click', () => turn(1)));
  document.querySelectorAll('.bprev, .edge.prev').forEach(b => b.addEventListener('click', () => turn(-1)));
  thumbs.forEach(t => t.addEventListener('click', () => goTo(+t.dataset.i)));
  book.tabIndex = 0;
  book.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { e.preventDefault(); turn(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); turn(-1); }
  });
  // Swipe on touch screens
  let sx = null;
  book.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  book.addEventListener('touchend', e => {
    if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 40) turn(dx < 0 ? 1 : -1);
  });
  wide.addEventListener('change', () => {
    if (wide.matches) k = spreadOf(i); else i = Math.max(0, spreadPages(k)[0] ?? 0);
    render();
  });
  pages.forEach(src => { const im = new Image(); im.src = src; });
  render();
})();
