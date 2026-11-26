from pathlib import Path
import re, sys
root = Path(__file__).resolve().parents[1]
errors=[]
for md in root.rglob('*.md'):
    if any(p in ('.git','00-original','.venv') for p in md.relative_to(root).parts): continue
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
        if link.startswith(('https://','http://','#','mailto:')): continue
        if not (md.parent / link.split('#')[0]).exists(): errors.append(f'{md.relative_to(root)}: {link}')
for dot in (root/'docs/diagrams').glob('*.dot'):
    for ext in ('.mmd','.png','.svg'):
        if not dot.with_suffix(ext).is_file(): errors.append(f'Missing {dot.with_suffix(ext)}')
print('Validation:', 'PASS' if not errors else '\n'.join(errors))
sys.exit(bool(errors))
