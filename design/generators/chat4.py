"""chat4 (CH-49): new customer chat frames for canvas — partial selection, 'not yet', shipping, order tracking, returns."""
import os, json
src = open('/home/claude/work/chat3.py', encoding='utf-8').read()
exec(src.split("\nf={}\n")[0])
OUT = '/home/claude/canvas/project'
WEL = 'سلام! من دستیار پشتیبانی فروشگاه نمایشی هستم. درباره محصولات، موجودی، ارسال، سفارش یا مرجوعی بپرسید.'
ANS = 'مانتو الف، مشکی، M طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ موجود است.<span style="display:block;margin-top:6px;font-size:14px;line-height:22px;color:' + C['mutedfg'] + '">این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.</span>'
Q = 'جواب سؤالتان را گرفتید؟'
def sel(t): return f'<button class="chip on" aria-pressed="true">{I("check",16)}{t}</button>'
def dim(t): return f'<button class="chip" disabled style="opacity:.5;cursor:default">{t}</button>'
CONF = rows(row('', chip('بله، ممنون'), chip('نه، هنوز نه')))
CTA = f'<button class="chip cta">{I("headset",18)}گفت‌وگو با پشتیبان</button>'
SHIP = 'هزینه ارسال به تهران برای سفارش‌های بالای ۲ میلیون تومان رایگان و برای بقیه ۸۰ هزار تومان است؛ شهرهای دیگر ۱۲۰ هزار تومان.<span style="display:block;margin-top:6px">زمان تقریبی رسیدن: تهران ۱ تا ۲ روز کاری، شهرهای دیگر ۳ تا ۵ روز کاری.</span>'
ASK_ORDER = 'شماره سفارشتان را بفرستید. این شماره در پیامک یا ایمیل تأیید سفارش آمده است.'
f = {}
f['Chat-ClarifyPartial.dc.html'] = ('ح۴ب · رفع ابهام — یکی از دو انتخاب', chatx('صفحه گفت‌وگو — رفع ابهام، انتخاب ناقص',
    DAY + me('سلام، مانتو الف رو دارید؟') + bot('این مانتو در سایزهای S، M، L و رنگ‌های مشکی و کرم هست. کدام سایز و رنگ را می‌خواهید؟', t='۱۰:۳۱',
    qr=rows(row('سایز', chip('S'), sel('M'), chip('L')), row('رنگ', chip('مشکی'), chip('کرم')), '<p class="qr-hint">رنگ را هم انتخاب کنید تا پیام فرستاده شود.</p>'))))
f['Chat-NotYet.dc.html'] = ('ح۳ب · «نه، هنوز نه» ← پیشنهاد ارجاع', chatx('صفحه گفت‌وگو — حل نشد',
    me('مانتو الف مشکی، سایز M موجوده؟') + bot(ANS, Q, qr=rows(row('', dim('بله، ممنون'), chip_on('نه، هنوز نه'))))
    + bot('متأسفم که پاسخ کامل نبود. می‌توانید سؤالتان را دقیق‌تر بپرسید یا با پشتیبان صحبت کنید.', t='۱۰:۳۳', qr=rows(row('', CTA)))))
f['Chat-Shipping.dc.html'] = ('ح۱۳ · هزینه و زمان ارسال', chatx('صفحه گفت‌وگو — هزینه و زمان ارسال',
    DAY + bot(WEL, t='۱۰:۳۰') + me('هزینه و زمان ارسال') + bot(SHIP, Q, qr=CONF)))
f['Chat-Order.dc.html'] = ('ح۱۴ · پیگیری سفارش (پرسیدن شماره)', chatx('صفحه گفت‌وگو — پیگیری سفارش',
    me('پیگیری سفارش', t='۱۰:۳۱') + bot(ASK_ORDER, t='۱۰:۳۱') + me('۱۲۳۴', t='۱۰:۳۲')
    + bot('سفارش ۱۲۳۴ طبق اطلاعات فروشگاه ۲۶ آبان ارسال شده است. زمان تقریبی رسیدن ۱ تا ۳ روز کاری است.', Q, t='۱۰:۳۲', qr=CONF)))
f['Chat-Return.dc.html'] = ('ح۱۵ · مرجوعی کالا (سفارش و کالا)', chatx('صفحه گفت‌وگو — مرجوعی کالا',
    me('مرجوعی کالا', t='۱۰:۳۱') + bot(ASK_ORDER, t='۱۰:۳۱') + me('۵۵۱', t='۱۰:۳۲')
    + bot('در سفارش ۵۵۱ دو کالا هست. کدام را می‌خواهید مرجوع کنید؟', t='۱۰:۳۲', qr=rows(row('', chip_on('مانتو ب سرمه‌ای L'), dim('شلوار جین آبی ۳۲'))))
    + bot('مرجوعی تا ۷ روز پس از تحویل ممکن است، به شرط استفاده‌نشده بودن و داشتن برچسب. سفارش ۵۵۱ دو روز پیش تحویل شده و هنوز در مهلت است.<span style="display:block;margin-top:6px">ثبت مرجوعی را همکاران پشتیبانی انجام می‌دهند؛ برای ثبت، «گفت‌وگو با پشتیبان» را بزنید.</span>', Q, t='۱۰:۳۳',
          qr=rows(row('', chip('بله، ممنون'), chip('نه، هنوز نه')), row('', CTA)))))
meta = {}
for k, (t, html) in f.items():
    open(os.path.join(OUT, k), 'w', encoding='utf-8').write(html)
    d = html.replace('width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;', f'width:560px;height:100vh;margin:0 auto;border-inline:1px solid {C["border"]};box-sizing:border-box;display:flex;flex-direction:column;').replace('</style>', f'body{{background:{C["muted"]}}}\n</style>', 1).replace('"$preview":{"width":390,"height":844}', '"$preview":{"width":1440,"height":900}')
    open(os.path.join(OUT, 'D-' + k), 'w', encoding='utf-8').write(d)
    meta[k] = t
# canvas boards
cj = os.path.join(OUT, 'canvas.json'); c = json.load(open(cj, encoding='utf-8'))
y = 12960
for k, t in meta.items():
    c['boards'][k] = {'x': 4642, 'y': y, 'w': 390, 'h': 844, 'title': t}
    c['boards']['D-' + k] = {'x': 5112, 'y': y, 'w': 1440, 'h': 900, 'title': 'دسکتاپ · ' + t}
    y += 1080
c['boards']['Bots-Sample.dc.html'] = {'x': 3040, 'y': 2560, 'w': 1440, 'h': 1000, 'title': 'SCR-12 · نمونه ۱۰تایی برای بازبینی', 'expand': 'fill'}
json.dump(c, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
print(meta)
