# Idempotent visual polish applied to every generated screen (run after any generator).
import glob, re, sys
DIR=sys.argv[1] if len(sys.argv)>1 else '/home/claude/canvas/project'
BG_OLD,BG_NEW='#eef5f3','#f7faf9'  # tint reverted per review (2026-11-16)
SCROLL='''/*polish*/
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:#e6ecea;border-radius:999px;margin:6px 0}
::-webkit-scrollbar-thumb{background:#0f766e;border-radius:999px;min-height:28px}
::-webkit-scrollbar-thumb:hover{background:#115e59}
::-webkit-scrollbar-button,::-webkit-scrollbar-corner{display:none;width:0;height:0;background:transparent}
textarea::-webkit-scrollbar{width:6px}
textarea::-webkit-scrollbar-track{margin:8px 0}
@supports not selector(::-webkit-scrollbar){*{scrollbar-width:thin;scrollbar-color:#0f766e #e6ecea}}
svg{flex:none}
.btn svg,.chip svg{display:block}
.chip{display:inline-flex;align-items:center;justify-content:center;gap:8px}
.brand-mark{flex:none;display:inline-flex;align-items:center;justify-content:center;border-radius:10px;background:#14b8a6;color:#fff;font-weight:700}
.store-mark{flex:none;display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:#ec9a55;color:#fff;font-size:18px;font-weight:700}
/*endpolishB*/'''
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
aside.rail .brand-mark{background:#99e2d6}'''
HB_OLD='border-radius:999px;border:0;background:#e7f4f1;color:#0b3b38;font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer'
HB_NEW='border-radius:999px;border:1.5px solid #0f766e;background:#ffffff;color:#0f766e;font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer'
n=0
OLDMARK=f'<span class="brand-mark" style="width:36px;height:36px" aria-hidden="true">{HS}</span>'
for f in glob.glob(DIR+'/*.dc.html')+glob.glob(DIR+'/*.html'):
    s=open(f,encoding='utf-8').read(); o=s
    if '/*endpolishB*/' not in s:
        s=re.sub(r'/\*polish\*/.*?(/\*endpolish\*/|(?=/\*polish2\*/|\n</style>))','',s,count=1,flags=re.S)
        s=s.replace('</style>',SCROLL+'\n</style>',1)
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

# ---- polish3: customer chat visual layer (2026-11-16) ----
P3='''/*polish3*/
header{height:72px!important;background:#0f766e!important;border-bottom:0!important;color:#fff}
header div[style*="color:#4f6260"]{color:#cdeee7!important}
header button[disabled]{background:#d9ece8!important;color:#2f8178!important;border:0!important;opacity:1!important}
header .store-mark{box-shadow:0 0 0 3px rgba(255,255,255,.25)}
header button:not([disabled]){border-color:#fff!important}
main{background:#ffffff!important}
.me .bub{background:#134e4a!important;color:#fff!important}
.them .bub{background:#f1f4f3!important;border:0!important;box-shadow:none!important;color:#0b2422}
.grp.them{position:relative;padding-inline-start:38px}
.grp.them::before{content:"✦";position:absolute;inset-inline-start:0;bottom:22px;width:28px;height:28px;border-radius:50%;background:#0f766e;color:#fff;font-size:13px;line-height:28px;text-align:center}
.grp.them:not(:has(.meta))::before{bottom:6px}
.typing{display:inline-flex!important;align-items:center;gap:8px;min-height:40px;padding:0 14px!important;border-radius:18px;background:#f1f4f3;border:0!important;color:#4f6260;font-size:13px}
.grp.them:has(.who-h)::before{content:"پ";background:#0b3b38;font-weight:700;font-size:14px}
.act{align-self:stretch;margin-top:-4px;padding:14px 16px;border-radius:18px;background:#e8f5ec;border:0;box-shadow:none}
.act .qr{margin:0;gap:12px}
.act .qr-row{gap:8px}
.act .qr-lab{min-width:40px;font-size:13px;font-weight:600;color:#166534}
.act .qr-row:not(:has(.qr-lab)) .chip{flex:1}
.act .chip{min-height:44px;border-color:#c4e2cd;background:#fff;color:#0b2422}
.act .chip.on{background:#fff;border:2px solid #166534;color:#166534;font-weight:600}
.act .chip.cta{background:#0f766e;border-color:#0f766e;color:#fff}
.day,.sys{background:transparent;box-shadow:none;color:#6b7c7a}
footer{border-top:1px solid #edf1f0!important}
footer textarea:not([aria-invalid]){background:#f1f5f4!important;border-color:transparent!important}
footer button[aria-label="ارسال"][disabled]{background:#e7f4f1!important;color:#0f766e!important;opacity:.55}
body{background:#f6f8f7!important}
@media (min-width:700px){body>div[style*="max-width:560px"]{height:calc(100vh - 48px)!important;margin:24px auto!important;border-radius:24px;overflow:hidden;border:1px solid #e3eae8;box-shadow:0 1px 3px rgba(11,59,56,.08),0 16px 40px rgba(11,59,56,.10)}}
/*endpolish3*/'''
HERO='<div class="hero" style="margin-block:auto;align-self:center;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center"><span class="store-mark" aria-hidden="true" style="width:72px;height:72px;font-size:30px;border-radius:22px;box-shadow:none">ف</span><div style="font-size:18px;font-weight:700;line-height:28px;margin-top:6px">فروشگاه نمایشی</div><div style="font-size:13px;line-height:20px;color:#4f6260">دستیار پشتیبانی فروشگاه</div></div>'
COL_OLD='width:560px;height:100vh;margin:0 auto;border-inline:1px solid #d3dcda;'
COL_NEW='width:560px;height:calc(100vh - 48px);margin:24px auto;border-radius:24px;border:1px solid #e3eae8;box-shadow:0 1px 3px rgba(11,59,56,.08),0 16px 40px rgba(11,59,56,.10);'
COL_PREV='width:560px;height:calc(100vh - 48px);margin:24px auto;border-radius:24px;box-shadow:0 24px 60px rgba(0,0,0,.28);'
import os
for f in glob.glob(DIR+'/*Chat-*.html'):
    s=open(f,encoding='utf-8').read(); o=s
    s=re.sub(r'/\*polish3\*/.*?/\*endpolish3\*/\n?','',s,count=1,flags=re.S)
    s=s.replace('</style>',P3+'\n</style>',1)
    s=s.replace(COL_OLD,COL_NEW).replace(COL_PREV,COL_NEW)
    if os.path.basename(f).replace('D-','').startswith('Chat-Welcome') and 'class="hero"' not in s:
        s=s.replace('justify-content:flex-end;gap:20px;padding:20px 16px">','justify-content:flex-end;gap:20px;padding:20px 16px">\n'+HERO,1)
    if s!=o: open(f,'w',encoding='utf-8').write(s); n+=1
print('polish3 total',n)
