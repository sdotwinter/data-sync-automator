import json

def print_summary(summary, as_json=False):
    if as_json:
        print(json.dumps(summary, indent=2)); return
    print('Sync summary')
    print('------------')
    for k in ['timestamp','source_count','target_count_before','target_count_after','created','updated','applied_changes','dry_run']:
        print(f"{k}: {summary.get(k)}")

def print_history(rows):
    if not rows:
        print('No sync history.')
        return
    for r in rows:
        print(f"[{r[0]}] {r[1]} src={r[2]} tgt={r[3]}")
