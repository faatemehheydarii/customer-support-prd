import os, json
src=open('/home/claude/work/gen.py',encoding='utf-8').read()
exec(src[:src.find('ADM_CSS=')])        # C, I, doc
exec(src[src.find('ADM_CSS='):src.find('def topbar')])
OUT='/home/claude/canvas/project'
ICX={'menu':'<path d="M4 7h16M4 12h16M4 17h16"/>','close':'<path d="M6 6l12 12M18 6 6 18"/>',
'flag':'<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>','box':'<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
'book':'<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>','gear':'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
'key':'<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M16 7l3 3"/>','chart':'<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
'plus':'<path d="M12 5v14M5 12h14"/>','dl':'<path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/>','info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>'}
_I=I
def I(name,size=20):
    if name in ICX: return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICX[name]}</svg>'
    return _I(name,size)
CSS=ADM_CSS+f'''
.rail a{{display:flex;align-items:center;gap:12px;min-height:44px;padding:0 12px;border-radius:10px;color:{C['fg']};text-decoration:none;font-size:14px}}
.rail a:hover{{background:{C['muted']}}}
.rail a[aria-current="page"]{{background:{C['sec']};color:{C['secfg']};font-weight:600}}
.cnt{{margin-inline-start:auto;min-width:22px;height:22px;padding:0 6px;box-sizing:border-box;border-radius:999px;background:{C['warns']};color:{C['warn']};font-size:12px;line-height:22px;text-align:center;font-weight:600}}
.card{{background:{C['card']};border:1px solid {C['border']};border-radius:14px}}
.lbl{{font-size:14px;font-weight:500;line-height:20px}}
.help{{font-size:12px;line-height:20px;color:{C['mutedfg']}}}
.inp{{box-sizing:border-box;min-height:40px;padding:0 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;color:{C['fg']};background:{C['card']};width:100%}}
textarea.inp{{padding:8px 12px;line-height:24px;resize:vertical}}
.tag{{display:inline-block;padding:0 8px;border-radius:6px;font-size:12px;line-height:22px;font-weight:500;white-space:nowrap}}
.t-warn{{background:{C['warns']};color:{C['warn']}}}.t-dang{{background:{C['dangs']};color:{C['dang']}}}.t-neu{{background:{C['neus']};color:{C['neu']}}}.t-info{{background:{C['infos']};color:{C['info']}}}.t-ok{{background:{C['succs']};color:{C['succ']}}}
.num{{font-variant-numeric:tabular-nums}}
.sw{{display:inline-flex;align-items:center;gap:8px;font-size:14px}}
.sw i{{width:36px;height:20px;border-radius:999px;background:{C['input']};position:relative;display:inline-block}}
.sw i::after{{content:"";position:absolute;top:2px;inset-inline-start:2px;width:16px;height:16px;border-radius:50%;background:#fff}}
.sw.on i{{background:{C['pri']}}}.sw.on i::after{{inset-inline-start:18px}}
.mrow{{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border-bottom:1px solid {C['border']};text-decoration:none;color:{C['fg']}}}
.mrow:last-child{{border-bottom:0}}
h1{{margin:0;font-size:28px;line-height:40px;font-weight:700}}
.m h1{{font-size:22px;line-height:34px}}
h2{{margin:0;font-size:18px;line-height:28px;font-weight:600}}
'''
MENU=[('flag','مغایرت‌ها','dis','۳'),('box','محصولات و گونه‌ها','prod',None),('book','دانش و سیاست','know',None),('gear','تنظیمات','set',None),('key','مجوزها','perm',None),('chart','گزارش','rep',None)]
def navlinks(active):
    return ''.join(f'<a href="#"{" aria-current=\"page\"" if k==active else ""}>{I(ic,20)}{t}{f"<span class=cnt aria-label=\"{c} مورد باز\">{c}</span>" if c else ""}</a>' for ic,t,k,c in MENU)
BAN3=('مسیر تماس جایگزین تنظیم نشده است. اگر ثبت درخواستی شکست بخورد، مشتری راه دیگری برای تماس نخواهد داشت.')
def banner(text, action='رفتن به تنظیمات', mobile=False):
    pad='12px 16px' if mobile else '12px 32px'
    act=f'<button class="btn btn-o" style="min-height:36px">{action}</button>' if action else ''
    return f'<div role="status" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:{pad};background:{C["warns"]};color:{C["warn"]};border-bottom:1px solid #f3dfb8">{I("alert",20)}<p style="flex:1;min-width:220px;margin:0;font-size:14px;line-height:22px;color:{C["fg"]}">{text}</p>{act}</div>'
def shell(active, inner, banners=''):
    return f'''<div style="display:flex;min-height:100vh;background:{C['bg']}">
<aside class="rail" style="width:256px;flex:none;box-sizing:border-box;display:flex;flex-direction:column;gap:4px;padding:20px 12px;background:{C['card']};border-inline-end:1px solid {C['border']}">
<div style="padding:0 12px 20px;margin-bottom:8px;border-bottom:1px solid {C['border']}"><div style="font-weight:700;font-size:16px;line-height:24px">دستیار پشتیبانی</div><div class="help">پنل فروشگاه · فروشگاه نمایشی</div></div>
<nav aria-label="پنل فروشگاه" style="display:flex;flex-direction:column;gap:2px">{navlinks(active)}</nav>
<div style="margin-top:auto;display:flex;align-items:center;gap:8px;padding:12px;border-top:1px solid {C['border']};font-size:14px">{I('user',18)}مریم<span class="help">مالک</span><a href="#" style="margin-inline-start:auto;color:{C['pri']}">خروج</a></div></aside>
<div style="flex:1;min-width:0">{banners}
<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px">{inner}</main></div></div>'''
def mshell(title, inner, banners='', back=None):
    lead=f'<a href="#" aria-label="بازگشت" style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;color:{C["fg"]}">{I("back",22)}</a>' if back else f'<button aria-label="منو" style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;border:0;background:transparent;color:{C["fg"]};position:relative">{I("menu",22)}<span style="position:absolute;top:8px;inset-inline-end:6px;width:8px;height:8px;border-radius:50%;background:{C["warn"]}"></span></button>'
    return f'''<div class="m" style="min-height:100vh;display:flex;flex-direction:column;background:{C['bg']}">
<header style="display:flex;align-items:center;gap:4px;height:56px;padding:0 6px;background:{C['card']};border-bottom:1px solid {C['border']};flex:none">{lead}<div style="flex:1;min-width:0;font-size:16px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{title}</div><span style="padding:0 10px" class="help">فروشگاه نمایشی</span></header>
{banners}<main style="box-sizing:border-box;padding:20px 16px 32px;display:flex;flex-direction:column;gap:16px">{inner}</main></div>'''
def head(t, sub='', right=''):
    s=f'<p style="margin:4px 0 0;color:{C["mutedfg"]};font-size:14px;line-height:22px">{sub}</p>' if sub else ''
    return f'<div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px"><div><h1>{t}</h1>{s}</div>{right}</div>'
def tabs(items, sel=0):
    return f'<div role="tablist" style="display:inline-flex;align-self:flex-start;gap:4px;padding:4px;background:{C["card"]};border:1px solid {C["border"]};border-radius:12px">'+''.join(f'<button class="tab" role="tab" aria-selected="{"true" if i==sel else "false"}">{t}</button>' for i,t in enumerate(items))+'</div>'
REF=f'<div style="display:flex;align-items:center;gap:8px" class="help">به‌روزرسانی: ۲ دقیقه پیش<button class="btn btn-o" style="min-height:36px;color:{C["fg"]}">{I("refresh",16)}تازه‌سازی</button></div>'
def search(ph): return f'<label style="flex:1;min-width:220px;display:flex;align-items:center;gap:8px;min-height:40px;padding:0 12px;border:1px solid {C["input"]};border-radius:10px;background:{C["card"]};color:{C["mutedfg"]}">{I("search",18)}<input aria-label="{ph}" placeholder="{ph}" style="flex:1;min-width:0;border:0;outline:0;font-family:inherit;font-size:14px;background:transparent"></label>'
def tbl(heads, rows):
    return f'<div class="card" style="overflow:hidden"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def mlist(items): return '<div class="card">'+''.join(items)+'</div>'
F={}
def add(name,title,html,w,h,page=True): F[name]=(html,title,w,h,page)
D=lambda t,b,h: doc(t,b,1440,h,CSS)
M=lambda t,b,h: doc(t,b,390,h,CSS+'html,body{overflow:hidden}')
# ---------- SCR-20
DIS=[('مانتو ب · سرمه‌ای · L',('قدیمی شده','warn'),'۵','۱۸ دقیقه پیش','موجود · تأیید ۳۰ ساعت پیش · نسخه ۴'),
('شلوار جین الف · آبی · ۳۲',('اطلاعات متعارض','dang'),'۳','۱ ساعت پیش','دو رکورد فعال: موجود / ناموجود'),
('پیراهن ج · سفید · M',('منبع ندارد','neu'),'۱','دیروز','موجودی ثبت نشده')]
def gname(g):
    n,rest=g.split(' · ',1); return f'<strong style="font-weight:600">{n}</strong><span style="color:{C["mutedfg"]}"> · {rest}</span>'
rows=[[gname(g),f'<span class="tag t-{k}">{t}</span>',f'<span class="num">{n}</span>',f'<span style="color:{C["mutedfg"]}">{last}</span>',f'<span style="font-size:14px">{cur}</span>',f'<span style="display:flex;align-items:center;gap:8px;justify-content:space-between">باز<span style="color:{C["mutedfg"]}">{I("chev",16)}</span></span>'] for g,(t,k),n,last,cur in DIS]
inner=head('موجودی‌هایی که دستیار نتوانست قطعی جواب بدهد','۳ مورد منتظر بررسی · ترتیب: بیشترین رخداد، بعد تازه‌ترین',REF)+tabs(['باز (۳)','بسته'])+tbl(['گونه','نوع','تعداد رخداد','آخرین رخداد','داده فعلی','وضعیت'],rows)
add('Store-Discrepancies.dc.html','SCR-20 · فهرست مغایرت‌ها',D('پنل فروشگاه — مغایرت‌ها',shell('dis',inner,banner(BAN3)),860),1440,860)
mi=[f'<a class="mrow" href="#"><div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start"><div style="font-size:14px;line-height:22px">{gname(g)}</div><span style="color:{C["mutedfg"]};flex:none;margin-top:2px">{I("chev",16)}</span></div><div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center"><span class="tag t-{k}">{t}</span><span class="help num">{n} رخداد · {last}</span></div><div class="help">{cur}</div></a>' for g,(t,k),n,last,cur in DIS]
minner=f'<div><h1>مغایرت‌ها</h1><p style="margin:2px 0 0" class="help">۳ مورد منتظر بررسی</p></div>'+f'<div style="display:flex;align-items:center;justify-content:space-between;gap:8px">{tabs(["باز (۳)","بسته"])}<button class="btn btn-o" aria-label="تازه‌سازی" style="min-height:40px;padding:0 10px;color:{C["fg"]}">{I("refresh",18)}</button></div>'+mlist(mi)
add('M-Store-Discrepancies.dc.html','موبایل · SCR-20',M('مغایرت‌ها',mshell('مغایرت‌ها',minner,banner(BAN3,mobile=True)),844),390,844,False)
# ---------- SCR-21
def field(label, ctrl, help_=''):
    h=f'<span class="help">{help_}</span>' if help_ else ''
    return f'<label style="display:grid;gap:6px"><span class="lbl">{label}</span>{ctrl}{h}</label>'
def radio_seg(opts, sel):
    return f'<div role="radiogroup" style="display:flex;gap:8px">'+''.join(f'<label style="flex:1;display:flex;align-items:center;gap:8px;min-height:44px;padding:0 12px;border:1px solid {C["pri"] if o==sel else C["input"]};border-radius:10px;background:{C["sec"] if o==sel else C["card"]};font-size:14px"><input type="radio" name="st"{" checked" if o==sel else ""} style="width:18px;height:18px;accent-color:{C["pri"]};margin:0">{o}</label>' for o in opts)+'</div>'
def kv2(k,v): return f'<div style="display:grid;gap:2px"><dt class="help">{k}</dt><dd style="margin:0;font-size:14px;line-height:22px">{v}</dd></div>'
CUR=f'''<section class="card" style="padding:20px;display:grid;gap:16px"><h2>داده فعلی</h2>
<dl style="margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px">{kv2('وضعیت','موجود · <span class="num">۴</span> عدد')}{kv2('منبع','فایل موجودی انبار')}{kv2('آخرین تأیید','۲۲ آبان، ۱۰:۱۲ · <span style="color:'+C['warn']+'">۳۰ ساعت پیش</span>')}{kv2('نسخه','۴')}{kv2('تأییدکننده','مریم')}</dl>
<p style="margin:0;display:flex;gap:8px;align-items:flex-start;font-size:14px;line-height:22px;color:{C['warn']}">{I('info',18)}<span>آستانه اعتبار ۲۴ ساعت است؛ این داده قدیمی شده و دستیار به آن تکیه نمی‌کند.</span></p></section>'''
DRAFT=f'''<section style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 16px;border-radius:14px;border:1px dashed {C['input']};background:{C['muted']}"><span class="tag t-neu">پیش‌نویس — در پاسخ استفاده نمی‌شود</span><span style="font-size:14px">ناموجود · <span class="num">۰</span> عدد</span><span class="help">سارا · ۲ ساعت پیش</span></section>'''
ACTS_D=f'<div style="display:flex;flex-wrap:wrap;gap:8px;padding-top:4px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button><button class="btn btn-o">هنوز درست است — تأیید دوباره</button></div><div style="padding-top:14px;border-top:1px solid {C["border"]};display:flex;align-items:center;gap:12px"><button class="btn btn-o" style="color:{C["dang"]};border-color:{C["border"]}">بستن مغایرت بدون اصلاح</button></div>'
FORM=lambda acts: f'''<section class="card" style="padding:20px;display:grid;gap:16px"><h2>اصلاح موجودی</h2>
<div style="display:grid;gap:6px"><span class="lbl">وضعیت</span>{radio_seg(['موجود','ناموجود'],'ناموجود')}</div>
{field('تعداد (اختیاری)','<input class="inp num" value="۰" inputmode="numeric" style="max-width:200px">','عدد صفر یا بیشتر.')}
<p class="help" style="margin:0">با «تأیید»، از پرسش بعدی مشتری دستیار از این اطلاعات استفاده می‌کند.</p>{acts}</section>'''
HIST=[('۴','موجود · ۴','۲۲ آبان، ۱۰:۱۲','مریم','اصلاح'),('۳','موجود · ۴','۲۰ آبان، ۰۹:۴۰','مریم','تأیید دوباره'),('۲','موجود · ۶','۱۷ آبان، ۱۸:۰۵','سارا','اصلاح')]
HTBL=f'<section style="display:grid;gap:12px"><h2>سابقه نسخه‌ها</h2>'+tbl(['نسخه','مقدار','زمان تأیید','عامل','نوع تغییر'],[[f'<span class="num">{a}</span>',b,f'<span class="num">{c}</span>',d,e] for a,b,c,d,e in HIST])+'</section>'
hdr=f'''<div style="display:flex;flex-direction:column;gap:8px"><a href="#" class="btn btn-g" style="align-self:flex-start;padding:0 4px;text-decoration:none;min-height:32px">{I('back',16)}مغایرت‌ها</a>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px"><h1>مانتو ب <span style="font-weight:400;color:{C['mutedfg']}">· سرمه‌ای · L</span></h1><span class="tag t-warn">قدیمی شده</span></div></div>'''
inner=hdr+f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start"><div style="display:grid;gap:16px">{DRAFT}{FORM(ACTS_D)}</div>{CUR}</div>'+HTBL
add('Store-FixInventory.dc.html','SCR-21 · اصلاح موجودی گونه (قدیمی شده + پیش‌نویس)',D('اصلاح موجودی',shell('dis',inner),1080),1440,1080)
ACTS_M=f'<div style="display:grid;gap:8px"><button class="btn btn-p" style="justify-content:center;min-height:44px">تأیید</button><button class="btn btn-o" style="justify-content:center;min-height:44px">ذخیره پیش‌نویس</button><button class="btn btn-o" style="justify-content:center;min-height:44px">هنوز درست است — تأیید دوباره</button><button class="btn btn-g" style="justify-content:center;min-height:44px;color:{C["dang"]}">بستن مغایرت بدون اصلاح</button></div>'
mh=''.join(f'<div class="mrow"><div style="display:flex;justify-content:space-between;font-size:14px"><span>نسخه <span class="num">{a}</span> · {b}</span><span class="help">{e}</span></div><div class="help num">{c} · {d}</div></div>' for a,b,c,d,e in HIST)
minner=f'<div style="display:flex;flex-direction:column;gap:6px"><h1 style="font-size:20px;line-height:30px">مانتو ب <span style="font-weight:400;color:{C["mutedfg"]}">· سرمه‌ای · L</span></h1><span class="tag t-warn" style="align-self:flex-start">قدیمی شده</span></div>'+CUR.replace('repeat(auto-fit,minmax(150px,1fr))','1fr 1fr')+DRAFT+FORM(ACTS_M)+f'<section style="display:grid;gap:10px"><h2>سابقه نسخه‌ها</h2><div class="card">{mh}</div></section>'
add('M-Store-FixInventory.dc.html','موبایل · SCR-21',M('اصلاح موجودی',mshell('اصلاح موجودی',minner,back=True),1640),390,1640,False)
# ---------- SCR-21 conflict variant (desktop only R5 focus) + mobile
CONF=[('موجود · ۳ عدد','۲۳ آبان، ۰۸:۳۰','مریم'),('ناموجود · ۰','۲۳ آبان، ۰۹:۱۵','سارا')]
R5=f'''<section class="card" style="padding:20px;display:grid;gap:12px"><h2>رکوردهای متعارض</h2><p style="margin:0;font-size:14px;line-height:24px">برای این گونه چند اطلاعات متفاوت ثبت شده است. کدام درست است؟</p>'''+''.join(f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 14px;border:1px solid {C["border"]};border-radius:10px"><div style="flex:1;min-width:160px"><div style="font-size:14px;font-weight:600">{v}</div><div class="help num">تأیید {t} · {who}</div></div><button class="btn btn-o">این رکورد درست است</button></div>' for v,t,who in CONF)+'</section>'
hdr2=hdr.replace('مانتو ب <span style="font-weight:400;color:'+C['mutedfg']+'">· سرمه‌ای · L</span>','شلوار جین الف <span style="font-weight:400;color:'+C['mutedfg']+'">· آبی · ۳۲</span>').replace('<span class="tag t-warn">قدیمی شده</span>','<span class="tag t-dang">اطلاعات متعارض</span>')
inner=hdr2+f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start">{R5}{FORM(ACTS_D.replace("<button class=\"btn btn-o\">هنوز درست است — تأیید دوباره</button>",""))}</div>'
add('Store-FixConflict.dc.html','SCR-21 · اطلاعات متعارض (R5)',D('اصلاح موجودی — تعارض',shell('dis',inner),760),1440,760)
minner=f'<div style="display:flex;flex-direction:column;gap:6px"><h1 style="font-size:20px;line-height:30px">شلوار جین الف <span style="font-weight:400;color:{C["mutedfg"]}">· آبی · ۳۲</span></h1><span class="tag t-dang" style="align-self:flex-start">اطلاعات متعارض</span></div>'+R5.replace('class="btn btn-o">این','class="btn btn-o" style="flex:1 1 100%;justify-content:center;min-height:44px">این')
add('M-Store-FixConflict.dc.html','موبایل · SCR-21 متعارض',M('تعارض',mshell('اصلاح موجودی',minner,back=True),844),390,844,False)
# ---------- SCR-22 list
PRODS=[('مانتو ب','۶','فعال','۱ روز پیش',True),('شلوار جین الف','۸','فعال','۳ ساعت پیش',False),('پیراهن ج','۴','فعال','۵ روز پیش',False),('کت پاییزه د','۵','فعال','۲ روز پیش',False)]
rows=[[f'<strong style="font-weight:600">{n}</strong>',f'<span class="num">{c}</span>',f'<span class="tag t-ok">{s}</span>',f'<span style="color:{C["mutedfg"]}">{t}</span>','<span class="tag t-neu">پیش‌نویس دارد</span>' if d else '',f'<span style="color:{C["mutedfg"]}">{I("chev",16)}</span>'] for n,c,s,t,d in PRODS]
inner=head('محصولات و گونه‌ها','',f'<button class="btn btn-p">{I("plus",18)}افزودن محصول</button>')+f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{tabs(["فعال","غیرفعال","همه"])}{search("جست‌وجوی نام محصول")}</div>'+tbl(['نام محصول','گونه‌ها','وضعیت','آخرین تأیید','',''],rows)
add('Store-Products.dc.html','SCR-22 · محصولات و گونه‌ها — فهرست',D('محصولات',shell('prod',inner),760),1440,760)
mi=[f'<a class="mrow" href="#"><div style="display:flex;justify-content:space-between;align-items:center"><strong style="font-weight:600;font-size:14px">{n}</strong><span style="color:{C["mutedfg"]}">{I("chev",16)}</span></div><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="help num">{c} گونه · تأیید {t}</span>{"<span class=\"tag t-neu\">پیش‌نویس دارد</span>" if d else ""}</div></a>' for n,c,s,t,d in PRODS]
minner=f'<div style="display:flex;justify-content:space-between;align-items:center"><h1>محصولات</h1><button class="btn btn-p" style="min-height:44px">{I("plus",18)}افزودن</button></div>'+search('جست‌وجوی نام محصول')+tabs(['فعال','غیرفعال','همه'])+mlist(mi)
add('M-Store-Products.dc.html','موبایل · SCR-22 فهرست',M('محصولات',mshell('محصولات و گونه‌ها',minner),844),390,844,False)
# ---------- SCR-22 edit
VARS=[('S','سرمه‌ای',True,('موجود','ok')),('M','سرمه‌ای',True,('موجود','ok')),('L','سرمه‌ای',True,('نامشخص','warn')),('M','مشکی',True,('ناموجود','neu')),('L','مشکی',False,('—','neu'))]
attrs=[('جنس','کتان'),('فصل','بهار و تابستان')]
PFORM=f'''<section class="card" style="padding:20px;display:grid;gap:16px"><h2>اطلاعات محصول</h2>
{field('نام *','<input class="inp" value="مانتو ب">')}
<div style="display:grid;gap:8px"><span class="lbl">ویژگی‌ها</span>'''+''.join(f'<div style="display:grid;grid-template-columns:1fr 1.4fr;gap:8px"><input class="inp" aria-label="ویژگی" value="{a}"><input class="inp" aria-label="مقدار" value="{b}"></div>' for a,b in attrs)+f'''<button class="btn btn-g" style="justify-self:start;padding:0 4px">{I('plus',16)}افزودن ویژگی</button></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">{field('قیمت (تومان)','<input class="inp num" value="۱٬۸۵۰٬۰۰۰">')}{field('تخفیف (اختیاری)','<input class="inp num" placeholder="مثلاً ۱۰٪">')}</div>
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:10px;background:{C['muted']}"><span class="sw on"><i></i>فعال</span><span class="help">غیرفعال: این محصول دیگر به مشتری‌ها پیشنهاد نمی‌شود.</span></div>
<div style="display:flex;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div></section>'''
vrows=[[s,c,f'<span class="sw{" on" if a else ""}"><i></i>{"فعال" if a else "غیرفعال"}</span>',f'<span class="tag t-{k}">{st}</span>',f'<button class="btn btn-g" style="min-height:32px;padding:0 6px">اصلاح موجودی</button>'] for s,c,a,(st,k) in VARS]
VSEC=f'<section style="display:grid;gap:12px"><div style="display:flex;justify-content:space-between;align-items:center"><h2>گونه‌ها</h2><button class="btn btn-o" style="min-height:36px">{I("plus",16)}افزودن گونه</button></div>'+tbl(['سایز','رنگ','وضعیت','موجودی','' ],vrows)+'<p class="help" style="margin:0">ستون موجودی نتیجه فعلی بررسی اعتبار است؛ «نامشخص» یعنی دستیار درباره این گونه جواب قطعی نمی‌دهد.</p></section>'
phdr=f'''<div style="display:flex;flex-direction:column;gap:8px"><a href="#" class="btn btn-g" style="align-self:flex-start;padding:0 4px;text-decoration:none;min-height:32px">{I('back',16)}محصولات و گونه‌ها</a>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px"><h1>مانتو ب</h1><span class="tag t-ok">فعال</span><span class="help num">نسخه ۷</span></div></div>'''
inner=phdr+f'<div style="display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:20px;align-items:start">{PFORM}{VSEC}</div>'
add('Store-ProductEdit.dc.html','SCR-22 · ویرایش محصول',D('ویرایش محصول',shell('prod',inner),900),1440,900)
mv=''.join(f'<div class="mrow"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:14px;font-weight:600">{c} · {s}</span><span class="tag t-{k}">{st}</span></div><div style="display:flex;justify-content:space-between;align-items:center"><span class="sw{" on" if a else ""}"><i></i>{"فعال" if a else "غیرفعال"}</span><button class="btn btn-g" style="min-height:40px;padding:0 6px">اصلاح موجودی</button></div></div>' for s,c,a,(st,k) in VARS)
minner=f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><h1>مانتو ب</h1><span class="tag t-ok">فعال</span><span class="help num">نسخه ۷</span></div>'+PFORM.replace('<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">','<div style="display:grid;gap:12px">').replace('<span class="help">غیرفعال: این محصول دیگر به مشتری‌ها پیشنهاد نمی‌شود.</span>','').replace('<div style="display:flex;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div>','<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><button class="btn btn-p" style="justify-content:center;min-height:44px">تأیید</button><button class="btn btn-o" style="justify-content:center;min-height:44px">ذخیره پیش‌نویس</button></div>')+f'<section style="display:grid;gap:10px"><div style="display:flex;justify-content:space-between;align-items:center"><h2>گونه‌ها</h2><button class="btn btn-o" style="min-height:40px">{I("plus",16)}افزودن گونه</button></div><div class="card">{mv}</div></section>'
add('M-Store-ProductEdit.dc.html','موبایل · SCR-22 ویرایش',M('ویرایش محصول',mshell('مانتو ب',minner,back=True),1640),390,1640,False)
# ---------- SCR-23 list
KN=[('ارسال','سفارش‌های بالای ۲ میلیون تومان ارسال رایگان دارند و بقیه…','۳','بدون انقضا',None,False),('مرجوعی','تا ۷ روز پس از تحویل، کالای استفاده‌نشده با برچسب…','۵','۳۰ آذر ۱۴۰۵',None,True),('راهنمای سایز','سایزهای مانتو بر اساس قد و دور سینه تنظیم شده‌اند…','۲','بدون انقضا',None,False),('تخفیف پاییزه','تا پایان مهر، خرید دو کالا ۱۵٪ تخفیف دارد…','۱','۳۰ مهر ۱۴۰۵','منقضی',False)]
rows=[[f'<strong style="font-weight:600">{s}</strong>',f'<span style="display:block;max-width:380px;overflow:hidden;text-overflow:ellipsis;color:{C["mutedfg"]}">{t}</span>',f'<span class="num">{v}</span>',f'<span class="num">{d}</span>',(f'<span class="tag t-warn">{e}</span> ' if e else '')+('<span class="tag t-neu">پیش‌نویس دارد</span>' if dr else ''),f'<span style="color:{C["mutedfg"]}">{I("chev",16)}</span>'] for s,t,v,d,e,dr in KN]
inner=head('دانش و سیاست','متن‌هایی که دستیار برای پاسخ به پرسش‌های ارسال، مرجوعی و سایز از آن‌ها استفاده می‌کند.',f'<button class="btn btn-p">{I("plus",18)}افزودن</button>')+f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{tabs(["معتبر","منقضی","همه"],2)}{search("جست‌وجو در موضوع و متن")}</div>'+tbl(['موضوع','متن','نسخه','تاریخ اعتبار','',''],rows)
add('Store-Knowledge.dc.html','SCR-23 · دانش و سیاست — فهرست (همه)',D('دانش و سیاست',shell('know',inner),760),1440,760)
mi=[f'<a class="mrow" href="#"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><strong style="font-weight:600;font-size:14px">{s}</strong><span style="display:flex;gap:6px;align-items:center">{f"<span class=\"tag t-warn\">{e}</span>" if e else ""}{"<span class=\"tag t-neu\">پیش‌نویس</span>" if dr else ""}<span style="color:{C["mutedfg"]}">{I("chev",16)}</span></span></div><div class="help" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{t}</div><div class="help num">نسخه {v} · {d}</div></a>' for s,t,v,d,e,dr in KN]
minner=f'<div style="display:flex;justify-content:space-between;align-items:center"><h1>دانش و سیاست</h1><button class="btn btn-p" style="min-height:44px">{I("plus",18)}افزودن</button></div>'+search('جست‌وجو در موضوع و متن')+tabs(['معتبر','منقضی','همه'],2)+mlist(mi)
add('M-Store-Knowledge.dc.html','موبایل · SCR-23 فهرست',M('دانش و سیاست',mshell('دانش و سیاست',minner),844),390,844,False)
# ---------- SCR-23 edit (expired)
KF=f'''<section class="card" style="padding:20px;display:grid;gap:16px">
{field('موضوع *','<input class="inp" value="تخفیف پاییزه" list="topics">','پیشنهادها: ارسال · مرجوعی · راهنمای سایز · پرداخت')}
{field('متن *','<textarea class="inp" rows="6">تا پایان مهر، خرید دو کالا ۱۵٪ تخفیف دارد. تخفیف روی کالاهای حراجی اعمال نمی‌شود.</textarea>','فقط متن ساده. دستیار همین متن را مبنای پاسخ قرار می‌دهد.')}
{field('تاریخ اعتبار (اختیاری)','<input class="inp num" value="۳۰ مهر ۱۴۰۵" style="max-width:220px">','خالی یعنی بدون انقضا.')}
<div style="display:flex;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div></section>'''
EXP=f'<div role="status" style="display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:10px;background:{C["warns"]};color:{C["warn"]};font-size:14px;line-height:22px">{I("alert",18)}<span style="color:{C["fg"]}">تاریخ اعتبار این سیاست گذشته است؛ دستیار از آن استفاده نمی‌کند.</span></div>'
KH=[('۱','۱ مهر ۱۴۰۵، ۱۰:۰۰','مریم')]
KHS=f'<section class="card" style="padding:20px;display:grid;gap:12px;align-content:start"><h2>سابقه نسخه‌ها</h2>'+''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;padding:10px 0;border-top:1px solid {C["border"]}"><span style="font-size:14px">نسخه <span class="num">{a}</span> · <span class="help num">{b} · {c}</span></span><button class="btn btn-g" style="min-height:32px;padding:0 6px">بازکردن</button></div>' for a,b,c in KH)+'</section>'
khdr=f'''<div style="display:flex;flex-direction:column;gap:8px"><a href="#" class="btn btn-g" style="align-self:flex-start;padding:0 4px;text-decoration:none;min-height:32px">{I('back',16)}دانش و سیاست</a><div style="display:flex;align-items:center;gap:12px"><h1>تخفیف پاییزه</h1><span class="tag t-warn">منقضی</span><span class="help num">نسخه ۱</span></div></div>'''
inner=khdr+EXP+f'<div style="display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:20px;align-items:start">{KF}{KHS}</div>'
add('Store-KnowledgeEdit.dc.html','SCR-23 · ویرایش منبع (منقضی)',D('ویرایش منبع',shell('know',inner),820),1440,820)
minner=f'<div style="display:flex;align-items:center;gap:8px"><h1>تخفیف پاییزه</h1><span class="tag t-warn">منقضی</span></div>'+EXP+KF.replace('<div style="display:flex;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div>','<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><button class="btn btn-p" style="justify-content:center;min-height:44px">تأیید</button><button class="btn btn-o" style="justify-content:center;min-height:44px">ذخیره پیش‌نویس</button></div>')+KHS
add('M-Store-KnowledgeEdit.dc.html','موبایل · SCR-23 ویرایش',M('ویرایش منبع',mshell('تخفیف پاییزه',minner,back=True),1100),390,1100,False)
# ---------- SCR-24 settings
def sec(t, body, last, extra='', state=''):
    return f'''<section class="card" style="padding:20px;display:grid;gap:14px"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px"><h2>{t}</h2>{state}</div>{body}
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding-top:14px;border-top:1px solid {C['border']}"><button class="btn btn-p">ذخیره</button>{extra}<span class="help" style="margin-inline-start:auto">{last}</span></div></section>'''
WARN_IN=lambda t: f'<div style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:10px;background:{C["warns"]};font-size:14px;line-height:22px">{I("alert",18).replace("currentColor",C["warn"])}<span>{t}</span></div>'
DAYS=['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه']
def dayrow(d,mobile=False):
    closed=d=='جمعه'; short=d=='پنجشنبه'
    a,b=('۰۹:۰۰','۱۴:۰۰') if short else ('۰۹:۰۰','۱۸:۰۰')
    times='' if closed else f'<span style="display:flex;align-items:center;gap:6px;font-size:14px">از <input class="inp num" value="{a}" style="width:84px;text-align:center"> تا <input class="inp num" value="{b}" style="width:84px;text-align:center"></span>'
    return f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;min-height:44px;padding:4px 0;border-top:1px solid {C["border"]}"><span style="width:72px;font-size:14px;font-weight:500">{d}</span><label class="sw{"" if closed else " on"}"><i></i>{"تعطیل" if closed else "باز"}</label>{times}</div>'
PREV=lambda t: f'<div style="display:grid;gap:6px"><span class="help">پیش‌نمایش پیامی که مشتری می‌بیند</span><div style="padding:10px 14px;border-radius:16px 16px 16px 6px;background:{C["card"]};border:1px solid {C["border"]};font-size:14px;line-height:24px;max-width:420px">{t}</div></div>'
def settings(mobile=False):
    s1=sec('آستانه اعتبار موجودی',WARN_IN('آستانه تنظیم نشده است؛ تا وقتی تنظیم نکنید، دستیار درباره موجودی هیچ گونه‌ای جواب قطعی نمی‌دهد.')+field('اطلاعات موجودی تا چند ساعت پس از آخرین تأیید معتبر است؟',f'<span style="display:flex;align-items:center;gap:8px"><input class="inp num" placeholder="مثلاً ۲۴" style="width:140px"><span style="font-size:14px">ساعت</span></span>','عدد ۱ تا ۷۲۰. پیش‌فرض ندارد.'),'هنوز تنظیم نشده')
    s2=sec('ساعات کاری',f'<p class="help" style="margin:0">اگر ساعات کاری را تنظیم نکنید، به مشتری هیچ زمان پاسخی گفته نمی‌شود. ساعت‌ها به وقت فروشگاه است.</p><div>'+''.join(dayrow(d,mobile) for d in DAYS)+'</div>','آخرین تغییر: مریم، ۲۰ آبان')
    s3=sec('زمان پاسخ خارج از ساعات',f'<div role="radiogroup" style="display:grid;gap:8px"><label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:32px"><input type="radio" name="o" checked style="width:18px;height:18px;accent-color:{C["pri"]};margin:0">از آغاز ساعت کاری بعدی</label><label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:32px"><input type="radio" name="o" style="width:18px;height:18px;accent-color:{C["pri"]};margin:0">متن کوتاه</label></div>'+PREV('درخواستتان ثبت شد. همکاران پشتیبانی از ساعت ۹ صبح شنبه پاسخ می‌دهند.'),'آخرین تغییر: مریم، ۲۰ آبان')
    s4=sec('مسیر تماس جایگزین',WARN_IN('مسیر تماس جایگزین تنظیم نشده است. اگر ثبت درخواستی شکست بخورد، مشتری راه دیگری برای تماس نخواهد داشت.')+field('مسیر تماس','<input class="inp" placeholder="مثلاً شماره ۰۲۱-۰۰۰۰۰۰۰۰ یا آیدی پیام‌رسان">','کوتاه بنویسید؛ عیناً به مشتری نشان داده می‌شود.')+PREV('ثبت درخواست ممکن نشد. لطفاً از راه [مسیر تماس] با ما در تماس باشید.'),'هنوز تنظیم نشده')
    s5=sec('منطقه زمانی',field('منطقه زمانی فروشگاه',f'<select class="inp" style="max-width:320px"><option>تهران (UTC+03:30)</option></select>'),'آخرین تغییر: تیم محصول، ۱۵ آبان')
    return s1,s2,s3,s4,s5
s=settings()
inner=head('تنظیمات فروشگاه','هر بخش جداگانه ذخیره می‌شود.')+f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start"><div style="display:grid;gap:20px">{s[0]}{s[2]}{s[4]}</div><div style="display:grid;gap:20px">{s[1]}{s[3]}</div></div>'
BAN2='آستانه اعتبار موجودی تنظیم نشده است؛ دستیار درباره موجودی جواب قطعی نمی‌دهد.'
add('Store-Settings.dc.html','SCR-24 · تنظیمات فروشگاه',D('تنظیمات',shell('set',inner,banner(BAN2,None)+banner(BAN3,None)),1260),1440,1260)
s=settings(True)
minner='<h1>تنظیمات</h1>'+''.join(x.replace('<button class="btn btn-p">ذخیره</button>','<button class="btn btn-p" style="min-height:44px">ذخیره</button>') for x in s)
minner=minner.replace('style="width:84px;text-align:center"','style="width:72px;text-align:center"')
add('M-Store-Settings.dc.html','موبایل · SCR-24',M('تنظیمات',mshell('تنظیمات',minner),2560),390,2560,False)
# ---------- SCR-25 permissions
ADM=[('سارا',True,True,'مریم · ۱۸ آبان'),('علی',True,False,'مریم · ۱۵ آبان'),('نگار',False,False,'—')]
SW=lambda on: f'<span class="sw{" on" if on else ""}"><i></i>{"بله" if on else "خیر"}</span>'
rows=[[f'<strong style="font-weight:600">{n}</strong>',SW(a),SW(b),f'<span class="help num">{t}</span>'] for n,a,b,t in ADM]
DESC=f'<div class="card" style="padding:16px 20px;display:grid;gap:8px;font-size:14px;line-height:24px"><div><strong style="font-weight:600">اصلاح منبع:</strong> اجازه اصلاح اطلاعات محصولات، موجودی و سیاست‌ها</div><div><strong style="font-weight:600">تغییر آستانه:</strong> اجازه تغییر آستانه اعتبار موجودی</div><div class="help">ساخت و حذف حساب ادمین در این صفحه نیست.</div></div>'
inner=head('مجوزها','تعیین کنید کدام ادمین‌ها می‌توانند اطلاعاتی را که دستیار به مشتری می‌گوید اصلاح کنند.')+DESC+tbl(['ادمین','اصلاح منبع','تغییر آستانه','آخرین تغییر'],rows)
add('Store-Permissions.dc.html','SCR-25 · مجوزها',D('مجوزها',shell('perm',inner),720),1440,720)
mi=[f'<div class="mrow"><div style="display:flex;justify-content:space-between"><strong style="font-weight:600;font-size:14px">{n}</strong><span class="help num">{t}</span></div><div style="display:flex;justify-content:space-between;align-items:center;min-height:40px"><span style="font-size:14px">اصلاح منبع</span>{SW(a)}</div><div style="display:flex;justify-content:space-between;align-items:center;min-height:40px"><span style="font-size:14px">تغییر آستانه</span>{SW(b)}</div></div>' for n,a,b,t in ADM]
minner='<h1>مجوزها</h1>'+DESC+mlist(mi)
add('M-Store-Permissions.dc.html','موبایل · SCR-25',M('مجوزها',mshell('مجوزها',minner),900),390,900,False)
# ---------- SCR-26 report
def kcard(name, val, defi, km, tag=None, warn=False):
    t=f'<span class="tag t-neu" style="align-self:flex-start">{tag}</span>' if tag else ''
    v=f'<div class="num" style="font-size:28px;line-height:36px;font-weight:700;{"color:"+C["dang"] if warn else ""}">{val}</div>' if val else ''
    return f'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;gap:8px"><span class="lbl">{name}</span><span class="help num">{km}</span></div>{v}{t}<span class="help">{defi}</span></div>'
GROUPS=[('گفت‌وگو',[('مکالمه‌ها','۴۸۲','مکالمه‌های آغازشده در بازه','KM-08'),('درخواست‌ها','۶۱۵','درخواست‌های مستقل مشتری','KM-08')]),
('پاسخ دستیار',[('پاسخ‌ها','۱٬۲۴۰','همه پاسخ‌های اطلاعاتی؛ تفکیک نوع در CSV','KM-01'),('نبود پاسخ','۷۴','پاسخ «اطلاعات تأییدشده ندارم»','KM-01'),('پاسخ قالبی','۲۰۸','پیام‌های ثابت سیستم','KM-01'),('صحت پاسخ',None,'این شاخص با برچسب آزمون یا بازبینی محاسبه می‌شود.','KM-01','نیازمند برچسب'),('ادعای حساس',None,'این شاخص با برچسب آزمون یا بازبینی محاسبه می‌شود.','KM-05','نیازمند برچسب')]),
('موجودی',[('پاسخ‌های موجودی','۳۱۲','موجود ۱۸۴ · ناموجود ۴۱ · نامشخص ۸۷','KM-04'),('نامعتبرِ اعلام‌شده قطعی','۰','باید صفر باشد','KM-04')]),
('ارجاع',[('ارجاع‌ها','۹۶','تفکیک علت در CSV','KM-02'),('ارجاع ازدست‌رفته احتمالی','۲','ارجاعی که به صف نرسید','KM-03'),('خطای ثبت ارجاع','۱','ثبتی که شکست خورد','KM-03')]),
('نتیجه',[('نرخ حل','۶۸٪','حل‌شده با تأیید مشتری','KM-06'),('بسته بدون تأیید','۴۱','پاسخ مشتری نیامد یا منصرف شد','KM-07'),('بازگشایی','۱۲','گفت‌وگوهای بسته که دوباره باز شدند','KM-07'),('حل بدون بازگشایی','۹۱٪','بازه ۷ روز — فرض A-16','KM-07')]),
('داده مرجع و بازبینی',[('مغایرت باز / بسته','۳ / ۱۷','موارد در بازه','KM-12'),('میانه بازماندن مغایرت','۹ ساعت','از ثبت تا بستن','KM-12'),('نشانه‌های بازبینی','۵۴','درست ۴۶ · نادرست ۵ · باید به پشتیبان می‌رسید ۳','KM-12')]),
('سرویس مدل',[('خطای سرویس','۳','پاسخ‌هایی که به خطا خوردند','KM-11'),('فراخوانی‌ها','۱٬۸۷۵','درخواست‌ها به سرویس مدل','KM-11'),('هزینه تقریبی','۴۲ دلار','بخشی از هزینه نامعلوم است؛ عدد واقعی بیشتر است.','KM-11','ناقص')])]
def report(mobile=False):
    cols='1fr 1fr' if mobile else 'repeat(4,minmax(0,1fr))'
    out=''
    for g,cards in GROUPS:
        out+=f'<section style="display:grid;gap:10px"><h2>{g}</h2><div style="display:grid;grid-template-columns:{cols};gap:12px">'+''.join(kcard(*c) for c in cards)+'</div></section>'
    return out
HEALTH=f'<div role="status" style="display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:10px;background:{C["warns"]};font-size:14px;line-height:22px">{I("alert",18).replace("currentColor",C["warn"])}<span>رویدادهای ثبت‌نشده در این بازه: <span class="num">۴</span>. عددهای این گزارش ممکن است کمتر از واقعیت باشند.</span></div>'
tools=f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{tabs(["امروز","۷ روز","۳۰ روز","دلخواه"],1)}<button class="btn btn-o" style="color:{C["fg"]}">{I("dl",18)}استخراج CSV</button></div>'
inner=head('گزارش سنجش','۱۷ تا ۲۴ آبان · عدد و جدول؛ شاخص‌های زمان پاسخ انسان فقط در CSV.',tools)+HEALTH+report()
add('Store-Report.dc.html','SCR-26 · گزارش سنجش',D('گزارش',shell('rep',inner),1560),1440,1560)
minner='<h1>گزارش سنجش</h1><p class="help" style="margin:-8px 0 0">۱۷ تا ۲۴ آبان</p>'+tabs(['امروز','۷ روز','۳۰ روز','دلخواه'],1)+f'<button class="btn btn-o" style="justify-content:center;min-height:44px;color:{C["fg"]}">{I("dl",18)}استخراج CSV</button>'+HEALTH+report(True)
add('M-Store-Report.dc.html','موبایل · SCR-26',M('گزارش',mshell('گزارش سنجش',minner),2900),390,2900,False)
# ---------- mobile nav drawer
drawer=f'''<div style="position:relative;height:100vh;background:{C['bg']}"><div style="position:absolute;inset:0;background:rgba(11,59,56,0.32)"></div>
<aside class="rail" role="dialog" aria-label="منو" style="position:absolute;top:0;bottom:0;inset-inline-start:0;width:300px;box-sizing:border-box;display:flex;flex-direction:column;gap:4px;padding:8px 12px 16px;background:{C['card']};box-shadow:0 12px 32px rgba(11,59,56,0.16)">
<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 4px 16px 12px;margin-bottom:8px;border-bottom:1px solid {C['border']}"><div><div style="font-weight:700;font-size:16px;line-height:24px">دستیار پشتیبانی</div><div class="help">پنل فروشگاه · فروشگاه نمایشی</div></div><button aria-label="بستن منو" style="width:44px;height:44px;border:0;background:transparent;display:flex;align-items:center;justify-content:center;color:{C['fg']}">{I('close',22)}</button></div>
<nav style="display:flex;flex-direction:column;gap:2px">{navlinks('dis')}</nav>
<div style="margin-top:auto;display:flex;align-items:center;gap:8px;padding:12px;border-top:1px solid {C['border']};font-size:14px">{I('user',18)}مریم<span class="help">مالک</span><a href="#" style="margin-inline-start:auto;color:{C['pri']}">خروج</a></div></aside></div>'''
add('M-Store-Nav.dc.html','موبایل · منوی پنل',M('منو',drawer,844),390,844,False)
for k,(html,_,_,_,_) in F.items(): open(os.path.join(OUT,k),'w',encoding='utf-8').write(html)
json.dump({k:{'title':t,'w':w,'h':h,'page':p} for k,(_,t,w,h,p) in F.items()},open('/home/claude/work/batch3.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(F))
