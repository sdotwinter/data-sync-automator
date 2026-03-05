import csv, json
from pathlib import Path

def load_records(path: Path):
    if path.suffix.lower() == '.json':
        return json.loads(path.read_text(encoding='utf-8'))
    rows=[]
    with path.open('r', encoding='utf-8', newline='') as f:
        r=csv.DictReader(f)
        for row in r: rows.append(dict(row))
    return rows

def save_records(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == '.json':
        path.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
        return
    if not records:
        path.write_text('', encoding='utf-8')
        return
    keys=sorted(records[0].keys())
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(records)
