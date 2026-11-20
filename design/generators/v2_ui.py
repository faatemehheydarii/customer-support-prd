"""v2 — CH-61 (ChatGPT P1, part 5): canvas artboards for shopping assistance.
New: Chat-Products, Chat-Alternative, Chat-Rescue (+ D- desktop), Store-Attributes (SCR-28).
Changed: store menu item, Store-ProductEdit (attributes + images), Store-Settings (assistant capabilities, tone),
Store-Report (topics, «خرید و درخواست‌ها»), Conversation* (summary: topic, assistant actions, next action; review marks),
admin status labels (DEC-337). Idempotent: works from the v2 canvas files in DIR (default /home/claude/canvas/project)."""
import os, re, sys, json, shutil
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
P = lambda n: os.path.join(DIR, n)
rd = lambda n: open(P(n), encoding='utf-8').read()
def wr(n, s): open(P(n), 'w', encoding='utf-8').write(s)
FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
def money(n): return f'{n:,}'.replace(',', '٬').translate(FA) + ' تومان'
SVG = lambda d, sz=18: f'<svg width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
GARMENT = '<path d="M9 3 4 6l1.5 4L8 9v12h8V9l2.5 1L20 6l-5-3a3 3 0 0 1-6 0z"/>'
TAG_ICON = '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>'

PLUS16 = SVG('<path d="M12 5v14M5 12h14"/>', 16)
PLUS22 = SVG('<path d="M12 5v14M5 12h14"/>', 22)
# ---------------------------------------------------------------- chat
CSS_CHAT = '''/*v2cards*/
.pc{display:grid;gap:8px;margin-top:10px}
.pcard{display:flex;gap:10px;align-items:stretch;padding:8px;border-radius:14px;background:#ffffff;border:1px solid #d3dcda;color:#142624}
.pimg{flex:none;width:60px;height:76px;border-radius:10px;background:#eef3f2;display:flex;align-items:center;justify-content:center;color:#7d8e8c}
.pbody{display:grid;gap:2px;min-width:0;align-content:start}
.pname{font-weight:600;font-size:15px;line-height:22px}
.pprice{font-size:14px;line-height:20px}
.pwhy{font-size:13px;line-height:20px;color:#4f6260}
.pdiff{font-size:13px;line-height:20px;color:#0b3b38;background:#e7f4f1;border-radius:8px;padding:2px 8px;justify-self:start}
/*endv2cards*/'''

def card(name, variant, price, line, diff=False):
    v = f' · {variant}' if variant else ''
    return (f'<div class="pcard"><span class="pimg" role="img" aria-label="تصویر {name}">{SVG(GARMENT, 26)}</span>'
            f'<span class="pbody"><span class="pname">{name}{v}</span><span class="pprice num">{money(price)}</span>'
            f'<span class="{"pdiff" if diff else "pwhy"}">{line}</span></span></div>')

Q = ('<div class="bub tail">جواب سؤالتان را گرفتید؟</div>')
CHIPS = ('<section class="act" aria-label="پاسخ سریع"><div class="qr"><div class="qr-row" role="group" aria-label="پاسخ سریع">'
         '<button class="chip">بله، ممنون</button><button class="chip">نه، هنوز نه</button></div></div></section>')
def them(html, t='۱۰:۳۲'): return f'<div class="grp them"><div class="bub">{html}</div>{Q}<span class="meta">دستیار · {t}</span></div>{CHIPS}'
def me(t, tm='۱۰:۳۱'): return f'<div class="grp me"><div class="bub tail">{t}</div><span class="meta">{tm}</span></div>'

CHATS = {
 'Chat-Products': ('صفحه گفت‌وگو — پیشنهاد محصول با دلیل (v2)', 'ح۱۶ · پیشنهاد محصول با دلیل (v2)',
   me('سلام، یه مانتو تابستونه برای محل کار می‌خوام، تا سه میلیون')
   + them('این‌ها با خواسته شما جور درمی‌آیند:<div class="pc">'
          + card('مانتو الف', '', 2450000, 'بهار و تابستان · لینن ترکیبی · مناسب محل کار · در بودجه شما')
          + card('مانتو پ', '', 2190000, 'تابستانه · لینن · مناسب محل کار · در بودجه شما')
          + card('مانتو ب', '', 1850000, 'بهار و تابستان · کتان · مناسب محل کار · در بودجه شما')
          + '</div><span style="display:block;margin-top:8px;font-size:14px;line-height:22px;color:#4f6260">برای موجودی هرکدام، رنگ و سایز را بگویید.</span>')),
 'Chat-Alternative': ('صفحه گفت‌وگو — جایگزین برای ناموجود (v2)', 'ح۱۷ · جایگزین برای گونه ناموجود (v2)',
   me('مانتو الف کرم سایز L موجوده؟')
   + them('مانتو الف، کرم، L طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ موجود نیست. این‌ها نزدیک‌ترین گزینه‌های موجود در سایز L هستند:<div class="pc">'
          + card('مانتو الف', 'مشکی · L', 2450000, 'رنگ مشکی به‌جای کرم', True)
          + card('مانتو پ', 'کرم · L', 2190000, 'فرم راسته به‌جای آزاد · لینن · ۲۶۰ هزار تومان ارزان‌تر', True)
          + card('مانتو ت', 'کرم · L', 1750000, 'قد کوتاه به‌جای متوسط · نخی · ۷۰۰ هزار تومان ارزان‌تر', True)
          + '</div><span style="display:block;margin-top:8px;font-size:14px;line-height:22px;color:#4f6260">این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.</span>')),
 'Chat-Rescue': ('صفحه گفت‌وگو — تردید در قیمت (v2)', 'ح۱۸ · کمک در تردید خرید: قیمت (v2)',
   me('مانتو الف رو دیدم ولی یه کم گرونه. ارزون‌تر ندارید؟', '۱۰:۳۴')
   + them('اگر بودجه‌تان کمتر است، این مانتوهای مشابه موجودند:<div class="pc">'
          + card('مانتو پ', '', 2190000, 'لینن · فرم راسته · ۲۶۰ هزار تومان ارزان‌تر', True)
          + card('مانتو ت', '', 1750000, 'نخی · قد کوتاه · ۷۰۰ هزار تومان ارزان‌تر', True)
          + card('مانتو ب', '', 1850000, 'کتان · قد بلند · ۶۰۰ هزار تومان ارزان‌تر', True)
          + '</div>', '۱۰:۳۵')),
}

def chat_board(name, base, title, inner):
    s = rd(base)
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    s = re.sub(r'(<main[^>]*>).*?(</main>)', lambda m: m.group(1) + '\n' + inner + '\n' + m.group(2), s, count=1, flags=re.S)
    if '/*v2cards*/' not in s:
        s = s.replace('</style>', CSS_CHAT + '\n</style>', 1)
    wr(name, s)

for n, (title, _, inner) in CHATS.items():
    chat_board(n + '.dc.html', 'Chat-Answer.dc.html', title, inner)
    chat_board('D-' + n + '.dc.html', 'D-Chat-Answer.dc.html', title, inner)

# ---------------------------------------------------------------- store menu
NAV_ITEM = f'<a href="#">{SVG(TAG_ICON, 20)}ویژگی‌های کاتالوگ</a>'
NAV_RE = re.compile(r'(<a href="#"(?: aria-current="page")?>' + r'<svg[^>]*>(?:(?!</svg>).)*</svg>محصولات و گونه‌ها</a>)', re.S)
def add_nav(s):
    if 'ویژگی‌های کاتالوگ</a>' in s: return s
    return NAV_RE.sub(lambda m: m.group(1) + NAV_ITEM, s, count=1)

# ---------------------------------------------------------------- SCR-28 attributes
ATTRS = [('دسته', 'فهرست مقدار', 'مانتو · شلوار · شال و روسری', 'محصول', True),
         ('جنس', 'فهرست مقدار', 'لینن · لینن ترکیبی · نخی · کتان · کرپ · جین · پشمی · ابریشم مصنوعی', 'محصول', True),
         ('فصل', 'فهرست مقدار (چند انتخاب)', 'بهار · تابستان · پاییز · زمستان', 'محصول', True),
         ('کاربرد', 'فهرست مقدار (چند انتخاب)', 'روزمره · اداری (هم‌ارز: محل کار) · مهمانی', 'محصول', True),
         ('قد', 'فهرست مقدار', 'کوتاه · متوسط · بلند', 'محصول', True),
         ('فرم', 'فهرست مقدار', 'راسته · آزاد · جذب', 'محصول', True),
         ('رنگ', 'فهرست مقدار', 'مشکی · کرم · سرمه‌ای · زیتونی · سفید · طوسی · آبی · آبی روشن · صورتی', 'گونه', True),
         ('سایز', 'فهرست مقدار', 'S · M · L · ۳۰ تا ۴۰ · تک‌سایز', 'گونه', True)]
def attr_rows():
    out = []
    for i, (n, t, v, lv, srch) in enumerate(ATTRS):
        sel = ' style="background:#e7f4f1"' if n == 'کاربرد' else ''
        out.append(f'<tr{sel}><td><strong style="font-weight:600">{n}</strong></td><td>{t}</td><td style="max-width:320px">{v}</td><td>{lv}</td>'
                   f'<td><span class="tag {"t-ok" if srch else "t-neu"}">{"بله" if srch else "خیر"}</span></td><td><span class="tag t-ok">فعال</span></td>'
                   f'<td><button class="btn btn-g" style="min-height:32px;padding:0 6px">ویرایش</button></td></tr>')
    return ''.join(out)
def chip(t, on=False): return f'<span class="tag {"t-ok" if on else "t-neu"}" style="display:inline-flex;gap:6px;align-items:center">{t}</span>'
ATTR_MAIN = (
 '<div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px"><div><h1>ویژگی‌های کاتالوگ</h1>'
 '<p style="margin:4px 0 0;color:#4f6260;font-size:14px;line-height:22px">ویژگی‌هایی که دستیار برای پیشنهاد محصول و جایگزین به کار می‌برد. هر محصول برای این ویژگی‌ها مقدار می‌گیرد.</p></div>'
 f'<button class="btn btn-p">{PLUS16}افزودن ویژگی</button></div>'
 '<div style="display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:20px;align-items:start">'
 '<div class="card" style="overflow:auto"><table><thead><tr><th>ویژگی</th><th>نوع</th><th>مقدارهای مجاز</th><th>سطح</th><th>قابل جست‌وجو</th><th>وضعیت</th><th></th></tr></thead><tbody>'
 + attr_rows() + '</tbody></table></div>'
 '<section class="card" style="padding:20px;display:grid;gap:14px"><h2>ویرایش ویژگی: کاربرد</h2>'
 '<label style="display:grid;gap:6px"><span class="lbl">نام *</span><input class="inp" value="کاربرد"></label>'
 '<label style="display:grid;gap:6px"><span class="lbl">نوع مقدار</span><select class="inp"><option>فهرست مقدار (چند انتخاب)</option><option>فهرست مقدار</option><option>عدد</option><option>متن کوتاه</option></select></label>'
 '<div style="display:grid;gap:8px"><span class="lbl">مقدارهای مجاز</span>'
 '<div style="display:grid;grid-template-columns:1fr 1.3fr;gap:8px"><input class="inp" aria-label="مقدار" value="روزمره"><input class="inp" aria-label="هم‌ارزها" placeholder="هم‌ارزها (اختیاری)"></div>'
 '<div style="display:grid;grid-template-columns:1fr 1.3fr;gap:8px"><input class="inp" aria-label="مقدار" value="اداری"><input class="inp" aria-label="هم‌ارزها" value="محل کار، سر کار"></div>'
 '<div style="display:grid;grid-template-columns:1fr 1.3fr;gap:8px"><input class="inp" aria-label="مقدار" value="مهمانی"><input class="inp" aria-label="هم‌ارزها" value="مهمونی"></div>'
 f'<button class="btn btn-g" style="justify-self:start;padding:0 4px">{PLUS16}افزودن مقدار</button>'
 '<span class="help">هم‌ارزها واژه‌هایی‌اند که مشتری ممکن است بنویسد؛ دستیار آن‌ها را همین مقدار می‌فهمد.</span></div>'
 '<fieldset style="border:0;margin:0;padding:0;display:grid;gap:6px"><legend class="lbl" style="padding:0;margin-bottom:6px">سطح</legend>'
 '<label style="display:flex;gap:8px;align-items:center;font-size:14px"><input type="radio" name="lv" checked> محصول</label>'
 '<label style="display:flex;gap:8px;align-items:center;font-size:14px"><input type="radio" name="lv"> گونه (مثل رنگ و سایز)</label></fieldset>'
 '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:10px;background:#eef3f2"><span class="sw on"><i></i>قابل جست‌وجو</span><span class="help">خاموش: در پیشنهاد و جایگزین به کار نمی‌رود.</span></div>'
 '<p class="help" style="margin:0">ویژگی حذف نمی‌شود؛ اگر دیگر لازم نیست، غیرفعالش کنید.</p>'
 '<div style="display:flex;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div></section></div>')

MAIN = re.compile(r'(<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px">).*?(</main>)', re.S)
def store_board_from(base, name, title, inner, nav_label):
    s = rd(base)
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    s, n = MAIN.subn(lambda m: m.group(1) + inner + m.group(2), s, count=1); assert n == 1, name
    s = re.sub(r'"\$preview":\{"width":1440,"height":\d+\}', '"$preview":{"width":1440,"height":900}', s, count=1)
    s = add_nav(s)
    s = s.replace(' aria-current="page"', '')
    s = s.replace(f'</svg>{nav_label}</a>', f'</svg>{nav_label}</a>', 1)
    s = re.sub(r'(<a href="#")(><svg[^>]*>(?:(?!</svg>).)*</svg>' + re.escape(nav_label) + '</a>)', r'\1 aria-current="page"\2', s, count=1, flags=re.S)
    wr(name, s)

# ---------------------------------------------------------------- product edit: attributes + images
SEL = lambda lab, opts, val: (f'<label style="display:grid;gap:6px"><span class="lbl">{lab}</span><select class="inp">'
                              + ''.join(f'<option{" selected" if o == val else ""}>{o}</option>' for o in opts) + '</select></label>')
ATTR_BLOCK = ('<div style="display:grid;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px"><span class="lbl">ویژگی‌ها</span>'
  '<a href="#" style="font-size:13px">ویژگی‌های کاتالوگ</a></div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">'
  + SEL('دسته', ['مانتو', 'شلوار', 'شال و روسری'], 'مانتو') + SEL('جنس', ['لینن', 'لینن ترکیبی', 'نخی', 'کتان', 'کرپ', 'جین', 'پشمی'], 'کتان')
  + SEL('قد', ['کوتاه', 'متوسط', 'بلند'], 'بلند') + SEL('فرم', ['راسته', 'آزاد', 'جذب'], 'راسته') + '</div>'
  '<div style="display:grid;gap:6px"><span class="lbl">فصل</span><div style="display:flex;flex-wrap:wrap;gap:6px">'
  + ''.join(f'<label class="tag {"t-ok" if x in ("بهار", "تابستان") else "t-neu"}" style="display:inline-flex;gap:6px;align-items:center;min-height:32px;padding:0 10px;cursor:pointer"><input type="checkbox"{" checked" if x in ("بهار", "تابستان") else ""}>{x}</label>' for x in ['بهار', 'تابستان', 'پاییز', 'زمستان'])
  + '</div></div><div style="display:grid;gap:6px"><span class="lbl">کاربرد</span><div style="display:flex;flex-wrap:wrap;gap:6px">'
  + ''.join(f'<label class="tag {"t-ok" if x == "اداری" else "t-neu"}" style="display:inline-flex;gap:6px;align-items:center;min-height:32px;padding:0 10px;cursor:pointer"><input type="checkbox"{" checked" if x == "اداری" else ""}>{x}</label>' for x in ['روزمره', 'اداری', 'مهمانی'])
  + '</div></div><span class="help">ویژگی ثبت‌نشده برآورده فرض نمی‌شود: مانتویی که «فصل» ندارد، در جست‌وجوی «تابستانه» پیشنهاد نمی‌شود.</span></div>')
OLD_ATTR = re.compile(r'<div style="display:grid;gap:8px"><span class="lbl">ویژگی‌ها</span>.*?افزودن ویژگی</button></div>', re.S)
def tile(color, main=False, alt=''):
    return (f'<div class="card" style="padding:10px;display:grid;gap:8px;width:180px">'
            f'<div style="position:relative;height:150px;border-radius:10px;background:#eef3f2;display:flex;align-items:center;justify-content:center;color:#7d8e8c" role="img" aria-label="جای تصویر محصول">{SVG(GARMENT, 40)}'
            + (f'<span class="tag t-ok" style="position:absolute;top:8px;inset-inline-start:8px">تصویر اصلی</span>' if main else '') + '</div>'
            f'<label style="display:grid;gap:4px"><span class="help">متن جایگزین *</span><input class="inp" value="{alt}" style="min-height:36px"></label>'
            f'<label style="display:grid;gap:4px"><span class="help">رنگ (اختیاری)</span><select class="inp" style="min-height:36px"><option>{color}</option><option>همه رنگ‌ها</option></select></label>'
            + ('' if main else '<button class="btn btn-g" style="min-height:32px;padding:0 6px;justify-self:start">تصویر اصلی شود</button>') + '</div>')
IMG_SEC = ('<section class="card" style="padding:20px;display:grid;gap:14px"><div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:12px"><h2>تصویرها</h2>'
  '<span class="help">JPG، PNG یا WebP · هر تصویر حداکثر ۲ مگابایت · تا ۸ تصویر · برای تغییر ترتیب، تصویر را بکشید</span></div>'
  '<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start">'
  + tile('سرمه‌ای', True, 'مانتو ب سرمه‌ای، نمای روبه‌رو') + tile('سرمه‌ای', False, 'مانتو ب سرمه‌ای، نمای پشت') + tile('مشکی', False, 'مانتو ب مشکی، نمای روبه‌رو')
  + f'<button class="btn btn-o" style="width:180px;min-height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;border-style:dashed">{PLUS22}افزودن تصویر</button></div>'
  '<p class="help" style="margin:0">تصویر اصلی در کارت پیشنهاد گفت‌وگو نمایش داده می‌شود. اگر تصویری به رنگی وصل باشد، کارت جایگزین تصویر همان رنگ را نشان می‌دهد. تصویر پیش‌نویس تا تأیید به مشتری نشان داده نمی‌شود.</p></section>')

def product_edit(s):
    if 'ویژگی‌های کاتالوگ</a></div>' not in s:
        s, n = OLD_ATTR.subn(ATTR_BLOCK, s, count=1); assert n == 1
    if '<h2>تصویرها</h2>' not in s:
        s = s.replace('گونه تازه تا موجودی تأییدشده نداشته باشد فعال نمی‌شود.</p></section></div>',
                      'گونه تازه تا موجودی تأییدشده نداشته باشد فعال نمی‌شود.</p></section></div>' + IMG_SEC, 1)
        assert '<h2>تصویرها</h2>' in s
    return s

# ---------------------------------------------------------------- settings: capabilities + tone
def sec(t, body, last, sid):
    return (f'<section class="card" data-sec="{t}" style="padding:20px;display:grid;gap:14px"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px"><h2>{t}</h2></div>{body}'
            f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding-top:14px;border-top:1px solid #d3dcda"><button class="btn btn-p" id="{sid}">ذخیره</button><span class="help" style="margin-inline-start:auto">{last}</span></div></section>')
def capsw(t, h):
    return (f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;min-height:44px;padding:6px 0;border-top:1px solid #d3dcda">'
            f'<label class="sw on cap-sw" role="switch" aria-checked="true" style="min-width:180px"><i></i>{t}</label><span class="help" style="flex:1;min-width:200px">{h}</span></div>')
CAPS = sec('قابلیت‌های دستیار',
  '<p class="help" style="margin:0">کمک‌های خرید را جداگانه روشن یا خاموش کنید. پاسخ به پرسش‌ها، موجودی و ارجاع همیشه فعال‌اند.</p><div>'
  + capsw('پیشنهاد محصول', 'تا سه محصول منطبق با دلیل هرکدام؛ خاموش: فهرست ساده بدون دلیل و بدون فیلتر قیمت و کاربرد.')
  + capsw('پیشنهاد جایگزین', 'برای گونه‌ای که موجود نیست، تا سه گزینه موجود و نزدیک با «تفاوت با انتخاب شما».')
  + capsw('کمک در تردید خرید', 'وقتی مشتری درباره قیمت یا انتخاب مردد است، اطلاعات یا گزینه مناسب. بدون تخفیف و وعده.') + '</div>',
  'آخرین تغییر: مریم احمدی، ۲۹ آبان', 'cap-save')
TONE = sec('لحن پاسخ',
  '<p class="help" style="margin:0">لحن فقط بر شیوه نوشتن اثر دارد، نه بر اطلاعاتی که دستیار می‌دهد.</p>'
  '<fieldset style="border:0;margin:0;padding:0;display:flex;gap:20px"><legend class="sr">لحن</legend>'
  '<label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:44px"><input type="radio" name="tone" checked> رسمی</label>'
  '<label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:44px"><input type="radio" name="tone"> صمیمی</label></fieldset>'
  '<label style="display:grid;gap:6px"><span class="lbl">توضیح لحن (اختیاری)</span><textarea class="inp" rows="2" style="min-height:64px;padding:10px 12px;font-family:inherit;line-height:24px">مشتری را «شما» خطاب کن و از ایموجی استفاده نکن.</textarea>'
  '<span class="help">حداکثر ۲۰۰ نویسه. این توضیح نمی‌تواند قاعده‌ای مثل پاسخ موجودی را تغییر دهد.</span></label>'
  '<div style="display:grid;gap:6px"><span class="help">پیش‌نمایش</span><div style="padding:10px 14px;border-radius:16px 16px 16px 6px;background:#ffffff;border:1px solid #d3dcda;font-size:14px;line-height:24px;max-width:420px">مانتو الف، مشکی، M طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ موجود است.</div></div>',
  'آخرین تغییر: مریم احمدی، ۲۹ آبان', 'tone-save')
def settings(s):
    if 'data-sec="قابلیت‌های دستیار"' in s: return s
    anchor = '<div class="toast demo" role="status">'
    i = s.index(anchor)
    return s[:i] + '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start">' + CAPS + TONE + '</div>' + s[i:]

# ---------------------------------------------------------------- report
def rcard(lab, num, help_, extra=''):
    return (f'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px"><span class="lbl">{lab}</span>'
            f'<div class="num" style="font-size:28px;line-height:36px;font-weight:700;">{num}</div><span class="help">{help_}</span>{extra}</div>')
def toplist(rows):
    return ('<ol style="margin:4px 0 0;padding-inline-start:18px;display:grid;gap:2px;font-size:13px;line-height:20px">'
            + ''.join(f'<li>{a} — <span class="num">{b}</span></li>' for a, b in rows) + '</ol>')
TOPICS = rcard('موضوع‌های پرتکرار', '۹ موضوع', 'موضوع پیام‌های مشتری در بازه',
               toplist([('موجودی', '۱۴۲'), ('ارسال', '۹۸'), ('سایز و اندازه', '۶۱'), ('مرجوعی و تعویض', '۴۴'), ('قیمت', '۳۷')]))
SHOP = ('<section style="display:grid;gap:10px" data-v2="shop"><div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:12px"><h2>خرید و درخواست‌ها</h2>'
  '<span class="help">داده تقاضای مشتری برای بهبود کاتالوگ و پاسخ‌ها</span></div>'
  '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">'
  + rcard('پیشنهادهای محصول', '۱۸۶', 'در <span class="num">۱۲۱</span> گفت‌وگو · میانگین <span class="num">۲٫۴</span> گزینه')
  + rcard('جست‌وجوی بی‌نتیجه', '۲۳', 'محدودیت‌های پرتکرار:', toplist([('جنس: چرم', '۹'), ('کاربرد: مهمانی + مانتو', '۶'), ('قد: بلند + زیر ۲ میلیون', '۴')]))
  + rcard('درخواست محصول ناموجود', '۵۴', 'گونه‌های پرتکرار:', toplist([('مانتو الف · کرم · L', '۲۱'), ('روسری ب · سرمه‌ای', '۱۲'), ('مانتو پ · زیتونی · M', '۷')]))
  + rcard('پیشنهاد جایگزین', '۴۱', 'جایگزین داده شد · بدون جایگزین: <span class="num">۱۳</span>')
  + rcard('کمک در تردید خرید', '۳۸', 'قیمت <span class="num">۱۹</span> · تردید میان گزینه‌ها <span class="num">۸</span> · سایز <span class="num">۶</span> · دیگر <span class="num">۵</span>',
          '<span class="help">نتیجه: پاسخ گرفت <span class="num">۱۴</span> · ادامه گفت‌وگو <span class="num">۹</span> · ارجاع شد <span class="num">۷</span> · نامعلوم <span class="num">۸</span></span>'
          '<span class="help" style="color:#8a4b06">نتیجه خرید در دسترس نیست؛ داده سفارش ثبت نمی‌شود.</span>')
  + rcard('نیازهای پوشش‌داده‌نشده', '۱۷', 'ویژگی‌هایی که مشتری خواست و در کاتالوگ نیست:', toplist([('جنس: چرم', '۹'), ('سایز: XL', '۵'), ('رنگ: قرمز', '۳')]))
  + '</div></section>')
def report(s):
    if 'data-v2="shop"' in s: return s
    # topics card into گفت‌وگو grid: after the first group's grid opening
    i = s.index('<h2>گفت‌وگو</h2>'); j = s.index('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">', i)
    k = s.index('</div></section>', j)
    s = s[:k] + TOPICS + s[k:]
    m = s.rindex('</section>', 0, s.index('</main>'))
    return s[:m + len('</section>')] + SHOP + s[m + len('</section>'):]

# ---------------------------------------------------------------- conversation summary + review
DT = lambda t, d: f'<div style="display:grid;gap:2px"><dt style="font-size:12px;line-height:18px;color:#4f6260">{t}</dt><dd style="margin:0;font-size:14px;line-height:22px">{d}</dd></div>'
SUM_ADD = (DT('موضوع', 'موجودی')
  + DT('کارهای دستیار', '<ul style="margin:0;padding-inline-start:18px;display:grid;gap:2px"><li>موجودی مانتو ب · سرمه‌ای · L را بررسی کرد: نامشخص (آخرین تأیید ۳ روز پیش)</li><li>جایگزین پیشنهاد نداد؛ برای نتیجه نامشخص جایگزین داده نمی‌شود</li></ul>')
  + DT('اقدام پیشنهادی', '<span class="tag t-ok">پاسخ موجودی پس از بررسی</span><span style="display:block;font-size:12px;line-height:18px;color:#4f6260;margin-top:2px">فقط پیشنهاد است و کاری انجام نمی‌دهد.</span>'))
REVIEW = ('<div class="rv" role="group" aria-label="بازبینی پاسخ دستیار" style="display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:-10px;font-size:12px;line-height:18px;color:#4f6260">بازبینی:'
  '<button class="btn btn-g" style="min-height:32px;padding:0 8px;font-size:12px">پاسخ درست بود</button>'
  '<button class="btn btn-g" style="min-height:32px;padding:0 8px;font-size:12px">پاسخ نادرست بود</button>'
  '<button class="btn btn-g" style="min-height:32px;padding:0 8px;font-size:12px">باید به پشتیبان می‌رسید</button></div>')
def conversation(name, s):
    if '<dt style="font-size:12px;line-height:18px;color:#4f6260">کارهای دستیار</dt>' not in s and 'علت ارجاع</dt>' in s:
        a = s.index('<div style="display:grid;gap:2px"><dt style="font-size:12px;line-height:18px;color:#4f6260">علت ارجاع</dt>')
        s = s[:a] + SUM_ADD + s[a:]
    if name == 'Conversation.dc.html' and 'class="rv"' not in s:
        a = s.index('<span class="meta">دستیار · ۱۰:۴۰</span></div>') + len('<span class="meta">دستیار · ۱۰:۴۰</span></div>')
        s = s[:a] + '\n' + REVIEW + s[a:]
    return s

# ---------------------------------------------------------------- status labels (DEC-337)
def labels(name, s):
    s = s.replace('نیازمند انسان', 'نیازمند رسیدگی')
    if name.startswith('Bots'):
        s = s.replace('<button class="tab" role="tab" aria-selected="false">پاسخ‌گویی دستیار</button>', '')
        s = s.replace('پاسخ‌گویی دستیار', 'منتظر مشتری')
    return s

# ---------------------------------------------------------------- apply
store_board_from('Store-Products.dc.html', 'Store-Attributes.dc.html', 'ویژگی‌های کاتالوگ', ATTR_MAIN, 'ویژگی‌های کاتالوگ')
for f in sorted(os.listdir(DIR)):
    if not f.endswith('.dc.html'): continue
    s0 = s = rd(f)
    if f.startswith(('Store-', 'Denied-Page')): s = add_nav(s)
    if f == 'Store-ProductEdit.dc.html': s = product_edit(s)
    if f == 'Store-Settings.dc.html': s = settings(s)
    if f == 'Store-Report.dc.html': s = report(s)
    if f.startswith('Conversation'): s = conversation(f, s)
    if f.startswith(('Main', 'Queue', 'Conversation', 'Bots')): s = labels(f, s)
    if s != s0: wr(f, s); print('changed', f)

# ---------------------------------------------------------------- canvas.json
def layout(cj):
    c = json.load(open(cj, encoding='utf-8')); B = c['boards']
    def shift_below(y0, d, xmax=4600):
        for k, v in B.items():
            if v['y'] > y0 and v['x'] < xmax: v['y'] += d
        for k, v in c.get('notes', {}).items():
            if isinstance(v, dict) and v.get('y', -1) > y0 and v.get('x', 0) < xmax: v['y'] += d
    if 'Store-Attributes.dc.html' not in B:
        pe = B['Store-ProductEdit.dc.html']; old = pe['h']; pe['h'] = 1420; shift_below(pe['y'], pe['h'] - old)
        st = B['Store-Settings.dc.html']; old = st['h']; st['h'] = 1900; shift_below(st['y'], st['h'] - old)
        rp = B['Store-Report.dc.html']; old = rp['h']; rp['h'] = 1760; shift_below(rp['y'], rp['h'] - old)
        cv = B['Conversation.dc.html']; cv['h'] = max(cv['h'], 1080)
        sp = B['Store-Products.dc.html']
        B['Store-Attributes.dc.html'] = {'x': 3040, 'y': sp['y'], 'w': 1440, 'h': 900, 'title': 'SCR-28 · ویژگی‌های کاتالوگ (v2)', 'expand': 'fill'}
        c['order'].append('Store-Attributes.dc.html')
        ys = max(v['y'] for k, v in B.items() if v['x'] == 4642)
        for i, (n, (_, t, _)) in enumerate(CHATS.items()):
            y = ys + 1080 * (i + 1)
            B[n + '.dc.html'] = {'x': 4642, 'y': y, 'w': 390, 'h': 844, 'title': t}
            B['D-' + n + '.dc.html'] = {'x': 5112, 'y': y, 'w': 1440, 'h': 900, 'title': 'دسکتاپ · ' + t, 'expand': 'fill'}
            c['order'] += [n + '.dc.html', 'D-' + n + '.dc.html']
    return c

if __name__ == '__main__' and len(sys.argv) > 2:
    c = layout(sys.argv[2]); json.dump(c, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('layout ok')
