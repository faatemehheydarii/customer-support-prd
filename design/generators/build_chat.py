import subprocess, glob, os
D='/home/claude/canvas/project'
subprocess.run(['python3','/home/claude/work/chat2.py'],check=True,capture_output=True)
subprocess.run(['python3','/home/claude/work/chat3.py'],check=True,capture_output=True)
subprocess.run(['python3','/home/claude/work/chat4.py'],check=True,capture_output=True)
for n in ['Chat-Welcome','Chat-Clarify','Chat-Answer','Chat-Registered','Chat-Human','Chat-Error']:
    s=open(f'{D}/{n}.dc.html',encoding='utf-8').read()
    d=s.replace('width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;','width:560px;height:100vh;margin:0 auto;border-inline:1px solid #d3dcda;box-sizing:border-box;display:flex;flex-direction:column;').replace('</style>','body{background:#eef3f2}\n</style>',1).replace('"$preview":{"width":390,"height":844}','"$preview":{"width":1440,"height":900}')
    open(f'{D}/D-{n}.dc.html','w',encoding='utf-8').write(d)
print('built')
