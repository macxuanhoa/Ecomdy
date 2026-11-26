from pathlib import Path
import subprocess
for source in sorted((Path(__file__).resolve().parents[1]/'docs/diagrams').glob('*.dot')):
    for fmt in ('svg','png'):
        subprocess.run(['dot','-T'+fmt,str(source),'-o',str(source.with_suffix('.'+fmt))],check=True)
