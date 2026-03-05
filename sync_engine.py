from datetime import datetime

def sync_records(source, target, key='id', conflict='source_wins', dry_run=False):
    t_index = {str(r.get(key,'')): r for r in target}
    applied = 0
    created = 0
    updated = 0

    merged = list(target)
    for s in source:
        sid = str(s.get(key,''))
        if not sid:
            continue
        if sid not in t_index:
            merged.append(dict(s)); created += 1; applied += 1; continue
        current = t_index[sid]
        if current != s:
            if conflict == 'source_wins':
                idx = merged.index(current)
                merged[idx] = dict(s)
            updated += 1
            applied += 1

    summary = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'source_count': len(source),
        'target_count_before': len(target),
        'target_count_after': len(merged),
        'created': created,
        'updated': updated,
        'applied_changes': applied,
        'dry_run': dry_run,
    }
    return merged, summary
