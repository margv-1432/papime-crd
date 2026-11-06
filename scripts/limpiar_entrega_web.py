"""Retira duplicados históricos de la web activa, preservando primero sus bytes."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
W=(R/'entregas/web').resolve()
assert W.is_relative_to(R.resolve()) and W.name=='web'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
canonical={}
for folder in [R/'entregas/pdf',R/'assets']:
 for p in folder.rglob('*'):
  if p.is_file() and p.suffix.lower() in ('.pdf','.png','.svg'):
   canonical.setdefault(sha(p),p)
actions=[]
for p in sorted(W.rglob('*')):
 if not p.is_file():continue
 legacy=p.suffix.lower()=='.pdf' or (p.parent.name=='recursos' and p.name.startswith(tuple('F0'+str(i) for i in range(1,8))) and p.suffix.lower() in ('.png','.svg'))
 if not legacy:continue
 assert p.resolve().is_relative_to(W)
 digest=sha(p)
 target=canonical.get(digest)
 if target is None:
  target=R/'entregas/antecedentes/web-B02-previa'/p.relative_to(W)
  assert target.resolve().is_relative_to((R/'entregas/antecedentes').resolve())
  target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert sha(target)==digest
  else:shutil.copy2(p,target)
 assert target.exists() and sha(target)==digest
 actions.append(dict(retirado=p.relative_to(R).as_posix(),conservado_en=target.relative_to(R).as_posix(),sha256=digest))
 p.unlink()
report=R/'seguimiento/limpieza-entrega-web-B02.json'
old=json.loads(report.read_text(encoding='utf8')) if report.exists() else dict(fecha='2026-11-06',decisiones='D25–D28',acciones=[])
known={(a['retirado'],a['sha256']) for a in old['acciones']}
old['acciones'] += [a for a in actions if (a['retirado'],a['sha256']) not in known]
report.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Copias históricas retiradas de web activa:',len(actions))
