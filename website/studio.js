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
