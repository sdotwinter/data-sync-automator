import json
from pathlib import Path

def read_source(path):
    p=Path(path)
    if not p.exists():
        return []
    txt=p.read_text(encoding='utf-8')
    try:
        return json.loads(txt)
    except Exception:
        return [{'line':ln} for ln in txt.splitlines() if ln.strip()]

def write_target(path, items):
    p=Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(items, indent=2), encoding='utf-8')
