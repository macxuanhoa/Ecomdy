from pathlib import Path
import re, sys
root = Path(__file__).resolve().parents[1]
errors=[]
for md in root.rglob('*.md'):
    if any(p in ('.git','00-original','.venv') for p in md.relative_to(root).parts): continue
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
        if link.startswith(('https://','http://','#','mailto:')): continue
        if not (md.parent / link.split('#')[0]).exists(): errors.append(f'{md.relative_to(root)}: {link}')
for folder, prefix in [(root/'docs/diagrams','ECOMDY'),(root/'.harness/docs/diagrams','HARNESS')]:
    gallery=folder/'README.md'
    gallery_text=gallery.read_text(encoding='utf-8') if gallery.exists() else ''
    ids=[]
    for source in sorted(folder.glob('*.mmd')):
        text=source.read_text(encoding='utf-8')
        match=re.search(r'(?:%%|//)\s*(?:Diagram ID:|ID:)\s*([A-Z]+-D\d+)\s*\|\s*Version:\s*([^|]+)\|\s*State:\s*([^\r\n]+)',text[:1000])
        if not match: errors.append(f'{source.relative_to(root)}: missing diagram ID/version/state metadata')
        else:
            diagram_id,version,state=match.groups()
            if not diagram_id.startswith(prefix+'-D'): errors.append(f'{source.relative_to(root)}: unexpected diagram ID {diagram_id}')
            if not version.strip() or not state.strip(): errors.append(f'{source.relative_to(root)}: empty version or state')
            ids.append(diagram_id)
        if source.name not in gallery_text: errors.append(f'{source.relative_to(root)}: source is not listed in {gallery.relative_to(root)}')
    if len(ids)!=len(set(ids)): errors.append(f'{folder.relative_to(root)}: duplicate Mermaid diagram IDs')
    for dot in folder.glob('*.dot'):
        for ext in ('.mmd','.png','.svg'):
            if not dot.with_suffix(ext).is_file(): errors.append(f'Missing {dot.with_suffix(ext)}')
        text=dot.read_text(encoding='utf-8')
        match=re.search(r'//\s*Diagram ID:\s*([A-Z]+-D\d+)\s*\|\s*Version:\s*([^|]+)\|\s*State:\s*([^\r\n]+)',text[:1000])
        if not match: errors.append(f'{dot.relative_to(root)}: missing diagram ID/version/state metadata')
print('Validation:', 'PASS' if not errors else '\n'.join(errors))
sys.exit(bool(errors))
