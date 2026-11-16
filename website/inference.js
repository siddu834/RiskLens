/* Exact exported preprocessing, XGBoost tree traversal and isotonic interpolation.
   No network requests or storage: the caller supplies the public model. */
(function (root) {
  'use strict';
  const late = ['NumberOfTime30-59DaysPastDueNotWorse', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfTimes90DaysLate'];
  const missing = v => v === null || v === undefined || Number.isNaN(v);
  function clean(input, features) {
    const row = Object.fromEntries(features.map(k => [k, input[k]]));
    if (row.age === 0) row.age = null;
    for (const k of ['age', 'MonthlyIncome', 'NumberOfDependents']) row['missingindicator_' + k] = +missing(row[k]);
    row.late_payment_sentinel = +late.some(k => row[k] === 96 || row[k] === 98);
    for (const k of late) if (row[k] === 96 || row[k] === 98) row[k] = null;
    return row;
  }
  function interpolate(value, x, y) {
    if (value <= x[0]) return y[0];
    if (value >= x[x.length - 1]) return y[y.length - 1];
    let lo = 0, hi = x.length - 1;
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (x[mid] <= value) lo = mid; else hi = mid; }
    return y[lo] + (value - x[lo]) / (x[hi] - x[lo]) * (y[hi] - y[lo]);
  }
  function predict(model, input) {
    const row = clean(input, model.features);
    const order = [...model.features, 'missingindicator_age', 'missingindicator_MonthlyIncome', 'missingindicator_NumberOfDependents', 'late_payment_sentinel'];
    const probabilities = model.members.map(member => {
      const values = order.map((k, i) => {
        let value = row[k];
        if (!missing(value) && Object.hasOwn(member.caps, k)) value = Math.min(value, member.caps[k]);
        return Math.fround(missing(value) ? member.medians[i] : value);
      });
      let margin = Math.fround(member.base_margin);
      for (const tree of member.trees) {
        let node = 0;
        while (tree.left_children[node] !== -1) {
          const value = values[tree.split_indices[node]];
          const left = Number.isNaN(value) ? tree.default_left[node] : value < Math.fround(tree.split_conditions[node]);
          node = left ? tree.left_children[node] : tree.right_children[node];
        }
        margin = Math.fround(margin + Math.fround(tree.split_conditions[node]));
      }
      const probability = Math.fround(1 / (1 + Math.exp(-margin)));
      return interpolate(probability, member.isotonic_x, member.isotonic_y);
    });
    return probabilities.reduce((a, b) => a + b, 0) / probabilities.length;
  }
  const api = { predict, clean, interpolate };
  if (typeof module !== 'undefined') module.exports = api;
  else root.RiskLens = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
