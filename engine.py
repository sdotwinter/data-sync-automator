from connectors import read_source, write_target
from checkpoint import get_offset, set_offset

def run_job(name, source, target, batch_size=100):
    data=read_source(source)
    off=get_offset(name)
    batch=data[off:off+batch_size]
    existing=read_source(target)
    if not isinstance(existing,list):
        existing=[]
    out=existing+batch
    write_target(target, out)
    set_offset(name, off+len(batch))
    return {'job':name,'read':len(batch),'new_offset':off+len(batch)}
