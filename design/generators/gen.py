import json, datetime, os
OUT='/home/claude/canvas/gen_tmp'
FONT='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&amp;display=swap">'
C=dict(bg='#f7faf9',fg='#142624',card='#ffffff',pri='#0f766e',prih='#115e59',sec='#e7f4f1',secfg='#0b3b38',muted='#eef3f2',mutedfg='#4f6260',border='#d3dcda',input='#7d8e8c',ring='#0d9488',deep='#0b3b38',deepfg='#e6f2ef',deepmuted='#9cc9c1',active='#155e58',mint='#99e2d6',succ='#166534',succs='#e8f5ec',warn='#8a4b06',warns='#fdf1dc',info='#1d4f91',infos='#e8f0fb',dang='#b42318',dangs='#fdecea',neu='#3f4e4c',neus='#edf1f0')
def I(name,size=20):
    p={'headset':'<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
    'send':'<path d="M20 12H5"/><path d="m11 6-6 6 6 6"/>',
    'alert':'<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4"/><path d="M12 17h.01"/>',
    'check':'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'search':'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    'refresh':'<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>',
    'chev':'<path d="m9 6 6 6-6 6"/>','back':'<path d="m9 6 6 6-6 6"/>',
    'pause':'<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>',
    'user':'<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'down':'<path d="m6 9 6 6 6-6"/>','file':'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>'}[name]
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
def doc(title, body, w, h, extra_css=''):
    return f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT}
<style>
body{{margin:0;font-family:Vazirmatn,Tahoma,sans-serif;color:{C['fg']};background:{C['bg']}}}
a{{color:{C['pri']}}}a:hover{{color:{C['prih']}}}
::selection{{background:{C['sec']};color:{C['secfg']}}}
button{{font-family:inherit}}
button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{{outline:2px solid {C['ring']};outline-offset:2px}}
{extra_css}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
# ---------- chat ----------
CHAT_CSS=f'''.msg{{max-width:82%;padding:8px 16px;border-radius:20px;font-size:16px;line-height:28px}}
.asst{{align-self:flex-start;background:{C['card']};border:1px solid {C['border']};border-start-start-radius:6px}}
.adm{{align-self:flex-start;background:{C['sec']};color:{C['secfg']};border-start-start-radius:6px}}
.cust{{align-self:flex-end;background:{C['pri']};color:#fff;border-start-end-radius:6px}}
.sys{{align-self:center;background:{C['muted']};color:{C['mutedfg']};font-size:12px;line-height:20px;padding:4px 12px;border-radius:999px}}
.who{{display:block;font-size:12px;line-height:20px;font-weight:600}}
.meta{{display:block;font-size:12px;line-height:20px;color:{C['mutedfg']};margin-top:2px}}
.cust .meta{{color:{C['sec']}}}
.chip{{min-height:44px;padding:0 16px;border-radius:999px;border:1px solid {C['pri']};background:{C['card']};color:{C['pri']};font-size:14px;cursor:pointer}}
.chip:disabled{{border-color:{C['border']};color:{C['mutedfg']};cursor:default}}'''
def chat(title, msgs, status=None, header_btn=True, composer_hint=None):
    btn = (f'<button style="display:flex;align-items:center;gap:6px;min-height:44px;padding:0 12px;border-radius:10px;border:1px solid {C["pri"]};background:{C["card"]};color:{C["pri"]};font-size:14px;font-weight:500;cursor:pointer">{I("headset",18)}گفت‌وگو با پشتیبان</button>' if header_btn else '')
    st=''
    if status=='s3':
        st=f'<div style="display:flex;gap:8px;align-items:flex-start;padding:10px 16px;background:{C["warns"]};color:{C["warn"]};font-size:14px;line-height:22px">{I("check",18)}<span>درخواستتان برای پشتیبانی ثبت شده است. پیام‌هایتان را همین‌جا بنویسید؛ پشتیبان همه را می‌بیند.</span></div>'
    if status=='s4':
        st=f'<div style="display:flex;gap:8px;align-items:flex-start;padding:10px 16px;background:{C["deep"]};color:#fff;font-size:14px;line-height:22px">{I("headset",18)}<span>پشتیبان فروشگاه در گفت‌وگوست. پیام‌هایتان را همین‌جا بنویسید.</span></div>'
    hint = composer_hint or ''
    body=f'''<div style="width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;background:{C['bg']};overflow:hidden">
<header style="display:flex;align-items:center;gap:12px;padding:12px 16px;background:{C['card']};border-bottom:1px solid {C['border']}">
<div style="width:40px;height:40px;border-radius:999px;background:{C['sec']};color:{C['pri']};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px">ف</div>
<div style="flex:1;min-width:0"><div style="font-size:16px;line-height:24px;font-weight:700">فروشگاه نمایشی</div>
<div style="display:flex;gap:6px;align-items:center;font-size:12px;line-height:20px;color:{C['mutedfg']}">دستیار پشتیبانی<span style="padding:0 6px;border-radius:6px;background:{C['neus']};color:{C['neu']};font-weight:500">نسخه نمایشی</span></div></div>
{btn}
</header>
{st}
<main style="flex:1;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;gap:8px;padding:16px">
{msgs}
</main>
<footer style="padding:12px 16px 20px;background:{C['card']};border-top:1px solid {C['border']}">
<div style="display:flex;gap:8px;align-items:flex-end">
<label style="flex:1;display:flex"><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">پیام</span>
<textarea rows="1" placeholder="پیامتان را بنویسید…" style="flex:1;resize:none;min-height:44px;box-sizing:border-box;padding:9px 16px;border:1px solid {C['input']};border-radius:22px;font-family:inherit;font-size:16px;line-height:24px;color:{C['fg']};background:{C['card']}"></textarea></label>
<button aria-label="ارسال" style="width:44px;height:44px;border-radius:999px;border:0;background:{C['pri']};color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer">{I('send',20)}</button>
</div>{hint}
</footer>
</div>'''
    return doc(title, body, 390, 844, CHAT_CSS)
def A(t,meta='دستیار · ۱۰:۳۲',extra=''): return f'<div class="msg asst">{t}<span class="meta">{meta}</span>{extra}</div>'
def U(t,meta='۱۰:۳۱'): return f'<div class="msg cust">{t}<span class="meta">{meta}</span></div>'
def S(t): return f'<div class="sys">{t}</div>'
def chips(*labels, disabled=False):
    d=' disabled' if disabled else ''
    return '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">'+''.join(f'<button class="chip"{d}>{l}</button>' for l in labels)+'</div>'
files={}
files['Chat-Welcome.dc.html']=chat('صفحه گفت‌وگو — خوش‌آمد', A('سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید. هر وقت خواستید، می‌توانید با پشتیبان انسانی هم صحبت کنید.','دستیار · ۱۰:۳۰'))
files['Chat-Clarify.dc.html']=chat('صفحه گفت‌وگو — رفع ابهام', U('سلام، مانتو الف رو دارید؟','۱۰:۳۱')+A('این مانتو الف در سایزهای S، M، L و رنگ‌های مشکی، کرم هست. کدام را می‌خواهید؟','دستیار · ۱۰:۳۱',chips('سایز S','سایز M','سایز L','مشکی','کرم')))
files['Chat-Answer.dc.html']=chat('صفحه گفت‌وگو — پاسخ موجودی و تأیید حل', U('مانتو الف رو دارید؟','۱۰:۳۱')+A('این مانتو الف در سایزهای S، M، L و رنگ‌های مشکی، کرم هست. کدام را می‌خواهید؟','دستیار · ۱۰:۳۱',chips('سایز M','مشکی',disabled=True))+U('مشکی، سایز M','۱۰:۳۲')+A('مانتو الف، مشکی، M طبق اطلاعات فروشگاه در امروز، ساعت ۱۰:۳۰ موجود است. این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.')+A('جواب سؤالتان را گرفتید؟','دستیار · ۱۰:۳۲',chips('بله، ممنون','نه، هنوز نه')))
files['Chat-Registered.dc.html']=chat('صفحه گفت‌وگو — درخواست ثبت شد (موجودی نامشخص)', U('مانتو ب سرمه‌ای سایز L موجوده؟','۱۰:۴۰')+A('الان نمی‌توانم با اطمینان بگویم مانتو ب، سرمه‌ای، L موجود است یا نه، چون اطلاعات موجودی آن به‌روز نیست. از همکارانم در پشتیبانی می‌پرسم.','دستیار · ۱۰:۴۰')+A('درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.','دستیار · ۱۰:۴۰')+U('ممنون، منتظرم','۱۰:۴۱'),status='s3',header_btn=False)
files['Chat-Human.dc.html']=chat('صفحه گفت‌وگو — پشتیبان در گفت‌وگو', U('مانتو ب سرمه‌ای سایز L موجوده؟','۱۰:۴۰')+A('درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.','دستیار · ۱۰:۴۰')+S('پشتیبان فروشگاه به گفت‌وگو پیوست')+f'<div class="msg adm"><span class="who">پشتیبان فروشگاه</span>سلام، الان از انبار پرسیدم؛ سرمه‌ای سایز L یک عدد مانده. می‌خواهید برایتان لینک خرید را بفرستم؟<span class="meta">۱۰:۴۶</span></div>'+U('بله لطفاً','۱۰:۴۷'),status='s4',header_btn=False)
files['Chat-Error.dc.html']=chat('صفحه گفت‌وگو — خطای سرویس', U('هزینه ارسال به شیراز چقدره؟','۱۰:۵۰')+A('الان نمی‌توانم به پیامتان جواب بدهم. می‌توانید کمی بعد دوباره بپرسید یا همین حالا با پشتیبان صحبت کنید.','دستیار · ۱۰:۵۰',f'<div style="margin-top:8px"><button class="chip" style="display:inline-flex;align-items:center;gap:6px">{I("headset",18)}گفت‌وگو با پشتیبان</button></div>'))
for k,v in files.items(): open(os.path.join(OUT,k),'w',encoding='utf-8').write(v)
print(list(files))
# ---------- admin ----------
ADM_CSS=f'''.tab{{min-height:40px;padding:0 14px;border-radius:10px;border:1px solid transparent;background:transparent;color:{C['fg']};font-size:14px;font-weight:500;cursor:pointer}}
.tab[aria-selected="true"]{{background:{C['sec']};color:{C['secfg']};border-color:{C['pri']}}}
.badge{{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:6px;font-size:12px;line-height:20px;font-weight:500;white-space:nowrap}}
.badge::before{{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}}
.s3{{background:{C['warns']};color:{C['warn']}}}.s4{{background:{C['deep']};color:#fff}}.s5{{background:{C['succs']};color:{C['succ']}}}.s1{{background:{C['sec']};color:{C['secfg']}}}
table{{border-collapse:separate;border-spacing:0;width:100%}}
th{{text-align:start;font-weight:500;font-size:14px;color:{C['mutedfg']};background:{C['muted']};padding:8px 16px;border-bottom:1px solid {C['border']};white-space:nowrap}}
td{{padding:12px 16px;border-bottom:1px solid {C['border']};font-size:14px;line-height:24px;vertical-align:middle;white-space:nowrap}}
tbody tr:hover td{{background:{C['bg']}}}
.btn{{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 16px;border-radius:10px;font-size:14px;font-weight:500;cursor:pointer;border:1px solid transparent;white-space:nowrap}}
.btn-p{{background:{C['pri']};color:#fff}}.btn-p:hover{{background:{C['prih']}}}
.btn-s{{background:{C['sec']};color:{C['secfg']}}}
.btn-o{{background:{C['card']};color:{C['fg']};border-color:{C['input']}}}
.btn-g{{background:transparent;color:{C['pri']}}}
.nav{{display:flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border-radius:10px;color:{C['deepfg']};text-decoration:none;font-size:14px}}
.nav:hover{{background:{C['active']};color:#fff}}

.grp{{display:flex;flex-direction:column;gap:4px;max-width:72%}}
.grp.me{{align-self:flex-end;align-items:flex-end}}
.grp.them{{align-self:flex-start;align-items:flex-start}}
.bub{{padding:8px 14px;border-radius:16px;font-size:14px;line-height:24px}}
.me .bub{{background:{C['sec']};color:{C['secfg']}}}
.me .bub.tail{{border-end-end-radius:6px}}
.them .bub{{background:{C['card']};border:1px solid {C['border']}}}
.them .bub.tail{{border-end-start-radius:6px}}
.meta{{font-size:12px;line-height:18px;color:{C['mutedfg']};padding:0 4px}}
.who-h{{color:{C['deep']};font-weight:600}}
.src{{display:block;margin-top:4px;font-size:12px;line-height:18px;color:{C['mutedfg']}}}
.nav[aria-current="page"]{{background:{C['active']};color:#fff;font-weight:600;box-shadow:inset 0 -3px 0 {C['mint']}}}'''
def topbar(active):
    def nav(label,key,count):
        cur=' aria-current="page"' if key==active else ''
        return f'<a class="nav" href="#"{cur}>{label}<span style="font-size:12px;color:{C["deepmuted"]}">{count}</span></a>'
    return f'''<header style="display:flex;flex-wrap:wrap;align-items:center;gap:16px;padding:10px 24px;background:{C['deep']};color:{C['deepfg']}">
<div style="font-weight:700;font-size:16px;line-height:24px;margin-inline-end:16px">دستیار پشتیبانی<span style="display:block;font-weight:400;font-size:12px;line-height:18px;color:{C['deepmuted']}">پنل ادمین · فروشگاه نمایشی</span></div>
<nav aria-label="پنل ادمین" style="display:flex;gap:4px">{nav('صف اقدام','queue','۶')}{nav('گفت‌وگوهای دستیار','bot','۱۲')}</nav>
<div style="margin-inline-start:auto;display:flex;align-items:center;gap:12px">
<span style="display:flex;align-items:center;gap:8px;font-size:14px"><span style="width:8px;height:8px;border-radius:50%;background:{C['mint']}"></span>پاسخ خودکار: فعال</span>
<button class="btn" style="background:transparent;color:{C['deepfg']};border-color:{C['deepmuted']}">{I('pause',16)}توقف پاسخ خودکار</button>
<span style="width:1px;height:24px;background:{C['active']}"></span>
<span style="display:flex;align-items:center;gap:6px;font-size:14px">{I('user',18)}سارا</span>
<a href="#" style="color:{C['mint']};font-size:14px">خروج</a>
</div></header>'''
rows=[('s3','نیازمند انسان','درخواست مشتری','می‌خواستم مرجوعی سفارش ۵۵۱ را ثبت کنم، مهلتش تمام نشده؟','#۱۰۴۲','۲۴ دقیقه','بدون مسئول',True),
('s3','نیازمند انسان','پاسخ معتبر نبود','مانتو ب سرمه‌ای سایز L موجوده؟','#۱۰۴۴','۱۸ دقیقه','بدون مسئول',True),
('s3','نیازمند انسان','خارج از اختیار دستیار','برای خرید ده‌تایی تخفیف می‌دهید؟','#۱۰۴۷','۱۱ دقیقه','بدون مسئول',False),
('s3','نیازمند انسان','ابهام حل نشد','همون شلوار قبلی که دیدم رو می‌خوام','#۱۰۴۹','۶ دقیقه','بدون مسئول',True),
('s4','در حال رسیدگی','درخواست مشتری','باشه، پس منتظر لینک می‌مونم','#۱۰۳۸','۳ دقیقه','سارا',False),
('s4','در حال رسیدگی','تحویل به درخواست ادمین','سفارشم هنوز ارسال نشده؟','#۱۰۳۵','۱ دقیقه','مریم',True)]
def row(r):
    cls,st,reason,last,cid,wait,owner,unread=r
    un=f'<span style="display:inline-flex;align-items:center;gap:6px;color:{C["pri"]};font-weight:600;font-size:12px"><span style="width:8px;height:8px;border-radius:50%;background:{C["pri"]}"></span>پیام تازه</span>' if unread else ''
    ow=f'<span style="color:{C["mutedfg"]}">{owner}</span>' if owner=='بدون مسئول' else owner
    fw='600' if unread else '400'
    return f'<tr><td><span class="badge {cls}">{st}</span></td><td>{reason}</td><td style="white-space:normal;width:100%"><a href="Conversation.dc.html" style="color:{C["fg"]};text-decoration:none;font-weight:{fw};display:block;max-width:440px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{last}</a><span style="font-size:12px;line-height:18px;color:{C["mutedfg"]};font-variant-numeric:tabular-nums">{cid}</span></td><td style="font-variant-numeric:tabular-nums">{wait}</td><td>{ow}</td><td>{un}</td></tr>'
queue=f'''<div style="min-height:100vh;display:flex;flex-direction:column;background:{C['bg']}">
{topbar('queue')}
<main style="width:100%;max-width:1280px;margin:0 auto;box-sizing:border-box;padding:32px 24px;display:flex;flex-direction:column;gap:20px">
<div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px">
<div><h1 style="margin:0;font-size:28px;line-height:40px;font-weight:700">صف اقدام</h1>
<p style="margin:0;color:{C['mutedfg']};font-size:14px">قدیمی‌ترین درخواست بالای صف است.</p></div>
<div style="display:flex;align-items:center;gap:8px;color:{C['mutedfg']};font-size:12px">آخرین به‌روزرسانی: ۳ دقیقه پیش<button class="btn btn-o" style="min-height:36px">{I('refresh',16)}تازه‌سازی</button></div>
</div>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">
<div role="tablist" aria-label="فیلتر وضعیت" style="display:flex;gap:4px;padding:4px;background:{C['card']};border:1px solid {C['border']};border-radius:12px">
<button class="tab" role="tab" aria-selected="true">همه (۶)</button><button class="tab" role="tab" aria-selected="false">نیازمند انسان (۴)</button><button class="tab" role="tab" aria-selected="false">در حال رسیدگی (۲)</button><button class="tab" role="tab" aria-selected="false">بسته</button></div>
<label style="display:flex;align-items:center;gap:8px;font-size:14px">مسئول
<select style="min-height:40px;padding:0 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;background:{C['card']};color:{C['fg']}"><option>همه</option><option>بدون مسئول</option><option>من</option></select></label>
<label style="flex:1;min-width:240px;display:flex;align-items:center;gap:8px;min-height:40px;padding:0 12px;border:1px solid {C['input']};border-radius:10px;background:{C['card']};color:{C['mutedfg']}">{I('search',18)}<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">جست‌وجو در صف</span><input placeholder="شناسه، متن پیام یا نام محصول" style="flex:1;border:0;outline:0;font-family:inherit;font-size:14px;background:transparent;color:{C['fg']}"></label>
</div>
<div style="overflow-x:auto;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<table><thead><tr><th>وضعیت</th><th>علت</th><th>آخرین پیام</th><th>زمان انتظار</th><th>مسئول</th><th><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">خوانده‌نشده</span></th></tr></thead>
<tbody>{''.join(row(r) for r in rows)}</tbody></table></div>
</main></div>'''
files2={'Main.dc.html':doc('پنل ادمین — صف اقدام',queue,1440,900,ADM_CSS)}
# conversation (owner view)
def hm(sender,text,meta,kind='a',src=None):
    styles={'c':f'background:{C["pri"]};color:#fff;align-self:flex-end;border-start-end-radius:6px','a':f'background:{C["card"]};border:1px solid {C["border"]};align-self:flex-start;border-start-start-radius:6px','h':f'background:{C["sec"]};color:{C["secfg"]};align-self:flex-start;border-start-start-radius:6px'}[kind]
    mc='#e7f4f1' if kind=='c' else C['mutedfg']
    s=f'<span style="display:block;font-size:12px;line-height:18px;color:{C["mutedfg"]};margin-top:4px">{src}</span>' if src else ''
    return f'<div style="max-width:72%;padding:8px 14px;border-radius:16px;font-size:14px;line-height:24px;{styles}"><span style="display:block;font-size:12px;line-height:18px;font-weight:600;opacity:.85">{sender}</span>{text}<span style="display:block;font-size:12px;line-height:18px;color:{mc}">{meta}</span>{s}</div>'
def sysl(t): return f'<div style="align-self:center;font-size:12px;line-height:18px;color:{C["mutedfg"]}">{t}</div>'
def kv(k,v): return f'<div style="display:grid;gap:2px"><dt style="font-size:12px;line-height:18px;color:{C["mutedfg"]}">{k}</dt><dd style="margin:0;font-size:14px;line-height:22px">{v}</dd></div>'
conv=f'''<div style="min-height:100vh;display:flex;flex-direction:column;background:{C['bg']}">
{topbar('queue')}
<main style="width:100%;max-width:1280px;margin:0 auto;box-sizing:border-box;padding:24px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">
<a href="Main.dc.html" class="btn btn-g" style="text-decoration:none;padding:0 8px">{I('back',16)}بازگشت به صف</a>
<span style="width:1px;height:24px;background:{C['border']}"></span>
<span style="font-variant-numeric:tabular-nums;color:{C['mutedfg']}">#۱۰۴۴</span>
<span class="badge s4">در حال رسیدگی</span>
<span style="font-size:14px">مسئول: <strong>سارا (شما)</strong></span>
<span style="font-size:14px;color:{C['mutedfg']}">علت: پاسخ معتبر نبود</span>
</div>
<div role="status" style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:{C['succs']};color:{C['succ']};font-size:14px">{I('check',18)}این گفت‌وگو حالا با شماست.</div>
<div style="display:flex;flex-wrap:wrap;gap:8px;padding:12px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<button class="btn btn-p">درخواست تأیید از مشتری</button>
<button class="btn btn-o">بستن — حل شد</button>
<button class="btn btn-o">بستن بدون تأیید</button>
<button class="btn btn-g" style="margin-inline-start:auto">واگذاری به دستیار</button>
</div>
<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start">
<section aria-label="تاریخچه گفت‌وگو" style="flex:999 1 560px;min-width:0;display:flex;flex-direction:column;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<div style="display:flex;flex-direction:column;gap:20px;padding:24px 20px;min-height:420px;justify-content:flex-end;background:{C['bg']};border-radius:14px 14px 0 0">
<div class="grp me"><div class="bub tail">مانتو ب سرمه‌ای سایز L موجوده؟</div><span class="meta">مشتری · ۱۰:۴۰</span></div>
<div class="grp them"><div class="bub">الان نمی‌توانم با اطمینان بگویم مانتو ب، سرمه‌ای، L موجود است یا نه، چون اطلاعات موجودی آن به‌روز نیست. از همکارانم در پشتیبانی می‌پرسم.<span class="src">پاسخ قالبی · موجودی: قدیمی شده (آخرین تأیید ۳ روز پیش)</span></div><div class="bub tail">درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.<span class="src">پاسخ قالبی</span></div><span class="meta">دستیار · ۱۰:۴۰</span></div>
{sysl('ارجاع ثبت شد · علت: پاسخ معتبر نبود · ۱۰:۴۰')}
<div class="grp me"><div class="bub tail">ممنون، منتظرم</div><span class="meta">مشتری · ۱۰:۴۱</span></div>
{sysl('سارا گفت‌وگو را تحویل گرفت · ۱۰:۵۸')}
</div>
<div style="padding:16px;border-top:1px solid {C['border']};display:grid;gap:8px">
<label for="reply" style="font-size:14px;font-weight:500">پاسخ به مشتری</label>
<textarea id="reply" rows="3" placeholder="پاسخ را بنویسید…" style="resize:vertical;box-sizing:border-box;width:100%;padding:10px 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;line-height:24px;color:{C['fg']}"></textarea>
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;color:{C['mutedfg']}">نام شما به مشتری نشان داده نمی‌شود؛ مشتری «پشتیبان فروشگاه» را می‌بیند.</span><button class="btn btn-p">ارسال</button></div>
</div>
</section>
<aside aria-label="خلاصه درخواست" style="flex:1 1 320px;min-width:0;max-width:380px;display:flex;flex-direction:column;gap:14px;padding:20px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<h2 style="margin:0;font-size:18px;line-height:28px;font-weight:600">خلاصه درخواست</h2>
<p style="margin:0;padding:10px 12px;border-radius:10px;background:{C['muted']};font-size:14px;line-height:24px">مشتری موجودی مانتو ب، سرمه‌ای، سایز L را می‌خواهد. دستیار به‌دلیل قدیمی‌بودن داده موجودی پاسخ قطعی نداد.<span style="display:block;margin-top:4px;font-size:12px;line-height:18px;color:{C['mutedfg']}">خلاصه خودکار — برای جزئیات دقیق، تاریخچه را ببینید.</span></p>
<dl style="margin:0;display:grid;gap:12px">
{kv('آخرین درخواست مشتری','«مانتو ب سرمه‌ای سایز L موجوده؟»')}
{kv('گونه مرتبط','مانتو ب · سرمه‌ای · L')}
{kv('موجودی ثبت‌شده','<span class="badge" style="background:'+C['warns']+';color:'+C['warn']+'">نامشخص</span> آخرین تأیید: ۳ روز پیش')}
{kv('پاسخ‌های داده‌شده','۲ پاسخ قالبی')}
{kv('علت ارجاع','پاسخ معتبر نبود')}
{kv('اطلاعات ناقص','ندارد')}
</dl>
<a href="#" style="font-size:14px">اصلاح موجودی این گونه در پنل فروشگاه</a>
</aside>
</div>
</main></div>'''
files2['Conversation.dc.html']=doc('پنل ادمین — نمای مکالمه (مالک)',conv,1440,1000,ADM_CSS)
for k,v in files2.items(): open(os.path.join(OUT,k),'w',encoding='utf-8').write(v)
# ---------- canvas.json ----------
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
boards={}; order=[]
x=0
chat_titles=[('Chat-Welcome.dc.html','ح۱ · خوش‌آمد'),('Chat-Clarify.dc.html','ح۴ · رفع ابهام'),('Chat-Answer.dc.html','ح۳ · پاسخ موجودی + تأیید حل'),('Chat-Registered.dc.html','ح۶ · نامشخص ← ثبت برای پشتیبانی (S3)'),('Chat-Human.dc.html','ح۷ · پشتیبان در گفت‌وگو (S4)'),('Chat-Error.dc.html','ح۹ · خطای سرویس')]
boards['Main.dc.html']={'x':0,'y':0,'w':1440,'h':900,'title':'SCR-10 · صف اقدام','expand':'fill'}
boards['Conversation.dc.html']={'x':1520,'y':0,'w':1440,'h':1000,'title':'SCR-11 · نمای مکالمه — مالک','expand':'fill'}
order=['Main.dc.html','Conversation.dc.html']
for i,(f,t) in enumerate(chat_titles):
    boards[f]={'x':i*(390+80),'y':1000+120+300,'w':390,'h':844,'title':t}
    order.append(f)
canvas={'v':3,'createdOnFiles':{'v':1,'at':now},'title':'دستیار پشتیبانی — طراحی صفحه‌ها','launch':{'view':'canvas'},'pages':[],'boards':boards,'order':order,
'notes':{'adm':{'x':0,'y':-300,'text':'پنل ادمین (دسکتاپ)','kind':'title1','maxW':2960},
'chat':{'x':0,'y':1120,'text':'صفحه گفت‌وگوی مشتری (موبایل)','kind':'title1','maxW':2740}},
'designSystems':[{'title':'دستیار پشتیبانی','namespace':'dastyar','artifact':'https://claude.ai/artifact/Wnt4fEfrQCmQeeE28BiSzb','version':None,'copiedAt':now}]}
json.dump(canvas,open(os.path.join(OUT,'canvas.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
