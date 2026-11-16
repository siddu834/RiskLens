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
