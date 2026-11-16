const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {predict, interpolate} = require('../website/inference.js');
const root = path.resolve(__dirname, '..');
const model = JSON.parse(fs.readFileSync(path.join(root, 'website/data/model.json')));
assert.equal(model.schema_version, 2);
for (const member of model.members) {
  member.trees = member.tree_files.flatMap(file => JSON.parse(fs.readFileSync(path.join(root, 'website/data', file))));
  assert.equal(member.trees.length, 300);
}
const fixturePath = process.argv[2] || path.join(__dirname, 'browser_fixtures.json');
const fixture = JSON.parse(fs.readFileSync(fixturePath));
let maxError = 0, classificationDisagreements = 0;
fixture.inputs.forEach((row, i) => {
  const before = JSON.stringify(row);
  const actual = predict(model, row);
  assert.equal(JSON.stringify(row), before, 'Inference must not mutate inputs');
  assert.ok(actual >= 0 && actual <= 1);
  maxError = Math.max(maxError, Math.abs(actual - fixture.expected[i]));
  if ((actual >= .23) !== (fixture.expected[i] >= .23)) classificationDisagreements++;
});
// XGBoost's float32 sigmoid and JS Math.exp differ at a few steep isotonic knots.
// Tolerance is 0.002 percentage points, well below the UI's 0.1-point precision.
assert.ok(maxError < 0.00002, `Python/browser probability mismatch: ${maxError}`);
assert.equal(classificationDisagreements, 0, 'Frozen-threshold classifications must agree');
assert.equal(interpolate(-1, [0, 1], [.1, .9]), .1);
assert.equal(interpolate(2, [0, 1], [.1, .9]), .9);
assert.equal(interpolate(.5, [0, 1], [.1, .9]), .5);
console.log(JSON.stringify({cases: fixture.inputs.length, max_probability_error: maxError, classification_disagreements: classificationDisagreements, passed: true}));
