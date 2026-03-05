import argparse, json
from pathlib import Path
from connectors import load_records, save_records
from sync_engine import sync_records
from state_store import add_run, list_runs
from reporter import print_summary, print_history

def run(argv=None):
    p=argparse.ArgumentParser(prog='data-sync-automator', description='Sync records between source and target datasets.')
    sub=p.add_subparsers(dest='cmd', required=True)

    s=sub.add_parser('sync')
    s.add_argument('--source', required=True)
    s.add_argument('--target', required=True)
    s.add_argument('--key', default='id')
    s.add_argument('--conflict', choices=['source_wins','target_wins'], default='source_wins')
    s.add_argument('--dry-run', action='store_true')
    s.add_argument('--json', action='store_true')
    s.add_argument('path', nargs='?', default='.')

    d=sub.add_parser('dry-run')
    d.add_argument('--source', required=True)
    d.add_argument('--target', required=True)
    d.add_argument('--key', default='id')
    d.add_argument('--json', action='store_true')
    d.add_argument('path', nargs='?', default='.')

    h=sub.add_parser('history')
    h.add_argument('path', nargs='?', default='.')

    st=sub.add_parser('status')
    st.add_argument('path', nargs='?', default='.')

    args=p.parse_args(argv)
    root=Path(getattr(args,'path','.')).resolve()

    if args.cmd in ('sync','dry-run'):
        src=Path(args.source); tgt=Path(args.target)
        source=load_records(src)
        target=load_records(tgt) if tgt.exists() else []
        merged, summary = sync_records(source,target,key=args.key,conflict=getattr(args,'conflict','source_wins'),dry_run=(args.cmd=='dry-run' or args.dry_run))
        if not (args.cmd=='dry-run' or args.dry_run):
            save_records(tgt, merged)
        add_run(root, summary['timestamp'], str(src), str(tgt), json.dumps(summary))
        print_summary(summary, as_json=args.json)
        return 0

    if args.cmd == 'history':
        print_history(list_runs(root))
        return 0

    if args.cmd == 'status':
        rows=list_runs(root, limit=1)
        if not rows:
            print('No sync runs yet.')
        else:
            print(f'Last run: {rows[0][1]} source={rows[0][2]} target={rows[0][3]}')
        return 0

    return 0
