// Lidija Torte i Kolači · home interactions
const motionOK = document.documentElement.classList.contains('js');
const COLORS = ['#00ABE6', '#FDB933', '#DB6E9D', '#F7ACBC', '#FFFFFF', '#A23D6B'];

// Sprinkles flying out of a point, then falling with gravity.
function sprinkle(layer, x, y, n, spread = 1) {
  for (let i = 0; i < n; i++) {
    const s = document.createElement('span');
    s.className = 'sp';
    s.style.background = COLORS[i % COLORS.length];
    s.style.left = x + 'px';
    s.style.top = y + 'px';
    layer.append(s);
    const a = (-Math.PI / 2) + (Math.random() - .5) * Math.PI * 1.3;
    const v = (90 + Math.random() * 140) * spread;
    const dx = Math.cos(a) * v, dy = Math.sin(a) * v;
    const r = (Math.random() - .5) * 720;
    s.animate([
      { transform: 'translate(-50%,-50%) rotate(0deg)', opacity: 1 },
      { transform: `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) rotate(${r / 2}deg)`, opacity: 1, offset: .45 },
      { transform: `translate(calc(-50% + ${dx * 1.3}px), calc(-50% + ${dy + 260 * spread}px)) rotate(${r}deg)`, opacity: 0 },
    ], { duration: 1300 + Math.random() * 600, easing: 'cubic-bezier(.2,.7,.4,1)', fill: 'forwards' }).onfinish = () => s.remove();
  }
}

// Hero: the bow unties, the ribbon slides off and the box opens.
const stage = document.getElementById('box-stage');
if (stage) {
const showerFromBox = (n) => {
  const w = stage.querySelector('.box-window').getBoundingClientRect();
  const st = stage.getBoundingClientRect();
  sprinkle(document.getElementById('sprinkles'), w.left - st.left + w.width * .55, w.top - st.top + 20, n);
};
if (motionOK) {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    stage.classList.remove('intro');
    setTimeout(() => showerFromBox(30), 1250);
    setTimeout(() => stage.querySelector('.sheen').classList.add('go'), 1500);
    // Intro finished: drop the staggered delays so hover moments respond at once.
    setTimeout(() => stage.classList.add('done'), 3400);
  }));
} else {
  stage.classList.remove('intro');
  stage.classList.add('done');
}

// Tapping the cake gives another little shower.
stage.querySelector('.box-window').addEventListener('click', (e) => {
  if (!motionOK) return;
  const st = stage.getBoundingClientRect();
  sprinkle(document.getElementById('sprinkles'), e.clientX - st.left, e.clientY - st.top, 18);
});
}

// Contact buttons: a small burst of sprinkles on press.
const burstLayer = document.createElement('div');
burstLayer.className = 'burst';
document.body.append(burstLayer);
document.querySelectorAll('[data-burst]').forEach((b) => b.addEventListener('pointerdown', (e) => {
  if (motionOK) sprinkle(burstLayer, e.clientX, e.clientY, 14, .7);
}));

// Reveal on scroll.
if (motionOK && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((es) => es.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal, .drip-edge, .drip').forEach((el) => io.observe(el));
} else {
  document.querySelectorAll('.reveal, .drip-edge, .drip').forEach((el) => el.classList.add('in'));
}

// How much cake: guests to kilograms, price range and tiers.
// Assumption to confirm with Lidija: about 8 slices per kilogram, minimum 2 kg.
const range = document.getElementById('guests');
if (range) {
const fmt = new Intl.NumberFormat('sr-RS');
const TOPS = { 1: 300, 2: 226, 3: 162, 4: 108 };
const narrow = matchMedia('(max-width: 900px)');
const cakeSvg = document.getElementById('cake-svg');
const LABELS = { 1: 'lepa torta za sto', 2: 'torta na dva sprata', 3: 'tri sprata, za veliko slavlje', 4: 'četiri sprata, svadbeni format' };
function updateCake() {
  const g = +range.value;
  const kg = Math.max(2, Math.ceil((g / 8) * 2) / 2);
  const tiers = kg <= 3 ? 1 : kg <= 6 ? 2 : kg <= 10 ? 3 : 4;
  document.getElementById('guests-out').value = g;
  document.getElementById('g2').textContent = g;
  document.getElementById('kg').textContent = fmt.format(kg);
  document.getElementById('price').textContent = `${fmt.format(kg * 1600)} do ${fmt.format(kg * 2000)}`;
  range.style.setProperty('--fill', ((g - range.min) / (range.max - range.min) * 100) + '%');
  document.querySelectorAll('.tier').forEach((t) => t.classList.toggle('off', +t.dataset.tier > tiers));
  const candle = document.getElementById('candle');
  if (candle) candle.style.transform = `translateY(${TOPS[tiers] - 108}px)`;
  const label = document.getElementById('cake-label');
  if (label) label.textContent = LABELS[tiers];
  // On narrow screens the drawing hugs the cake, so no empty headroom sits between slider and price.
  if (cakeSvg && cakeSvg.dataset.trim !== 'off') {
    const top = narrow.matches ? TOPS[tiers] - 80 : 0;
    cakeSvg.setAttribute('viewBox', `0 ${top} 400 ${420 - top}`);
  }
  const msg = `Zdravo! Treba mi torta za ${g} osoba (oko ${fmt.format(kg)} kg). Datum: `;
  document.getElementById('calc-wa').href = 'https://wa.me/381649643302?text=' + encodeURIComponent(msg);
}
range.addEventListener('input', updateCake);
narrow.addEventListener('change', updateCake);
updateCake();
}

// Phone dock: appears once the hero buttons scroll away.
const dock = document.querySelector('.dock');
const heroActions = document.querySelector('[data-hero-actions], .hero .actions');
if (dock && heroActions && 'IntersectionObserver' in window) {
  new IntersectionObserver(([en]) => dock.classList.toggle('show', !en.isIntersecting && en.boundingClientRect.top < 0))
    .observe(heroActions);
}

// Occasions ribbon: slides with the scroll instead of looping on its own.
const track = document.querySelector('.band-track');
if (motionOK && track) {
  let ticking = false;
  const move = () => { track.style.transform = `translateX(${-(scrollY * 0.35) % (track.scrollWidth / 2)}px)`; ticking = false; };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(move); } }, { passive: true });
  move();
}

// Header contact menu: opens on hover (CSS) or on click / tap.
const cmenu = document.getElementById('cmenu');
if (cmenu) {
const cbtn = cmenu.querySelector('button');
const setMenu = (open) => { cmenu.classList.toggle('open', open); cbtn.setAttribute('aria-expanded', open); };
cbtn.addEventListener('click', () => setMenu(!cmenu.classList.contains('open')));
document.addEventListener('click', (e) => { if (!cmenu.contains(e.target)) setMenu(false); });
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && cmenu.classList.contains('open')) { setMenu(false); cbtn.focus(); }
});
cmenu.addEventListener('focusout', (e) => { if (!cmenu.contains(e.relatedTarget)) setMenu(false); });
}

// Google reviews: the summary is static HTML; live data from /api/recenzije replaces it.
// Append ?primer to the URL to preview the layout with clearly labeled sample notes.
const rev = document.getElementById('recenzije');
if (rev) {
  const sample = new URLSearchParams(location.search).has('primer');
  const load = sample
    ? new Promise((ok, no) => { const s = document.createElement('script'); s.src = (document.documentElement.dataset.root || '') + 'dev/recenzije-primer.js'; s.onload = () => ok(window.REVIEWS_SAMPLE); s.onerror = no; document.head.append(s); })
    : location.protocol === 'file:' ? Promise.reject('local file')
    : fetch('/api/recenzije').then((r) => (r.ok ? r.json() : Promise.reject(r.status)));
  load.then(renderReviews).catch(() => rev.classList.add('rev-offline'));
}
function renderReviews(d) {
  if (!d || !d.rating) throw new Error('no data');
  const q = (sel) => rev.querySelector(sel);
  q('[data-rev-score]').textContent = d.rating.toLocaleString('sr-RS', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  q('[data-rev-count]').textContent = d.count.toLocaleString('sr-RS');
  if (d.url) { q('[data-rev-all]').href = d.url; const ck = q('.rev-cookie'); if (ck) ck.href = d.url; }
  if (d.id) q('[data-rev-write]').href = 'https://search.google.com/local/writereview?placeid=' + encodeURIComponent(d.id);
  const list = q('[data-rev-list]');
  const MAC = ['#F7ACBC', '#FDD27A', '#A9E4F7', '#F5C6E0', '#CDEBC3'];
  (d.reviews || []).forEach((r, k) => {
    const li = document.createElement('li');
    li.className = 'rev-note'; li.style.setProperty('--k', k);
    li.innerHTML = '<span class="tape" aria-hidden="true"></span><div class="rev-who"><span class="macaron" aria-hidden="true"><span></span></span><div><a class="rev-name" rel="noopener" target="_blank"></a><span class="rev-when"></span></div></div><span class="stars"></span><p class="rev-text"></p>';
    const name = r.author || 'Google korisnik';
    li.querySelector('.macaron').style.setProperty('--m1', MAC[k % MAC.length]);
    li.querySelector('.macaron span').textContent = name.trim().charAt(0).toUpperCase();
    const a = li.querySelector('.rev-name'); a.textContent = name;
    if (r.authorUrl) a.href = r.authorUrl; else a.removeAttribute('href');
    li.querySelector('.rev-when').textContent = r.when || '';
    const st = li.querySelector('.stars'); st.setAttribute('aria-label', `Ocena ${r.rating} od 5`);
    for (let i = 1; i <= 5; i++) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('aria-hidden', 'true'); if (i > r.rating) svg.classList.add('off');
      svg.innerHTML = '<use href="#i-star"/>'; st.append(svg);
    }
    li.querySelector('.rev-text').textContent = r.text || '';
    if (r.url) { const m = document.createElement('a'); m.className = 'rev-more'; m.href = r.url; m.rel = 'noopener'; m.target = '_blank'; m.textContent = 'celu recenziju na Google-u'; li.append(m); }
    list.append(li);
  });
  if (list.children.length) {
    list.hidden = false; q('[data-rev-attr]').hidden = false;
    if (motionOK && 'IntersectionObserver' in window) {
      const o = new IntersectionObserver(([en]) => { if (en.isIntersecting) { list.classList.add('in'); o.disconnect(); } }, { rootMargin: '0px 0px -10% 0px' });
      o.observe(list);
    } else list.classList.add('in');
  }
}

// WhatsApp links open with a message that fits the section the visitor is reading.
const WA_MSG = {
  pocetak: 'Zdravo! Zanima me torta po porudžbini. Datum: ',
  torte: 'Zdravo! Šaljem vam sliku torte koja mi se dopada. Datum: ',
  cene: 'Zdravo! Zanima me cena torte. Broj osoba: , datum: ',
  kolicina: 'Zdravo! Zanima me cena torte. Broj osoba: , datum: ',
  ukusi: 'Zdravo! Treba mi savet za ukus torte. ',
  porucivanje: 'Zdravo! Želim da poručim tortu. Datum i vreme: , ukus: , veličina: ',
  dostava: 'Zdravo! Da li dostavljate tortu u mesto: ? Datum: ',
  dijaspora: 'Zdravo! Javljam se iz inostranstva, želim tortu za porodicu u Leskovcu. Datum: ',
  pitanja: 'Zdravo! Imam pitanje: ',
};
const WA_DEFAULT = 'Zdravo! Imam pitanje za tortu. ';
document.querySelectorAll('a[href^="https://wa.me/"]').forEach((a) => {
  if (a.id === 'calc-wa') return;
  const msg = a.dataset.msg || WA_MSG[a.closest('[id]')?.id] || WA_DEFAULT;
  a.href = 'https://wa.me/381649643302?text=' + encodeURIComponent(msg);
});

// Analytics: with no forms, clicks on phone, WhatsApp and Viber are the site's conversions.
// Fill GA_ID once the GA4 property exists, then mark "contact_click" as a key event in GA4.
const GA_ID = '';
if (GA_ID) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', GA_ID);
  document.head.append(Object.assign(document.createElement('script'), { async: true, src: 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID }));
}
document.addEventListener('click', (e) => {
  const a = e.target.closest('a[href]');
  if (!a || !window.gtag) return;
  const h = a.getAttribute('href');
  const method = h.startsWith('tel:') ? 'telefon' : h.includes('wa.me/') ? 'whatsapp' : h.startsWith('viber:') ? 'viber'
    : h.includes('writereview') ? 'recenzija' : h.includes('maps.app.goo.gl') || h.includes('google.com/maps') ? 'mapa'
    : h.includes('instagram.com') ? 'instagram' : null;
  if (!method) return;
  const section = a.closest('.cmenu') ? 'meni' : a.closest('.dock') ? 'traka-dole' : a.closest('[id]')?.id || 'ostalo';
  gtag('event', ['telefon', 'whatsapp', 'viber'].includes(method) ? 'contact_click' : 'outbound_click', { method, section });
});

// Carousels: prev/next buttons scroll the track by one card.
document.querySelectorAll('[data-carousel]').forEach((c) => {
  const track = c.querySelector('[data-track]');
  const step = () => (track.firstElementChild?.getBoundingClientRect().width || 300) + 24;
  c.querySelector('[data-prev]')?.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  c.querySelector('[data-next]')?.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
});

// Section rail: highlights the section currently in view.
const rail = document.querySelector('[data-rail]');
if (rail && 'IntersectionObserver' in window) {
  const links = [...rail.querySelectorAll('a')];
  const ro = new IntersectionObserver((es) => es.forEach((en) => {
    if (!en.isIntersecting) return;
    links.forEach((l) => l.classList.toggle('on', l.getAttribute('href') === '#' + en.target.id));
  }), { rootMargin: '-45% 0px -50% 0px' });
  links.forEach((l) => { const t = document.querySelector(l.getAttribute('href')); if (t) ro.observe(t); });
}

// Version switcher (client preview): close on outside click or Escape
const vsw = document.querySelector('.vsw');
if (vsw) {
  document.addEventListener('click', (e) => { if (!vsw.contains(e.target)) vsw.open = false; });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') vsw.open = false; });
}
