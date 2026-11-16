import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def reject_constant(value):
    raise ValueError(value)


def test_website_data_is_strict_json():
    for path in (ROOT / 'website/data').glob('*.json'):
        json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)


def test_threshold_counts_and_reported_optima():
    rows = json.loads((ROOT / 'website/data/threshold_metrics.json').read_text())
    assert len(rows) == 101
    for row in rows:
        assert sum(row[k] for k in ('tn', 'fp', 'fn', 'tp')) == 120000
        denominator = 2 * row['tp'] + row['fp'] + row['fn']
        assert row['f1_score'] == pytest.approx(2 * row['tp'] / denominator)
        assert row['illustrative_cost'] == 50000 * row['fn'] + 5000 * row['fp']
    # Check reported development optima against data, without freezing a search result.
    report = (ROOT / 'docs/reproduction_report.md').read_text(encoding='utf-8')
    best_f1 = max(rows, key=lambda x: x['f1_score'])['threshold']
    best_cost = min(rows, key=lambda x: x['illustrative_cost'])['threshold']
    assert f'F1 optimum is {best_f1:.2f}' in report
    assert f'cost optimum is {best_cost:.2f}' in report


def test_test_metrics_match_confusion_matrix():
    row = json.loads((ROOT / 'results/final_test_metrics.json').read_text())
    assert sum(row[k] for k in ('tn', 'fp', 'fn', 'tp')) == 30000
    assert row['threshold'] == .23
    assert row['precision'] == pytest.approx(row['tp'] / (row['tp'] + row['fp']))
    assert row['recall'] == pytest.approx(row['tp'] / (row['tp'] + row['fn']))
    assert row['f1_score'] == pytest.approx(2 * row['tp'] / (2 * row['tp'] + row['fp'] + row['fn']))
