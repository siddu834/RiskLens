"""Build a self-contained static site and reject missing assets or invalid JSON."""
import json
import shutil
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('img', 'script') and attrs.get('src'):
            self.paths.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            self.paths.append(attrs['href'])
        if tag == 'a' and attrs.get('href', '').startswith('data/'):
            self.paths.append(attrs['href'])


def reject_constant(value):
    raise ValueError(f'Non-standard JSON constant: {value}')


def build():
    destination = ROOT / 'site'
    # Overlay only: never recursively delete user files.
    shutil.copytree(ROOT / 'website', destination, dirs_exist_ok=True)
    shutil.copytree(ROOT / 'figures', destination / 'figures', dirs_exist_ok=True)
    # Stable public schemas requested by the website rubric; regenerate from
    # notebook exports so aliases cannot silently retain an earlier run.
    data = ROOT / 'website/data'
    exports = {
        'metrics_summary.json': json.loads((data / 'summary_metrics.json').read_text()),
        'roc_pr.json': {
            'roc': json.loads((data / 'roc_curve.json').read_text()),
            'pr': json.loads((data / 'pr_curve.json').read_text()),
        },
        'calibration.json': json.loads((data / 'calibration_curve.json').read_text()),
    }
    charts = {'calibration': exports['calibration.json']}
    for name in ['roc', 'pr']:
        rows = exports['roc_pr.json'][name]
        indices = sorted({round(i * (len(rows)-1) / 499) for i in range(500)})
        charts[name] = [rows[i] for i in indices]
    exports['chart_data.json'] = charts
    for filename, value in exports.items():
        serialized = json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n'
        (data / filename).write_text(serialized, encoding='utf-8')
        (destination / 'data' / filename).write_text(serialized, encoding='utf-8')
    metrics = json.loads((ROOT / 'results/final_test_metrics.json').read_text(encoding='utf-8'),
                         parse_constant=reject_constant)
    count = sum(metrics[k] for k in ['tn', 'fp', 'fn', 'tp'])
    summary = (f'On {count:,} held-out records: ROC-AUC {metrics["roc_auc"]:.4f}, '
               f'average precision {metrics["pr_auc"]:.4f}, and Brier score {metrics["brier_score"]:.4f}. '
               f'At threshold {metrics["threshold"]:.2f}: precision {metrics["precision"]:.2%}, '
               f'recall {metrics["recall"]:.2%}, and F1 {metrics["f1_score"]:.4f}. '
               'Generated from the saved final evaluation metrics.')
    index = destination / 'index.html'
    html, replacements = re.subn(r'(<p id="finalTestSummary">).*?(</p>)',
                                 lambda match: match[1]+summary+match[2],
                                 index.read_text(encoding='utf-8'), flags=re.DOTALL)
    if replacements != 1:
        raise ValueError('Expected exactly one final-test summary placeholder')
    index.write_text(html, encoding='utf-8')
    for path in (destination / 'data').rglob('*.json'):
        value = json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)
        compact = json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n'
        path.write_text(compact, encoding='utf-8')
        (data / path.relative_to(destination / 'data')).write_text(compact, encoding='utf-8')
    assets = Assets()
    assets.feed((destination / 'index.html').read_text(encoding='utf-8'))
    for relative in assets.paths:
        path = (destination / relative).resolve()
        if not path.is_relative_to(destination.resolve()) or not path.is_file():
            raise ValueError(f'Missing or external site asset: {relative}')
    print('Website built; JSON and referenced assets verified:', destination)


if __name__ == '__main__':
    build()
