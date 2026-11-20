"""polish7 (CH-53): store-panel wording — menu «بررسی موجودی», intro line, action hint per type,
customer-facing column names, «منتظر تأیید» instead of «پیش‌نویس دارد». Idempotent; runs on canvas dir or proto/screens."""
import re, glob, os, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
REP = [('پنل فروشگاه — مغایرت‌ها','پنل فروشگاه — بررسی موجودی'),
       ('بستن مغایرت بدون اصلاح','بستن بدون اصلاح'),
       ('"بستن مغایرت"','"بستن مورد"'),('>بستن مغایرت<','>بستن مورد<'),
       ('>مغایرت‌ها<','>بررسی موجودی<'),('</svg>مغایرت‌ها<','</svg>بررسی موجودی<'),('"مغایرت‌ها"','"بررسی موجودی"'),
       ('۳ مورد منتظر بررسی · ترتیب: بیشترین رخداد، بعد تازه‌ترین','دستیار درباره این محصولات به مشتری جواب قطعی نداده است؛ داده را تأیید یا اصلاح کنید تا دوباره جواب بدهد. ترتیب: بیشترین پرسش، بعد تازه‌ترین'),
       ('>تعداد رخداد<','>مشتری‌هایی که پرسیدند<'),('>آخرین رخداد<','>آخرین پرسش<'),
       ('پیش‌نویس — در پاسخ استفاده نمی‌شود','منتظر تأیید — دستیار تا تأیید از آن استفاده نمی‌کند'),
       ('>پیش‌نویس دارد<',' title="تا تأیید نشود، دستیار از آن استفاده نمی‌کند">منتظر تأیید<'),
       ('مغایرت باز / بسته','موارد بررسی موجودی: باز / بسته'),('میانه بازماندن مغایرت','میانه زمان تا بررسی'),
       ('>مغایرت بازی نیست.<','>موردی منتظر بررسی نیست؛ دستیار برای همه موجودی‌ها داده معتبر دارد.<')]
ACT = {'قدیمی شده':'دوباره تأیید یا اصلاح کنید','منبع ندارد':'موجودی را ثبت کنید','اطلاعات متعارض':'رکورد درست را انتخاب کنید',
       'زمان تأیید نامعتبر':'دوباره تأیید کنید','آستانه تنظیم نشده':'آستانه اعتبار را در تنظیمات تعیین کنید'}
n = 0
files = [f for f in glob.glob(os.path.join(DIR,'*.html')) if re.search(r'(^|/)(M-)?(Store-|SW\d|Login-Store|Denied)', f)]
for f in files:
    s = open(f, encoding='utf-8').read(); o = s
    for a,b in REP:
        if a.startswith('>پیش‌نویس دارد'):
            s = s.replace('class="tag t-neu">پیش‌نویس دارد<', 'class="tag t-neu"'+b)
        else: s = s.replace(a,b)
    s = s.replace('class="tag t-neu" title="تا تأیید','class="tag t-warn" title="تا تأیید')
    if 'Discrepancies' in f and 'hint7' not in s:
        for t,h in ACT.items():
            s = re.sub(r'(<span class="tag t-\w+"[^>]*>'+t+r'</span>)(?=</td>|<span style="display:flex)',
                       r'<span class="hint7" style="display:flex;flex-direction:column;align-items:flex-start;gap:4px">\1<span style="font-size:12px;line-height:18px;color:#64748b">'+h+'</span></span>', s)
    if s != o: open(f,'w',encoding='utf-8').write(s); n += 1
print('polish7', n, 'of', len(files))
