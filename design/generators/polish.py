# Idempotent visual polish applied to every generated screen (run after any generator).
import glob, re, sys
DIR=sys.argv[1] if len(sys.argv)>1 else '/home/claude/canvas/project'
BG_OLD,BG_NEW='#eef5f3','#f7faf9'  # tint reverted per review (2026-11-16)
SCROLL='''/*polish*/
*{scrollbar-width:thin;scrollbar-color:#0f766e transparent}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#0f766e;border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:#115e59}
::-webkit-scrollbar-button{display:none;width:0;height:0}
textarea::-webkit-scrollbar-thumb{background:#7d8e8c}
svg{flex:none}
.btn svg{display:block}
.brand-mark{flex:none;display:inline-flex;align-items:center;justify-content:center;border-radius:10px;background:linear-gradient(135deg,#0f766e 0%,#14b8a6 100%);color:#fff;font-weight:700;box-shadow:inset 0 0 0 1px rgba(255,255,255,.18)}
.store-mark{flex:none;display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#f6c26b 0%,#e8894a 100%);color:#fff;font-size:18px;font-weight:700}'''
REF_OLD='<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>'
REF_NEW='<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M8 16H3v5"/>'
HS='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/></svg>'
MARK='<span class="brand-mark" style="width:32px;height:32px;border-radius:999px" aria-hidden="true" title="جای لوگوی محصول"></span>'

P2='''/*polish2*/
aside.rail{background:#0b3b38!important;border-inline-end-color:#0b3b38!important;color:#e6f2ef}
aside.rail>div{border-color:rgba(230,242,239,.14)!important}
aside.rail .help{color:#9cc9c1}
aside.rail a{color:#e6f2ef}
aside.rail a:hover{background:#155e58}
aside.rail a[aria-current="page"]{background:#155e58;color:#fff;box-shadow:inset -3px 0 0 #99e2d6}
aside.rail>div:last-child a{color:#99e2d6!important}
aside.rail .brand-mark{background:linear-gradient(135deg,#14b8a6 0%,#99e2d6 100%)}'''
HB_OLD='border-radius:999px;border:0;background:#e7f4f1;color:#0b3b38;font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer'
HB_NEW='border-radius:999px;border:1.5px solid #0f766e;background:#ffffff;color:#0f766e;font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer'
n=0
OLDMARK=f'<span class="brand-mark" style="width:36px;height:36px" aria-hidden="true">{HS}</span>'
for f in glob.glob(DIR+'/*.dc.html')+glob.glob(DIR+'/*.html'):
    s=open(f,encoding='utf-8').read(); o=s
    if '/*polish*/' not in s: s=s.replace('</style>',SCROLL+'\n</style>',1)
    if '/*polish2*/' not in s and 'class="rail"' in s: s=s.replace('</style>',P2+'\n</style>',1)
    s=s.replace(HB_OLD,HB_NEW)
    s=s.replace(OLDMARK,MARK)
    s=s.replace(BG_OLD,BG_NEW).replace(REF_OLD,REF_NEW)
    # table header tint
    s=s.replace('color:#0b3b38;background:#e7f4f1;padding:10px 16px;border-bottom:1px solid #d3dcda','color:#4f6260;background:#eef3f2;padding:8px 16px;border-bottom:1px solid #d3dcda')  # reverted
    # chat header: store logo placeholder
    if 'class="store-mark"' not in s:
        s=s.replace('<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:2px">\n<div style="font-size:16px;line-height:22px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">فروشگاه نمایشی',
                    '<span class="store-mark" aria-hidden="true" title="جای لوگوی فروشگاه">ف</span>\n<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:2px">\n<div style="font-size:16px;line-height:22px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">فروشگاه نمایشی')
        s=s.replace('gap:16px;height:64px;box-sizing:border-box;padding:0 16px;background:','gap:12px;height:64px;box-sizing:border-box;padding:0 16px;background:',1)
    if 'class="brand-mark"' not in s:
        # admin top bar
        s=s.replace('<div style="font-weight:700;font-size:16px;line-height:24px;margin-inline-end:16px">دستیار پشتیبانی',
                    f'<div style="display:flex;align-items:center;gap:10px;margin-inline-end:16px">{MARK}<div style="font-weight:700;font-size:16px;line-height:24px">دستیار پشتیبانی',)
        if 'margin-inline-end:16px">'+MARK in s:
            s=s.replace('color:#9cc9c1">پنل ادمین · فروشگاه نمایشی</span></div>','color:#9cc9c1">پنل ادمین · فروشگاه نمایشی</span></div></div>')
        # store rail
        s=s.replace('<div style="font-weight:700;font-size:16px;line-height:24px">دستیار پشتیبانی</div><div class="help">پنل فروشگاه · فروشگاه نمایشی</div>',
                    f'<div style="display:flex;align-items:center;gap:10px">{MARK}<div><div style="font-weight:700;font-size:16px;line-height:24px">دستیار پشتیبانی</div><div class="help">پنل فروشگاه · فروشگاه نمایشی</div></div></div>')
    if s!=o: open(f,'w',encoding='utf-8').write(s); n+=1
print('polished',n)
