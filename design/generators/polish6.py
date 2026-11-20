"""polish6 (CH-52): customer chat — customer messages on the right, assistant/agent on the left;
default store image (generic shopping bag; product domain still open, D-01); textarea scrollbar only when overflowing.
Idempotent. Runs on canvas dir and on proto/screens (Chat files only)."""
import re, glob, os, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
BAG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 7h12l1 13H5L6 7z'/%3E%3Cpath d='M9 9V6a3 3 0 0 1 6 0v3'/%3E%3C/svg%3E"
PERSON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='1.8' stroke-linecap='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6'/%3E%3C/svg%3E"
CSS6 = f'''/*polish6*/
.grp.me{{align-self:flex-start!important;align-items:flex-start!important}}
.grp.them{{align-self:flex-end!important;align-items:flex-end!important;padding-inline-start:0!important;padding-inline-end:38px}}
.grp.them::before{{inset-inline-start:auto!important;inset-inline-end:0;content:""!important;background:#ec9a55 url("{BAG}") center/16px no-repeat!important}}
.grp.them:has(.who-h)::before{{background:#0b3b38 url("{PERSON}") center/16px no-repeat!important}}
.me .bub.tail{{border-end-end-radius:18px!important;border-end-start-radius:6px!important}}
.them .bub.tail{{border-end-start-radius:18px!important;border-end-end-radius:6px!important}}
.store-mark{{font-size:0!important;color:transparent!important;background:#ec9a55 url("{BAG}") center/55% no-repeat!important}}
textarea{{scrollbar-width:none}}
textarea::-webkit-scrollbar{{width:0!important;height:0!important}}
textarea.scroll,textarea[aria-invalid]{{scrollbar-width:thin}}
textarea.scroll::-webkit-scrollbar,textarea[aria-invalid]::-webkit-scrollbar{{width:6px!important}}
/*endpolish6*/'''
n = 0
for f in glob.glob(os.path.join(DIR, '*Chat-*.html')):
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'/\*polish6\*/.*?/\*endpolish6\*/\n?', '', s, flags=re.S)
    i = s.rfind('</style>')
    s = s[:i] + CSS6 + '\n' + s[i:]
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('polish6', n)
