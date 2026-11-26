import argparse, hashlib, json, shutil, sys
from pathlib import Path
HOME=Path(__file__).resolve().parent
def write_new(p,content):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists(): p.write_text(content,encoding='utf-8')
def initialize(project):
    project.mkdir(parents=True,exist_ok=True)
    write_new(project/'AGENTS.md',(HOME/'templates/AGENTS.md').read_text(encoding='utf-8'))
    write_new(project/'.harness/config.json',(HOME/'config/default.json').read_text(encoding='utf-8'))
    write_new(project/'docs/00-original/README.md','Place authorized source documents here.\n')
    for p in ['01-project-context','02-requirements','03-product-vision','04-architecture','05-roadmap','06-sprints','07-decisions','08-evidence']:
        write_new(project/'docs'/p/'README.md',f'# {p}\nPending review.\n')
    write_new(project/'.harness/task.template.json',(HOME/'templates/task.json').read_text(encoding='utf-8'))
    # Preserve existing ignore rules; append protective entries once.
    ignore=project/'.gitignore'; current=ignore.read_text(encoding='utf-8') if ignore.exists() else ''
    rules=['.env','.env.*','!.env.example','*.pem','*.key','.harness/state/','.harness/cache/','.harness/logs/','docs/00-original/*','!docs/00-original/README.md']
    missing=[r for r in rules if r not in current.splitlines()]
    if missing: ignore.write_text(current.rstrip()+'\n'+'\n'.join(missing)+'\n',encoding='utf-8')
    print('Initialized (existing files preserved):',project)
def ingest(project, overwrite=False):
    source=project/'docs/00-original'; out=project/'docs/01-project-context'
    if not source.is_dir(): raise SystemExit('Run init first.')
    data=[]
    for p in sorted(source.rglob('*')):
        if not p.is_file() or p.is_symlink() or p==source/'README.md' or not p.resolve().is_relative_to(source.resolve()): continue
        h=hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
        data.append({'path':p.relative_to(project).as_posix(),'sha256':h.hexdigest(),'bytes':p.stat().st_size,'status':'inventoried_not_extracted'})
    registry=out/'SOURCE_REGISTRY.json'; context_prompt=out/'CONTEXT_UPDATE_PROMPT.md'
    existing=[p for p in (registry,context_prompt) if p.exists()]
    if existing and not overwrite:
        names=', '.join(str(p) for p in existing)
        raise SystemExit(f'Refusing to overwrite existing generated file(s): {names}. Review or back them up, then rerun with --overwrite.')
    out.mkdir(parents=True,exist_ok=True)
    registry.write_text(json.dumps(data,indent=2),encoding='utf-8')
    prompt=(HOME/'prompts/bootstrap.md').read_text(encoding='utf-8')+'\n## Source inventory (not extracted)\n'+''.join('- '+i['path']+' / SHA256 '+i['sha256']+'\n' for i in data)
    context_prompt.write_text(prompt,encoding='utf-8')
    print(f'Inventoried {len(data)} files. Content extraction and requirement approval are manual in V0.1.')
def main():
    p=argparse.ArgumentParser(description='DevHarness V0.1 advisory starter'); p.add_argument('command',choices=['init','ingest','doctor']); p.add_argument('--project',default='.'); p.add_argument('--overwrite',action='store_true',help='replace existing generated inventory and prompt files (ingest only)'); a=p.parse_args(); project=Path(a.project).resolve()
    if a.command=='init': initialize(project)
    elif a.command=='ingest': ingest(project,overwrite=a.overwrite)
    else:
        print('Python',sys.version.split()[0]); print('Project',project); print('Git:',shutil.which('git') or 'not installed'); print('Graphviz:',shutil.which('dot') or 'optional / not installed'); print('GitHub CLI:',shutil.which('gh') or 'optional / not installed'); print('Mode: advisory; no agent execution or scheduling.')
if __name__=='__main__': main()
