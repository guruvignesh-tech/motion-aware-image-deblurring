"""Check published record completeness and aggregates; does not run neural inference."""
import csv
import json
import math
import statistics
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'results'
with (root / 'measurements.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
summary = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
protocol = json.loads((root / 'protocol.json').read_text(encoding='utf-8'))
assert len(rows) == 304
assert len({(r['sample'], r['method']) for r in rows}) == 304
assert {r['sample'] for r in rows} == set(protocol['sample_ids'])
assert len(summary) == 19
assert {r['method'] for r in rows} == {s['method'] for s in summary}
assert all(0 <= int(r['correct_matches']) <= int(r['matches']) for r in rows)
for s in summary:
    group = [r for r in rows if r['method'] == s['method']]
    assert len(group) == s['n'] == 16
    for metric in ['psnr_linear_db', 'ssim_linear', 'correct_matches']:
        values = [float(r[metric]) for r in group]
        assert all(math.isfinite(v) for v in values)
        assert math.isclose(statistics.mean(values), s[metric], rel_tol=1e-9, abs_tol=1e-9)
print('PASS: 304 unique measurements, 16 samples, 19 conditions; aggregates agree.')
