import os, json
src=open('/home/claude/work/chat2.py',encoding='utf-8').read()
exec(src.split("f={}")[0])
OUT='/home/claude/canvas/project'
EXTRA=f'''
.typing{{display:inline-flex;align-items:center;gap:10px;padding:12px 16px;border-radius:18px;border-end-start-radius:6px;background:{C['card']};border:1px solid {C['border']};font-size:14px;line-height:20px;color:{C['mutedfg']}}}
.dots{{display:inline-flex;gap:4px}}.dots i{{width:6px;height:6px;border-radius:50%;background:{C['pri']};opacity:.35;animation:b 1.2s infinite}}
.dots i:nth-child(2){{animation-delay:.2s}}.dots i:nth-child(3){{animation-delay:.4s}}
@keyframes b{{0%,80%,100%{{opacity:.35}}40%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.dots i{{animation:none;opacity:.7}}}}
.spin{{width:14px;height:14px;border-radius:50%;border:2px solid {C['border']};border-top-color:{C['pri']};animation:s .9s linear infinite}}
@keyframes s{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.spin{{animation:none}}}}
.fail{{color:{C['dang']};font-weight:500}}
.lnk{{border:0;background:none;padding:0 2px;min-height:32px;color:{C['pri']};font-family:inherit;font-size:12px;font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}}'''
def chatx(title, items, header='on', footer=None):
    html=chat(title, items, None, True)
    html=html.replace('</style>',EXTRA+'\n</style>',1)
    if header=='disabled':
        html=html.replace(f'background:{C["sec"]};color:{C["secfg"]};font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:pointer">',f'background:{C["muted"]};color:{C["mutedfg"]};font-size:14px;line-height:20px;font-weight:600;white-space:nowrap;cursor:not-allowed" disabled aria-disabled="true">',1)
    if footer:
        i=html.find('<footer'); j=html.find('</footer>')+len('</footer>')
        html=html[:i]+footer+html[j:]
    return html
LONG='سلام. سفارش ۱۲۳۴ رو هفته پیش ثبت کردم و هنوز به دستم نرسیده. توی پیگیری نوشته ارسال شده ولی کد رهگیری کار نمی‌کنه. قبلاً هم یک بار از همین فروشگاه خرید کرده بودم و همه چیز خوب بود، برای همین تعجب کردم. یک مانتو و یک شلوار سفارش دادم، رنگ مانتو سرمه‌ای و سایز L بود و شلوار جین آبی سایز ۳۲. آدرس رو هم دوباره چک کردم درسته. می‌خواستم بدونم دقیقاً کجاست، کی می‌رسه، و اگر گم شده باشه چه کار باید بکنم. ضمناً اگر دیرتر از جمعه برسه دیگه لازمش ندارم چون برای مهمانی می‌خواستم و ممکنه بخوام مرجوعش کنم. شرایط مرجوعی چیه و هزینه ارسال برگشت با کیه؟ اگر بشه هم شماره تماس پیک رو بدید ممنون می‌شم. باز هم ببخشید پیام طولانی شد ولی می‌خواستم همه چیز رو یک‌جا بگم تا مجبور نشید چند بار…'
FOOT_LONG=f'''<footer style="padding:10px 16px 20px;background:{C['card']};border-top:1px solid {C['border']}">
<div style="display:flex;gap:8px;align-items:flex-start">
<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px">
<div style="display:flex;flex-direction:column;border:1px solid {C['dang']};border-radius:20px;background:{C['card']};overflow:hidden">
<label style="display:flex"><span class="sr">پیام</span>
<textarea rows="4" aria-invalid="true" aria-describedby="h12 c12" style="flex:1;margin:0 0 0 8px;resize:none;height:100px;box-sizing:border-box;padding:9px 16px 4px;border:0;outline:0;font-family:inherit;font-size:16px;line-height:24px;color:{C['fg']};background:transparent">{LONG}</textarea></label>
<div style="display:flex;justify-content:flex-end;margin:0 12px;padding:6px 0 8px;border-top:1px solid #f6dada"><span id="c12" style="padding:0 8px;border-radius:999px;background:{C['dangs']};color:{C['dang']};font-size:12px;line-height:20px;font-weight:600;font-variant-numeric:tabular-nums">۱۰۴۲ از ۱۰۰۰</span></div>
</div>
<p id="h12" role="alert" style="margin:0;padding:0 4px;font-size:12px;line-height:18px;color:{C['dang']}">پیامتان طولانی است. لطفاً کوتاه‌ترش کنید یا در چند پیام بفرستید.</p>
</div>
<button aria-label="ارسال" disabled style="flex:none;margin-top:88px;width:44px;height:44px;border-radius:999px;border:0;background:{C['muted']};color:{C['mutedfg']};display:flex;align-items:center;justify-content:center">{I('send',20)}</button>
</div>
</footer>'''
ASK='مانتو الف مشکی، سایز M موجوده؟'
f={}
f['Chat-Typing.dc.html']=('ح۲ · در حال پاسخ',chatx('صفحه گفت‌وگو — در حال پاسخ', DAY+bot('سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید.',t='۱۰:۳۰')+me(ASK)+f'<div class="grp them" role="status" aria-live="polite"><div class="typing"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>در حال نوشتن پاسخ…</div></div>'))
f['Chat-Registering.dc.html']=('ح۵ · در حال ثبت',chatx('صفحه گفت‌وگو — در حال ثبت', me('هزینه ارسال به شیراز چقدره؟',t='۱۰:۵۰')+bot('الان نمی‌توانم به پیامتان جواب بدهم. می‌توانید کمی بعد دوباره بپرسید یا همین حالا با پشتیبان صحبت کنید.',t='۱۰:۵۰',qr=rows(row('',chip_on('گفت‌وگو با پشتیبان'))))+f'<div class="sys" role="status" aria-live="polite"><span class="spin" aria-hidden="true"></span>در حال ثبت درخواستتان…</div>',header='disabled'))
f['Chat-Closed.dc.html']=('ح۸ · بسته (پس از تأیید حل)',chatx('صفحه گفت‌وگو — بسته', me(ASK)+bot('مانتو الف، مشکی، M طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ موجود است.','جواب سؤالتان را گرفتید؟',qr=rows(row('',chip_on('بله، ممنون'),'<button class="chip" disabled style="opacity:.5;cursor:default">نه، هنوز نه</button>')))+bot('خوشحالم که کمک کرد. اگر سؤال دیگری داشتید، همین‌جا بپرسید.',t='۱۰:۳۳')))
f['Chat-RegisterFailed.dc.html']=('ح۱۰ · شکست ثبت (با مسیر جایگزین)',chatx('صفحه گفت‌وگو — شکست ثبت', me('می‌خوام با پشتیبان صحبت کنم',t='۱۰:۵۲')+bot('متأسفانه الان نتوانستم درخواستتان را ثبت کنم. برای پیگیری می‌توانید از این راه با فروشگاه تماس بگیرید: <strong style="font-weight:600">تماس با مسئول جلسه آزمون از طریق تسهیل‌گر</strong>. یا چند دقیقه بعد دوباره امتحان کنید.',t='۱۰:۵۲',qr=rows(row('',f'<button class="chip">{I("refresh",16)}دوباره امتحان کنید</button>')))))
f['Chat-SendFailed.dc.html']=('ح۱۱ · ارسال نشد',chatx('صفحه گفت‌وگو — ارسال نشد', DAY+bot('سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید.',t='۱۰:۳۰')+f'<div class="grp me"><div class="bub tail">{ASK}</div><span class="meta" role="alert"><span class="fail" style="display:inline-flex;align-items:center;gap:4px">{I("alert",14)}ارسال نشد. دوباره بفرستید.</span><button class="lnk">ارسال دوباره</button></span></div>'))
f['Chat-TooLong.dc.html']=('ح۱۲ · پیام بلند',chatx('صفحه گفت‌وگو — پیام بلند', DAY+bot('سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید.',t='۱۰:۳۰'),footer=FOOT_LONG))
meta={}
for k,(t,html) in f.items():
    open(os.path.join(OUT,k),'w',encoding='utf-8').write(html)
    d=html.replace('width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;',f'width:560px;height:100vh;margin:0 auto;border-inline:1px solid {C["border"]};box-sizing:border-box;display:flex;flex-direction:column;').replace('</style>',f'body{{background:{C["muted"]}}}\n</style>',1).replace('"$preview":{"width":390,"height":844}','"$preview":{"width":1440,"height":900}')
    open(os.path.join(OUT,'D-'+k),'w',encoding='utf-8').write(d)
    meta[k]=t
json.dump(meta,open('/home/claude/work/batch5.json','w'),ensure_ascii=False)
print(meta)
