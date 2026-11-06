"""Prepara blobs canónicos del checkpoint, sin credenciales ni escritura remota."""
from pathlib import Path
import subprocess,json,base64,hashlib,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base',default='c35d2b974799d1b17d44e9ac597d43dfe0686710',help='Checkpoint local cuyo árbol ya está publicado en el fork')
args=parser.parse_args()
R=Path(__file__).resolve().parents[1];BASE=args.base
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
tree=git('rev-parse','HEAD^{tree}').decode().strip();head=git('rev-parse','HEAD').decode().strip()
entries={}
for item in git('ls-tree','-rz','--full-tree','HEAD').split(b'\0'):
 if not item:continue
 h,p=item.split(b'\t',1);mode,typ,sha=h.decode().split();entries[p.decode()]=(mode,typ,sha)
files=[];blobs={}
folder=R/'tmp/upload-B02';folder.mkdir(exist_ok=True)
for p in git('diff','--name-only','--no-renames','-z',BASE,'HEAD').split(b'\0'):
 if not p:continue
 p=p.decode()
 if p not in entries:files.append(dict(path=p,mode='100644',type='blob',sha=None));continue
 mode,typ,sha=entries[p];data=git('show','HEAD:'+p)
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha
 assert len(data)<100*1024*1024,(p,len(data))
 files.append(dict(path=p,mode=mode,type=typ,sha=sha))
 if sha not in blobs:
  dest=folder/(sha+'.b64');dest.write_bytes(base64.b64encode(data));blobs[sha]=dict(sha=sha,size=len(data),base64_size=dest.stat().st_size,file=dest.relative_to(R).as_posix())
out=dict(base=BASE,head=head,tree=tree,base_tree=git('rev-parse',BASE+'^{tree}').decode().strip(),files=files,blobs=list(blobs.values()))
(R/'tmp/publicacion-B02.json').write_text(json.dumps(out),encoding='utf8')
print(json.dumps(dict(head=head,tree=tree,rutas=len(files),blobs=len(blobs),bytes=sum(x['size'] for x in blobs.values()),mayor=max(x['size'] for x in blobs.values()))))
