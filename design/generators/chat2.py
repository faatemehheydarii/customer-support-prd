import sys, os
sys.argv=['x']
exec(open('/home/claude/work/gen.py',encoding='utf-8').read().split('# ---------- chat ----------')[0])
OUT='/home/claude/canvas/project'
CSS=f'''html,body{{overflow:hidden}}
.grp{{display:flex;flex-direction:column;gap:4px;max-width:85%}}
.grp.me{{align-self:flex-end;align-items:flex-end}}
.grp.them{{align-self:flex-start;align-items:flex-start}}
.bub{{padding:10px 14px;border-radius:18px;font-size:16px;line-height:26px}}
.me .bub{{background:{C['sec']};color:{C['secfg']}}}
.me .bub.tail{{border-end-end-radius:6px}}
.them .bub{{background:{C['card']};border:1px solid {C['border']}}}
.them .bub.tail{{border-end-start-radius:6px}}
.meta{{font-size:12px;line-height:18px;color:{C['mutedfg']};padding:0 4px;display:flex;align-items:center;gap:4px}}
.who-h{{color:{C['deep']};font-weight:600}}
.qr{{display:flex;flex-direction:column;gap:8px;align-self:stretch;margin-top:4px}}
.qr-row{{display:flex;flex-wrap:wrap;align-items:center;gap:8px}}
.qr-lab{{font-size:12px;line-height:18px;color:{C['mutedfg']};min-width:28px}}
.chip{{min-height:44px;padding:0 18px;border-radius:999px;border:1px solid {C['border']};background:{C['card']};color:{C['fg']};font-size:15px;font-weight:500;cursor:pointer}}
.chip:hover{{border-color:{C['pri']};color:{C['pri']}}}
.chip.on{{background:{C['sec']};border-color:{C['sec']};color:{C['secfg']};display:inline-flex;align-items:center;gap:6px;cursor:default}}
.chip.cta{{background:{C['pri']};border-color:{C['pri']};color:#fff;display:inline-flex;align-items:center;gap:8px}}
.day{{align-self:center;font-size:12px;line-height:18px;color:{C['mutedfg']};padding:2px 10px;border-radius:999px;background:{C['muted']}}}
.sys{{align-self:center;font-size:12px;line-height:18px;color:{C['mutedfg']};display:flex;align-items:center;gap:6px}}
.qr-hint{{margin:0;font-size:13px;line-height:20px;color:#4f6260}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}'''
def chat(title, items, status=None, header_btn=True):
    btn=(f'<button style="flex:none;display:inline-flex;align-items:center;gap:6px;height:44px;padding:0 14px;border-radius:999px;border:0;background:{C["sec"]};color:{C["secfg"]};font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer">{I("headset",18)}گفت‌وگو با پشتیبان</button>' if header_btn else '')
    st=''
    if status=='s3':
        st=f'<div role="status" style="display:flex;gap:10px;align-items:flex-start;padding:12px 16px;background:{C["warns"]};color:{C["warn"]};font-size:14px;line-height:22px">{I("clock",20)}<span>درخواستتان برای پشتیبانی ثبت شده است. پیام‌هایتان را همین‌جا بنویسید؛ پشتیبان همه را می‌بیند.</span></div>'
    if status=='s4':
        st=f'<div role="status" style="display:flex;gap:10px;align-items:flex-start;padding:12px 16px;background:#e8f5ec;color:#166534;font-size:14px;line-height:22px">{I("headset",20)}<span>پشتیبان فروشگاه در گفت‌وگوست. پیام‌هایتان را همین‌جا بنویسید.</span></div>'
    body=f'''<div style="width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;background:{C['bg']};overflow:hidden">
<header style="display:flex;align-items:center;gap:16px;height:64px;box-sizing:border-box;padding:0 16px;background:{C['card']};border-bottom:1px solid {C['border']}">

<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:2px">
<div style="font-size:16px;line-height:22px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">فروشگاه نمایشی</div>
<div style="font-size:12px;line-height:16px;color:{C['mutedfg']};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">نسخه نمایشی</div>
</div>
{btn}
</header>
{st}
<main style="flex:1;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;gap:20px;padding:20px 16px">
{items}
</main>
<footer style="padding:10px 16px 24px;background:{C['card']};border-top:1px solid {C['border']}">
<div style="display:flex;gap:8px;align-items:center">
<label style="flex:1;display:flex"><span class="sr">پیام</span>
<textarea rows="1" placeholder="پیامتان را بنویسید…" style="flex:1;resize:none;height:44px;box-sizing:border-box;padding:9px 16px;border:1px solid {C['input']};border-radius:22px;font-family:inherit;font-size:16px;line-height:24px;color:{C['fg']};background:{C['card']}"></textarea></label>
<button aria-label="ارسال" disabled style="flex:none;width:44px;height:44px;border-radius:999px;border:0;background:{C['muted']};color:{C['mutedfg']};display:flex;align-items:center;justify-content:center">{I('send',20)}</button>
</div>
</footer>
</div>'''
    return doc(title, body, 390, 844, CSS)
def me(*texts, t='۱۰:۳۱'):
    return '<div class="grp me">'+''.join(f'<div class="bub{" tail" if i==len(texts)-1 else ""}">{x}</div>' for i,x in enumerate(texts))+f'<span class="meta">{t}</span></div>'
def bot(*texts, t='۱۰:۳۲', qr=''):
    g='<div class="grp them">'+''.join(f'<div class="bub{" tail" if i==len(texts)-1 else ""}">{x}</div>' for i,x in enumerate(texts))+f'<span class="meta">دستیار · {t}</span></div>'
    return g+(f'<section class="act" aria-label="{"پیشنهاد شروع" if "موجودی محصول" in qr else "پاسخ سریع"}">{qr}</section>' if qr else '')
def human(*texts, t='۱۰:۴۶'):
    return '<div class="grp them">'+''.join(f'<div class="bub{" tail" if i==len(texts)-1 else ""}">{x}</div>' for i,x in enumerate(texts))+f'<span class="meta"><span class="who-h">پشتیبان فروشگاه</span> · {t}</span></div>'
def rows(*rs): return '<div class="qr">'+''.join(rs)+'</div>'
def row(label,*chips):
    lab=f'<span class="qr-lab">{label}</span>' if label else ''
    return f'<div class="qr-row" role="group" aria-label="{label or "پاسخ سریع"}">{lab}'+''.join(chips)+'</div>'
def chip(t): return f'<button class="chip">{t}</button>'
def chip_on(t): return f'<button class="chip on" disabled aria-pressed="true">{I("check",16)}{t}</button>'
DAY='<div class="day">امروز</div>'
f={}
f['Chat-Welcome.dc.html']=chat('صفحه گفت‌وگو — خوش‌آمد', bot('سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید.','هر وقت خواستید، می‌توانید با پشتیبان انسانی هم صحبت کنید.',t='۱۰:۳۰',qr=rows(row('',chip('موجودی محصول'),chip('هزینه و زمان ارسال')),row('',chip('پیگیری سفارش'),chip('مرجوعی کالا')))))
f['Chat-Clarify.dc.html']=chat('صفحه گفت‌وگو — رفع ابهام', DAY+me('سلام، مانتو الف رو دارید؟')+bot('این مانتو در سایزهای S، M، L و رنگ‌های مشکی و کرم هست. کدام سایز و رنگ را می‌خواهید؟',t='۱۰:۳۱',qr=rows(row('سایز',chip('S'),chip('M'),chip('L')),row('رنگ',chip('مشکی'),chip('کرم')),'<p class="qr-hint">سایز و رنگ را انتخاب کنید؛ با انتخاب هر دو، پیام فرستاده می‌شود.</p>')))
f['Chat-Answer.dc.html']=chat('صفحه گفت‌وگو — پاسخ موجودی و تأیید حل', me('مانتو الف مشکی، سایز M موجوده؟')+bot('مانتو الف، مشکی، M طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ موجود است.<span style="display:block;margin-top:6px;font-size:14px;line-height:22px;color:'+C['mutedfg']+'">این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.</span>','جواب سؤالتان را گرفتید؟',qr=rows(row('',chip('بله، ممنون'),chip('نه، هنوز نه')))))
f['Chat-Registered.dc.html']=chat('صفحه گفت‌وگو — درخواست ثبت شد (موجودی نامشخص)', me('مانتو ب سرمه‌ای سایز L موجوده؟',t='۱۰:۴۰')+bot('الان نمی‌توانم با اطمینان بگویم مانتو ب، سرمه‌ای، L موجود است یا نه، چون اطلاعات موجودی آن به‌روز نیست. از همکارانم در پشتیبانی می‌پرسم.','درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.',t='۱۰:۴۰')+me('ممنون، منتظرم',t='۱۰:۴۱'),status='s3',header_btn=False)
f['Chat-Human.dc.html']=chat('صفحه گفت‌وگو — پشتیبان در گفت‌وگو', me('مانتو ب سرمه‌ای سایز L موجوده؟',t='۱۰:۴۰')+bot('درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.',t='۱۰:۴۰')+f'<div class="sys">{I("headset",14)}پشتیبان فروشگاه به گفت‌وگو پیوست</div>'+human('سلام، از انبار پرسیدم؛ سرمه‌ای سایز L موجود است.','می‌خواهید لینک خریدش را برایتان بفرستم؟')+me('بله لطفاً',t='۱۰:۴۷'),status='s4',header_btn=False)
f['Chat-Error.dc.html']=chat('صفحه گفت‌وگو — خطای سرویس', me('هزینه ارسال به شیراز چقدره؟',t='۱۰:۵۰')+bot('الان نمی‌توانم به پیامتان جواب بدهم. می‌توانید کمی بعد دوباره بپرسید یا همین حالا با پشتیبان صحبت کنید.',t='۱۰:۵۰',qr=rows(row('',f'<button class="chip cta">{I("headset",18)}گفت‌وگو با پشتیبان</button>'))))
for k,v in f.items(): open(os.path.join(OUT,k),'w',encoding='utf-8').write(v)
print('ok',len(f))
