// Case study template: shared behavior for every case study page.
// - Express / Local toggle (remembers the reader's choice)
// - Trip progress line that fills as you scroll and jumps to a stop when clicked
// - Iteration slider driven by a <script type="application/json" id="iterations-data"> block
// - Click-to-load live embed, so the page stays fast
{
  const body = document.body;
  // Add ?draft to the address to see the yellow "To add" boxes
  if (new URLSearchParams(location.search).has('draft')) body.classList.add('draft');
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // ---- Express / Local ----
  const btns = [...document.querySelectorAll('[data-mode]')];
  function setMode(m, scroll) {
    body.classList.toggle('express', m === 'express');
    body.classList.toggle('local', m === 'local');
    btns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === m)));
    store.set('cs-mode', m);
    if (scroll) document.getElementById('mode-start')?.scrollIntoView({ block: 'start' });
    placeTrip();
  }
  btns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode, b.hasAttribute('data-scroll'))));

  // ---- Trip progress line ----
  const trip = document.querySelector('.trip');
  const fill = trip?.querySelector('.fill');
  const stops = trip ? [...trip.querySelectorAll('a')] : [];
  const secs = stops.map(a => document.querySelector(a.getAttribute('href')));
  function placeTrip() {
    if (!trip || !body.classList.contains('local')) return;
    const line = innerHeight * 0.35;
    let cur = -1;
    secs.forEach((s, i) => { if (s && s.getBoundingClientRect().top < line) cur = i; });
    let prog = 0;
    if (cur >= 0) {
      const s = secs[cur], next = secs[cur + 1];
      const top = s.getBoundingClientRect().top, end = next ? next.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
      const part = Math.min(1, Math.max(0, (line - top) / Math.max(1, end - top)));
      prog = (cur + part) / Math.max(1, stops.length - 1);
    }
    fill.style.width = `calc(${Math.min(1, prog) * 100}% - ${Math.min(1, prog) * 16}px)`;
    stops.forEach((a, i) => { a.classList.toggle('done', i <= cur); a.classList.toggle('now', i === cur); });
  }
  addEventListener('scroll', placeTrip, { passive: true });
  addEventListener('resize', placeTrip);
  setMode(new URLSearchParams(location.search).get('mode') || store.get('cs-mode') || 'express', false);

  // ---- Iteration slider ----
  const data = document.getElementById('iterations-data');
  const iter = document.querySelector('.iter');
  if (data && iter) {
    const V = JSON.parse(data.textContent);
    const range = iter.querySelector('input[type=range]');
    const img = iter.querySelector('figure img');
    const out = k => iter.querySelector(`[data-out="${k}"]`);
    range.max = V.length - 1;
    iter.querySelector('.ticks').innerHTML = V.map(v => `<span>${v.short}</span>`).join('');
    V.forEach(v => { const p = new Image(); p.src = v.img; });
    function show(i) {
      const v = V[i];
      range.value = i;
      img.src = v.img; img.alt = v.alt;
      out('ver').textContent = `Version ${i + 1} of ${V.length} · ${v.date}`;
      out('title').textContent = v.title;
      out('what').textContent = v.what;
      out('why').textContent = v.why;
      range.setAttribute('aria-valuetext', v.title);
    }
    range.addEventListener('input', () => show(+range.value));
    iter.querySelector('[data-step="-1"]').addEventListener('click', () => show(Math.max(0, +range.value - 1)));
    iter.querySelector('[data-step="1"]').addEventListener('click', () => show(Math.min(V.length - 1, +range.value + 1)));
    show(0);
  }

  // ---- Live embed, loaded on click ----
  document.querySelectorAll('.tryit .start').forEach(btn => btn.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.src = btn.dataset.src;
    f.title = btn.dataset.title || 'Live project';
    f.loading = 'lazy';
    btn.replaceWith(f);
  }));
}
