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
def emit_json(result, output, label):
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if output:
        try: Path(output).write_text(text,encoding='utf-8')
        except OSError as exc:
            print(f'{label} output error: {exc}',file=sys.stderr); return 1
    print(text,end='')
    return 0

def main():
    p=argparse.ArgumentParser(description='DevHarness advisory starter, deterministic compilers and controlled verification')
    p.add_argument('command',choices=['init','ingest','doctor','route','capabilities','compile','context','scope','verify'])
    p.add_argument('--project',default='.')
    p.add_argument('--task',default='-',help='Task, route or context request JSON file or - for stdin')
    p.add_argument('--output',help='Write JSON to this path')
    p.add_argument('--root',help='Harness root to inspect (capabilities only)')
    p.add_argument('--session-skill',action='append',default=[],help='Observed session capability ID or skill name; repeatable')
    p.add_argument('--strict',action='store_true',help='Fail when a registered tool is BLOCKED (capabilities only)')
    p.add_argument('--recipe',help='Explicit recipe ID (compile only)')
    p.add_argument('--task-type',help='Unique recipe task type (compile only)')
    p.add_argument('--context',help='Optional context request JSON file (compile only)')
    p.add_argument('--overwrite',action='store_true',help='replace existing generated inventory and prompt files (ingest only)')
    a=p.parse_args(); project=Path(a.project).resolve()
    if a.command=='init': initialize(project)
    elif a.command=='ingest': ingest(project,overwrite=a.overwrite)
    elif a.command=='doctor':
        print('Python',sys.version.split()[0]); print('Project',project); print('Git:',shutil.which('git') or 'not installed'); print('Graphviz:',shutil.which('dot') or 'optional / not installed'); print('GitHub CLI:',shutil.which('gh') or 'optional / not installed'); print('Mode: advisory; no agent execution or scheduling.')
    else:
        sys.path.insert(0,str(HOME/'scripts'))
        if a.command=='route':
            import technique_router
            try:
                task=technique_router.load_task(a.task); result=technique_router.route_task(task)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Route input error: {exc}',file=sys.stderr); return 1
            if emit_json(result,a.output,'Route'): return 1
            return {'RECOMMENDED':0,'NO_MATCH':2,'BLOCKED':3}.get(result['state'],1)
        if a.command=='capabilities':
            import capability_doctor
            try: result=capability_doctor.inspect_capabilities(Path(a.root).resolve() if a.root else HOME,a.session_skill)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Capability inspection error: {exc}',file=sys.stderr); return 1
            print(json.dumps(result,indent=2,ensure_ascii=False))
            if result['status']=='FAIL': return 1
            if a.strict and result['registries']['tools']['blocked']: return 2
        elif a.command=='compile':
            import recipe_compiler
            try:
                route=recipe_compiler.load_json(a.task)
                context_request=recipe_compiler.load_json(a.context) if a.context else None
                result=recipe_compiler.compile_recipe(route,a.recipe,a.task_type,context_request,project)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Recipe compile input error: {exc}',file=sys.stderr); return 1
            if emit_json(result,a.output,'Recipe compile'): return 1
            return {'COMPILED':0,'BLOCKED':3}.get(result['state'],1)
        elif a.command=='context':
            import context_compiler
            try: result=context_compiler.compile_context(context_compiler.load_json(a.task),project)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Context compile input error: {exc}',file=sys.stderr); return 1
            if emit_json(result,a.output,'Context compile'): return 1
            return {'COMPILED':0,'BLOCKED':3}.get(result['state'],1)
        elif a.command=='scope':
            import scope_checker
            try: result=scope_checker.check_scope(scope_checker.task_contract.load_json(a.task),project)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Scope input error: {exc}',file=sys.stderr); return 2
            if emit_json(result,a.output,'Scope check'): return 2
            if result.get('errors'): return 2
            return 0 if result['state']=='PASS' else 3
        elif a.command=='verify':
            import verification_runner
            try: result=verification_runner.verify_task(verification_runner.task_contract.load_json(a.task),project)
            except (OSError,ValueError,json.JSONDecodeError) as exc:
                print(f'Verification input error: {exc}',file=sys.stderr); return 2
            if emit_json(result,a.output,'Verification'): return 2
            if result.get('input_error'): return 2
            return {'PASS':0,'FAIL':1,'BLOCKED':3}.get(result['state'],2)
    return 0
if __name__=='__main__': sys.exit(main())
