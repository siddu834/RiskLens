async function setupDetectionWindow() {
  const slider = document.querySelector('#scopeCut');
  const result = document.querySelector('#scopeResult');
  try {
    const response = await fetch('data/threshold_metrics.json');
    if (!response.ok) throw new Error('Threshold data unavailable');
    const rows = await response.json();
    const field = document.querySelector('#dotField');
    const dots = Array.from({length: 100}, () => field.appendChild(document.createElement('i')));
    function update() {
      const threshold = Number(slider.value) / 100;
      const row = rows.find(item => item.threshold === threshold);
      const caught = Math.round(row.recall * 100);
      dots.forEach((dot, index) => dot.classList.toggle('caught', index < caught));
      document.querySelector('#cutValue').textContent = threshold.toFixed(2);
      result.textContent = caught + '% caught · ' + (100 - caught) + '% missed';
      slider.setAttribute('aria-valuetext', threshold.toFixed(2));
    }
    update();
    slider.disabled = false;
    slider.addEventListener('input', update);
  } catch {
    result.textContent = 'Threshold data could not load. Refresh to try again.';
  }
}
setupDetectionWindow();

const rooms = [
  ['overview', 'Overview', ['.studio', '#question']],
  ['lab', 'Prediction lab', ['#lab']],
  ['results', 'Model evidence', ['#results', '#errors', '#limits', '#conclusion']],
  ['data', 'Research notebook', ['#data', '#preprocess', '#methods', '#evaluation', '#reproduce', '#disclosure']]
];
const navigation = document.createElement('nav');
navigation.className = 'workspace-nav';
navigation.setAttribute('aria-label', 'Research workspace');
const links = rooms.map(([id, label]) => {
  const link = document.createElement('a');
  link.href = '#' + id;
  link.textContent = label;
  navigation.append(link);
  return link;
});
document.querySelector('.studio').id = 'overview';
document.querySelector('main').prepend(navigation);
const topbar = document.querySelector('.topbar');
topbar.style.position = 'sticky';
topbar.style.top = '0';
function updateNavigationOffsets() {
  const headerHeight = topbar.offsetHeight;
  const narrow = matchMedia('(max-width:1000px)').matches;
  navigation.style.top = (headerHeight + (narrow ? 0 : 12)) + 'px';
  const offset = headerHeight + (narrow ? navigation.offsetHeight : 0) + 12;
  document.documentElement.style.scrollPaddingTop = offset + 'px';
  document.querySelectorAll('main > section, #thresholds').forEach(section => {
    section.style.scrollMarginTop = '0';
  });
  document.querySelector('.prediction-panel').style.top = offset + 'px';
}
const navigationResize = new ResizeObserver(updateNavigationOffsets);
navigationResize.observe(topbar);
navigationResize.observe(navigation);
updateNavigationOffsets();
function openRoom() {
  const target = document.getElementById(location.hash.slice(1));
  const active = rooms.findIndex(([, , selectors]) =>
    selectors.some(selector => target && document.querySelector(selector).contains(target)));
  rooms.forEach(([, , selectors], index) => {
    const visible = index === Math.max(0, active);
    links[index].setAttribute('aria-current', visible ? 'page' : 'false');
    for (const selector of selectors) document.querySelector(selector).hidden = !visible;
  });
  if (target && target !== document.querySelector('main')) target.scrollIntoView();
  else window.scrollTo(0, 0);
}
window.addEventListener('hashchange', openRoom);
openRoom();

let previousScroll = window.scrollY;
let scrollDirection = 1;
window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;
  if (Math.abs(currentScroll - previousScroll) > 2) {
    scrollDirection = currentScroll > previousScroll ? 1 : -1;
  }
  previousScroll = currentScroll;
}, {passive:true});
const sectionObserver = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    entry.target.style.setProperty('--scroll-direction', scrollDirection);
    entry.target.classList.remove('scroll-arrived');
    void entry.target.offsetWidth;
    entry.target.classList.add('scroll-arrived');
  }
}, {threshold:.18});
document.querySelectorAll('main > section').forEach(section => sectionObserver.observe(section));

const utilization = document.getElementById('RevolvingUtilizationOfUnsecuredLines');
const scrubber = document.createElement('div');
scrubber.className = 'utilization-control';
scrubber.innerHTML = '<label for="utilDial">Explore credit utilization <output id="utilValue"></output></label><input id="utilDial" type="range" min="0" max="200" step="1"><small>Adjust from 0% to 200% to recalculate this profile with the other inputs held fixed.</small>';
document.querySelector('#inputFields').before(scrubber);
const dial = scrubber.querySelector('input');
function syncDial() {
  dial.value = Math.round(Number(utilization.value) * 100);
  scrubber.querySelector('output').textContent = utilization.value === '' ? '—' : Number((Number(utilization.value) * 100).toFixed(1)) + '%';
}
dial.addEventListener('input', () => {
  utilization.value = Number(dial.value) / 100;
  utilization.dispatchEvent(new Event('input', {bubbles:true}));
  estimate();
});
utilization.addEventListener('input', syncDial);
document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', syncDial));
syncDial();

// Each stationary hit area plays its own note while the glyph moves inside it.
const hoverMotion = matchMedia('(hover: hover) and (prefers-reduced-motion: no-preference)');
const pianoControls = '.brand, .topbar nav a, .workspace-nav a, .actions a, .preset-row button, .segmented button, .download-row a';
for (const control of document.querySelectorAll(pianoControls)) {
  const walker = document.createTreeWalker(control, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    if (!node.textContent.trim()) continue;
    const fragment = document.createDocumentFragment();
    for (const word of node.textContent.split(/(\s+)/u)) {
      if (!word.trim()) { fragment.append(word); continue; }
      const group = document.createElement('i');
      group.style.cssText = 'display:inline-block;font-style:inherit';
      for (const char of word) {
        const key = document.createElement('i');
        key.style.cssText = 'display:inline-block;font-style:inherit';
        const glyph = key.cloneNode();
        glyph.style.pointerEvents = 'none';
        glyph.textContent = char;
        key.append(glyph);
        key.addEventListener('pointerenter', event => {
          if (!hoverMotion.matches || event.pointerType === 'touch') return;
          for (const animation of glyph.getAnimations()) animation.cancel();
          glyph.animate([
            { transform:'translateY(0)' },
            { transform:'translateY(-0.24em)', offset:0.35 },
            { transform:'translateY(0)' }
          ], {duration:300, easing:'ease-in-out'});
        });
        group.append(key);
      }
      fragment.append(group);
    }
    node.replaceWith(fragment);
  }
}
