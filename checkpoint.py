import sqlite3
from pathlib import Path

DB=Path.home()/'.data-sync-automator'/'checkpoints.db'

def _conn():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS cp(job TEXT PRIMARY KEY, offset INTEGER)')
    return c

def get_offset(job):
    c=_conn(); r=c.execute('SELECT offset FROM cp WHERE job=?',(job,)).fetchone(); c.close(); return r[0] if r else 0

def set_offset(job, offset):
    c=_conn(); c.execute('INSERT OR REPLACE INTO cp(job,offset) VALUES(?,?)',(job,offset)); c.commit(); c.close()
