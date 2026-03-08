import yaml
from pathlib import Path

def load_jobs(path):
    cfg_path=Path(path).resolve()
    data=yaml.safe_load(cfg_path.read_text(encoding='utf-8')) or {}
    data.setdefault('jobs', [])
    base=cfg_path.parent
    # Normalize job paths relative to config file
    for j in data['jobs']:
        if 'source' in j:
            j['source']=str((base / j['source']).resolve()) if not Path(j['source']).is_absolute() else j['source']
        if 'target' in j:
            j['target']=str((base / j['target']).resolve()) if not Path(j['target']).is_absolute() else j['target']
    return data
