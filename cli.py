import argparse, json
from config import load_jobs
from engine import run_job
from checkpoint import get_offset

def run(argv=None):
    p=argparse.ArgumentParser(prog='data-sync-automator')
    sub=p.add_subparsers(dest='cmd', required=True)

    r=sub.add_parser('run'); r.add_argument('--config', required=True); r.add_argument('--job', required=True)
    pl=sub.add_parser('plan'); pl.add_argument('--config', required=True)
    st=sub.add_parser('status'); st.add_argument('--job', required=True)
    rt=sub.add_parser('retry'); rt.add_argument('--config', required=True); rt.add_argument('--job', required=True)

    a=p.parse_args(argv)

    if a.cmd in ('run','retry'):
        jobs=load_jobs(a.config).get('jobs',[])
        j=next((x for x in jobs if x.get('name')==a.job), None)
        if not j:
            print('Job not found'); return 1
        res=run_job(j['name'], j['source'], j['target'], j.get('batch_size',100))
        print(json.dumps(res, indent=2)); return 0

    if a.cmd=='plan':
        jobs=load_jobs(a.config).get('jobs',[])
        print(f"Loaded {len(jobs)} jobs")
        for j in jobs:
            print(f"- {j.get('name')}: {j.get('source')} -> {j.get('target')}")
        return 0

    if a.cmd=='status':
        print({'job':a.job,'offset':get_offset(a.job)})
        return 0

    return 0
