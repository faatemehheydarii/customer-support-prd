"""gen6 (CH-54): store panel redesign — settings (subscription, minutes threshold, day toggles, toast),
users & permissions (manager/employee, 4 groups, per-permission last change), employee form (SCR-27),
change-password dialog (store W5), report redesign (6 groups). Splices new <main> into existing polished
canvas files so earlier polish passes are kept. Idempotent: rebuilds the same main each run."""
import os, re, json, shutil
src = open('/home/claude/work/gen3.py', encoding='utf-8').read()
os.makedirs('/tmp/gen3out', exist_ok=True)
src = src.replace("OUT='/home/claude/canvas/project'", "OUT='/tmp/gen3out'").replace("/home/claude/work/batch3.json", "/tmp/gen3out/batch3.json")
exec(src)                            # all gen3 helpers (writes only to /tmp/gen3out)
P = '/home/claude/canvas/project'
MAIN = re.compile(r'<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px">.*?</main>', re.S)
MAIN_OPEN = '<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px">'

def splice(name, inner, base=None, title=None, nav=None):
    f = os.path.join(P, name)
    if not os.path.exists(f):
        shutil.copy(os.path.join(P, base), f)
    s = open(f, encoding='utf-8').read()
    s, n = MAIN.subn(lambda m: MAIN_OPEN + inner + '</main>', s, count=1)
    assert n == 1, name
    if title: s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    if nav:   # move aria-current to the right menu item
        s = s.replace(' aria-current="page"', '')
        s = re.sub(r'(<a href="#")(>(?:(?!</a>).)*?' + re.escape(nav) + ')', r'\1 aria-current="page"\2', s, count=1, flags=re.S)
    open(f, 'w', encoding='utf-8').write(s)

SWT = lambda on, a='ویرایش', b='فقط دیدن': f'<span class="sw{" on" if on else ""}"><i></i>{a if on else b}</span>'
TOAST = lambda t: f'<div class="toast demo" role="status">{I("check",18)}<span>{t}</span></div>'

# ---------------- SCR-24 settings ----------------
def sec2(t, body, last, state='', save=True, sid=''):
    foot = (f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding-top:14px;border-top:1px solid {C["border"]}">'
            f'<button class="btn btn-p"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>ذخیره</button><span class="help" style="margin-inline-start:auto">{last}</span></div>') if save else ''
    return (f'<section class="card" data-sec="{t}" style="padding:20px;display:grid;gap:14px"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">'
            f'<h2>{t}</h2>{state}</div>{body}{foot}</section>')

def dayrow2(d):
    off = d == 'جمعه'; short = d == 'پنجشنبه'
    a, b = ('۰۹:۰۰', '۱۴:۰۰') if short else ('۰۹:۰۰', '۱۸:۰۰')
    if off: a, b = '۱۰:۰۰', '۱۴:۰۰'
    times = (f'<span class="times" style="display:{"none" if off else "flex"};align-items:center;gap:6px;font-size:14px">از '
             f'<input class="inp num" value="{a}" aria-label="{d} از" style="width:84px;text-align:center"> تا '
             f'<input class="inp num" value="{b}" aria-label="{d} تا" style="width:84px;text-align:center"></span>')
    return (f'<div class="day" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;min-height:44px;padding:4px 0;border-top:1px solid {C["border"]}">'
            f'<span style="width:72px;font-size:14px;font-weight:500">{d}</span><label class="sw day-sw{"" if off else " on"}" role="switch" aria-checked="{"false" if off else "true"}"><i></i>{"تعطیل" if off else "باز"}</label>{times}</div>')

SUB = sec2('اشتراک',
    f'''<div style="display:flex;flex-wrap:wrap;align-items:center;gap:20px"><div style="display:grid;gap:2px"><span class="help">نوع اشتراک</span><strong style="font-weight:600;font-size:15px">ماهانه</strong></div>
<div style="display:grid;gap:2px"><span class="help">روزهای باقی‌مانده</span><strong class="num" style="font-weight:700;font-size:28px;line-height:36px;color:{C["pri"]}">۱۲ روز</strong></div>
<div style="display:grid;gap:2px"><span class="help">پایان اشتراک</span><strong class="num" style="font-weight:600;font-size:15px">۲ آذر ۱۴۰۵</strong></div>
<button class="btn btn-o" id="renew" style="margin-inline-start:auto;color:{C["fg"]}">تمدید اشتراک</button></div>
<p class="help" style="margin:0">فقط مدیر فروشگاه این بخش را می‌بیند. پرداخت در نسخه نمایشی فعال نیست.</p>''',
    '', save=False)
THR = sec2('آستانه اعتبار موجودی',
    field('اطلاعات موجودی تا چند دقیقه پس از آخرین تأیید معتبر است؟',
          f'<span style="display:flex;align-items:center;gap:8px"><input class="inp num" id="thr" value="۶۰" inputmode="numeric" style="width:120px"><span style="font-size:14px">دقیقه</span></span>',
          'پس از این زمان، دستیار درباره موجودی جواب قطعی نمی‌دهد تا داده دوباره تأیید شود.')
    + f'<p class="err" id="thr-err" role="alert" style="display:none;margin:0;font-size:13px;color:{C["dang"]}">آستانه باید بین ۱۵ تا ۶۰ دقیقه باشد.</p>',
    'آخرین تغییر: مریم احمدی، ۲۸ آبان', sid='thr-save')
HRS = sec2('ساعات کاری', f'<p class="help" style="margin:0">روزهای باز را روشن کنید و ساعت شروع و پایان را بنویسید. اگر هیچ روزی تنظیم نشود، به مشتری زمان پاسخی گفته نمی‌شود. ساعت‌ها به وقت فروشگاه است.</p><div>'
           + ''.join(dayrow2(d) for d in DAYS) + '</div>', 'آخرین تغییر: مریم احمدی، ۲۰ آبان')
RESP = sec2('زمان پاسخ خارج از ساعات',
    f'<div role="radiogroup" style="display:grid;gap:8px"><label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:32px"><input type="radio" name="o" checked style="width:18px;height:18px;accent-color:{C["pri"]};margin:0">از آغاز ساعت کاری بعدی</label><label style="display:flex;gap:8px;align-items:center;font-size:14px;min-height:32px"><input type="radio" name="o" style="width:18px;height:18px;accent-color:{C["pri"]};margin:0">متن کوتاه</label></div>'
    + PREV('درخواستتان ثبت شد. همکاران پشتیبانی از ساعت ۹ صبح شنبه پاسخ می‌دهند.'), 'آخرین تغییر: مریم احمدی، ۲۰ آبان')
ALT = sec2('مسیر تماس جایگزین',
    f'<div class="alt-warn">{WARN_IN("مسیر تماس جایگزین تنظیم نشده است. اگر ثبت درخواستی شکست بخورد، مشتری راه دیگری برای تماس نخواهد داشت.")}</div>'
    + field('مسیر تماس', '<input class="inp" id="alt" placeholder="مثلاً شماره ۰۲۱-۰۰۰۰۰۰۰۰ یا آیدی پیام‌رسان">', 'کوتاه بنویسید؛ عیناً به مشتری نشان داده می‌شود.')
    + f'<p class="err" id="alt-err" role="alert" style="display:none;margin:0;font-size:13px;color:{C["dang"]}">مسیر تماس را بنویسید.</p>'
    + PREV('ثبت درخواست ممکن نشد. لطفاً از راه [مسیر تماس] با ما در تماس باشید.'), '<span class="alt-last">هنوز تنظیم نشده</span>', sid='alt-save')
TZ = sec2('منطقه زمانی', field('منطقه زمانی فروشگاه', f'<select class="inp" style="max-width:320px"><option>تهران (UTC+03:30)</option></select>'), 'آخرین تغییر: تیم محصول، ۱۵ آبان')
settings_inner = (head('تنظیمات فروشگاه', 'هر بخش جداگانه ذخیره می‌شود و نتیجه ذخیره همان‌جا اعلام می‌شود.')
    + SUB
    + f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start"><div style="display:grid;gap:20px">{THR}{RESP}{TZ}</div><div style="display:grid;gap:20px">{HRS}{ALT}</div></div>'
    + TOAST('ساعات کاری ذخیره شد.'))
splice('Store-Settings.dc.html', settings_inner)

# ---------------- SCR-25 users & permissions ----------------
GRP = [('بررسی موجودی', 'تأیید و اصلاح موجودی گونه‌ها و بستن موارد بررسی'),
       ('محصولات و گونه‌ها', 'افزودن و ویرایش محصول و گونه'),
       ('دانشنامه فروشگاه', 'افزودن و ویرایش متن‌هایی که دستیار از آن‌ها جواب می‌دهد'),
       ('تنظیمات', 'آستانه اعتبار، ساعات کاری، زمان پاسخ، مسیر تماس و منطقه زمانی')]
USERS = [('مریم احمدی', 'maryam', 'مدیر', None, True),
         ('سارا رحیمی', 'sara', 'کارمند', [(True, 'مریم احمدی · ۱۸ آبان'), (True, 'مریم احمدی · ۱۸ آبان'), (False, '—'), (False, '—')], True),
         ('علی کریمی', 'ali', 'کارمند', [(True, 'مریم احمدی · ۲۵ آبان'), (False, 'مریم احمدی · ۲۵ آبان'), (True, 'مریم احمدی · ۱۵ آبان'), (False, '—')], True),
         ('نگار صادقی', 'negar', 'کارمند', [(False, '—'), (False, '—'), (False, '—'), (False, '—')], False)]
def pcell(p):
    on, last = p
    return f'<div style="display:grid;gap:2px">{SWT(on)}<span class="help num" style="font-size:11px;line-height:16px">{last}</span></div>'
def urow(u):
    n, un, role, perms, active = u
    name = f'<div style="display:grid;gap:0"><strong style="font-weight:600">{n}</strong><span class="help" dir="ltr" style="text-align:right">{un}</span></div>'
    rtag = f'<span class="tag {"t-info" if role == "مدیر" else "t-neu"}">{role}</span>'
    cells = [f'<span class="help">همه دسترسی‌ها</span>'] * 4 if perms is None else [pcell(p) for p in perms]
    st = f'<span class="tag {"t-ok" if active else "t-neu"}">{"فعال" if active else "غیرفعال"}</span>'
    edit = '' if role == 'مدیر' else f'<a href="#" class="lnk" style="color:{C["pri"]};font-size:14px">ویرایش</a>'
    return [name, rtag] + cells + [st, edit]
GDESC = (f'<div class="card" style="padding:16px 20px;display:grid;gap:10px;font-size:14px;line-height:22px"><div style="display:flex;flex-wrap:wrap;gap:6px 24px">'
         + ''.join(f'<div style="flex:1;min-width:220px"><strong style="font-weight:600">{g}:</strong> <span style="color:{C["mutedfg"]}">{d}</span></div>' for g, d in GRP)
         + f'</div><div class="help">بدون مجوز، کارمند همه بخش‌ها را فقط می‌بیند. «گزارش»، «اشتراک» و «کاربران و مجوزها» فقط برای مدیر است. حساب مدیر را تیم محصول می‌سازد.</div></div>')
perm_inner = (head('کاربران و مجوزها', 'کارمندان فروشگاه را اضافه کنید و برای هر بخش اجازه ویرایش بدهید یا بگیرید.',
                   f'<button class="btn btn-p" id="add-emp">{I("plus",18)}افزودن کارمند</button>')
              + GDESC + tbl(['نام و نام خانوادگی', 'نقش'] + [g for g, _ in GRP] + ['حساب', ''], [urow(u) for u in USERS]))
splice('Store-Permissions.dc.html', perm_inner, title='کاربران و مجوزها')

# ---------------- SCR-27 employee form ----------------
def prow(g, d, on, last):
    seg = (f'<div role="radiogroup" aria-label="{g}" class="seg" style="display:inline-flex;gap:4px;padding:4px;border:1px solid {C["border"]};border-radius:10px;background:{C["card"]}">'
           f'<button class="tab" role="radio" aria-checked="{"false" if on else "true"}" aria-selected="{"false" if on else "true"}">فقط دیدن</button>'
           f'<button class="tab" role="radio" aria-checked="{"true" if on else "false"}" aria-selected="{"true" if on else "false"}">ویرایش</button></div>')
    return (f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 0;border-top:1px solid {C["border"]}"><div style="flex:1;min-width:240px;display:grid;gap:2px">'
            f'<span class="lbl">{g}</span><span class="help">{d}</span></div>{seg}<span class="help num" style="width:200px">آخرین تغییر: {last}</span></div>')
EMP_ACC = (f'<section class="card" style="padding:20px;display:grid;gap:16px"><h2>اطلاعات حساب</h2>'
           f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{field("نام *", "<input class=inp value=سارا>")}{field("نام خانوادگی *", "<input class=inp value=رحیمی>")}</div>'
           f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{field("نام کاربری *", "<input class=inp value=sara dir=ltr style=text-align:left>", "برای ورود به پنل فروشگاه")}'
           f'{field("رمز موقت", f"<span style={chr(34)}display:flex;gap:8px{chr(34)}><input class=inp value=•••••••• type=password><button class={chr(34)}btn btn-o{chr(34)} style={chr(34)}white-space:nowrap;color:{C[chr(102)+chr(103)]}{chr(34)}>ساخت رمز تازه</button></span>", "کارمند در نخستین ورود رمز را عوض می‌کند.")}</div>'
           f'<label style="display:flex;align-items:center;gap:12px;font-size:14px"><span class="sw on" role="switch" aria-checked="true"><i></i>حساب فعال</span><span class="help">با غیرفعال‌کردن، کارمند دیگر وارد نمی‌شود ولی سابقه کارهایش می‌ماند. حذف حساب نداریم.</span></label></section>')
EMP_PERM = (f'<section class="card" style="padding:20px;display:grid;gap:4px"><h2 style="margin-bottom:6px">دسترسی‌ها</h2>'
            + prow(*GRP[0], True, 'مریم احمدی · ۱۸ آبان') + prow(*GRP[1], True, 'مریم احمدی · ۱۸ آبان')
            + prow(*GRP[2], False, '—') + prow(*GRP[3], False, '—') + '</section>')
emp_inner = (f'<div style="display:flex;flex-direction:column;gap:8px"><a href="#" class="btn btn-g" style="align-self:flex-start;padding:0 4px;text-decoration:none;min-height:32px">{I("back",16)}کاربران و مجوزها</a>'
             + head('ویرایش کارمند · سارا رحیمی', 'برای افزودن کارمند تازه همین فرم خالی باز می‌شود.') + '</div>'
             + EMP_ACC + EMP_PERM
             + f'<div style="display:flex;gap:8px"><button class="btn btn-p" id="emp-save">ذخیره</button><button class="btn btn-o" style="color:{C["fg"]}">انصراف</button></div>')
splice('Store-Employee.dc.html', emp_inner, base='Store-Permissions.dc.html', title='ویرایش کارمند', nav='مجوزها')

# ---------------- W5 change password (store + admin) ----------------
pw = os.path.join(P, 'SW5-Password.dc.html')
if not os.path.exists(pw): shutil.copy(os.path.join(P, 'SW4-Leave.dc.html'), pw)
s = open(pw, encoding='utf-8').read()
dlg = (f'<div style="width:520px;height:440px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;background:rgba(11,59,56,0.32);padding:24px">'
       f'<div role="dialog" aria-modal="true" aria-labelledby="t" style="width:100%;box-sizing:border-box;display:flex;flex-direction:column;gap:14px;padding:24px;background:#ffffff;border-radius:14px;box-shadow:0 12px 32px rgba(11,59,56,0.16)">'
       f'<h2 id="t" style="margin:0;font-size:18px;line-height:28px;font-weight:600">تغییر رمز عبور</h2>'
       f'<label style="display:grid;gap:6px"><span class="lbl">رمز فعلی</span><input class="inp" type="password" autocomplete="current-password"></label>'
       f'<label style="display:grid;gap:6px"><span class="lbl">رمز تازه</span><input class="inp" type="password" autocomplete="new-password"><span class="help">دست‌کم ۸ نویسه</span></label>'
       f'<label style="display:grid;gap:6px"><span class="lbl">تکرار رمز تازه</span><input class="inp" type="password" autocomplete="new-password"></label>'
       f'<div style="display:flex;gap:8px"><button class="btn btn-p">تغییر رمز</button><button class="btn btn-o">انصراف</button></div></div></div>')
s = re.sub(r'(</helmet>\n).*?(\n</x-dc>)', lambda m: m.group(1) + dlg + m.group(2), s, count=1, flags=re.S)
s = s.replace('"height":240', '"height":440').replace('<title>ترک صفحه</title>', '<title>تغییر رمز عبور</title>')
open(pw, 'w', encoding='utf-8').write(s)

# ---------------- SCR-26 report ----------------
def kc(name, val, defi, tag=None, warn=False, sub=None):
    t = f'<span class="tag t-neu" style="align-self:flex-start">{tag}</span>' if tag else ''
    v = f'<div class="num" style="font-size:28px;line-height:36px;font-weight:700;{"color:" + C["dang"] if warn else ""}">{val}</div>' if val else ''
    sb = f'<div class="num" style="font-size:13px;line-height:20px">{sub}</div>' if sub else ''
    return f'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px"><span class="lbl">{name}</span>{v}{sb}{t}<span class="help">{defi}</span></div>'
G2 = [('گفت‌وگو', '', [kc('گفت‌وگوهای باز شده', '۴۸۲', 'گفت‌وگوهایی که در بازه شروع شدند'),
                       kc('میانگین پیام تا بسته شدن', '۷٫۴', 'پیام‌های مشتری، دستیار و پشتیبان در هر گفت‌وگوی بسته‌شده'),
                       kc('گفت‌وگوهای بسته‌شده', '۱۲۸', 'حل‌شده یا بسته بدون تأیید'),
                       kc('پیام‌های پاسخ‌داده', '۱٬۲۴۰', 'جمع پاسخ‌های دستیار و پشتیبان', sub='دستیار ۱٬۰۳۲ · پشتیبان ۲۰۸')]),
      ('ارجاع', '', [kc('نرخ ارجاع', '۲۰٪', 'ارجاع به پشتیبان نسبت به گفت‌وگوهای باز شده', sub='۹۶ از ۴۸۲'),
                     kc('ارجاع بی‌رسیدگی بیش از ۳۰ دقیقه', '۲', 'ارجاع‌های باز که هنوز کسی تحویل نگرفته؛ هم‌اندازه هشدار صف ادمین', warn=True),
                     kc('خطای ثبت ارجاع', '۱', 'درخواست‌هایی که ثبتشان شکست خورد')]),
      ('نتیجه', '', [kc('نرخ حل', '۶۸٪', 'حل‌شده نسبت به همه گفت‌وگوهای بسته‌شده', sub='با «بله» مشتری ۵۲٪ · با ثبت پشتیبان ۱۶٪'),
                     kc('بسته بدون تأیید', '۴۱', 'پاسخ مشتری نیامد یا منصرف شد'),
                     kc('بازگشایی', '۱۲', 'گفت‌وگوهای بسته که مشتری دوباره باز کرد')]),
      ('پاسخ دستیار', '', [kc('زمان پاسخ', '۴٫۲ ثانیه', 'میانه زمان پاسخ به هر پیام مشتری', sub='صدک ۹۵: ۸٫۷ ثانیه · هدف: ۱۰ ثانیه'),
                           kc('بی‌پاسخ بیش از ۳۰ دقیقه', '۳', 'پیام‌های مشتری که نه دستیار و نه پشتیبان جواب داد', warn=True),
                           kc('نبود پاسخ', '۷۴', 'دفعه‌هایی که دستیار گفت پاسخ تأییدشده ندارد و گفت‌وگو را به پشتیبان سپرد'),
                           kc('ادعای حساس', None, 'ادعای بی‌پشتوانه درباره موجودی، سفارش یا مرجوعی؛ با برچسب بازبینی شمرده می‌شود', tag='نیازمند برچسب')]),
      ('موجودی', f'<span class="help">وضعیت همین لحظه · با باز شدن صفحه به‌روز می‌شود</span>',
                 [kc('موجود', '۱۸', 'گونه‌های فعال با موجودی معتبر'),
                  kc('ناموجود', '۴', 'گونه‌های فعال که ناموجود تأیید شده‌اند'),
                  kc('نامشخص', '۳', 'داده معتبر ندارند؛ دستیار درباره‌شان جواب قطعی نمی‌دهد. در «بررسی موجودی» دیده می‌شوند')])]

rep = ''
for g, note, cards in G2:
    rep += (f'<section style="display:grid;gap:10px"><div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:12px"><h2>{g}</h2>{note}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({180 if len(cards) > 4 else 220}px,1fr));gap:12px">' + ''.join(cards) + '</div></section>')
tools2 = f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{tabs(["امروز","۷ روز","۳۰ روز","دلخواه"],1)}<button class="btn btn-o" style="color:{C["fg"]}">{I("dl",18)}استخراج CSV</button></div>'
rep_inner = head('گزارش سنجش', '۱۷ تا ۲۴ آبان · فقط مدیر فروشگاه این صفحه را می‌بیند. همه داده‌ها در فایل CSV هم هست.', tools2) + HEALTH + rep
splice('Store-Report.dc.html', rep_inner)

# ---------------- canvas boards ----------------
cj = os.path.join(P, 'canvas.json'); d = json.load(open(cj, encoding='utf-8'))
B = d['boards']
B['Store-Settings.dc.html'].update({'h': 1500})
B['Store-Permissions.dc.html'].update({'h': 820, 'title': 'SCR-25 · کاربران و مجوزها'})
B['Store-Report.dc.html'].update({'h': 1380})
yb = max(v['y'] + v['h'] for k, v in B.items() if v.get('x', 0) in (0, 1520) and k.startswith(('Store-', 'SW')))
if 'Store-Employee.dc.html' not in B:
    B['Store-Employee.dc.html'] = {'x': 0, 'y': yb + 160, 'w': 1440, 'h': 1000, 'title': 'SCR-27 · افزودن و ویرایش کارمند', 'expand': 'fill'}
    B['SW5-Password.dc.html'] = {'x': 1520, 'y': yb + 160, 'w': 520, 'h': 440, 'title': 'W5 · تغییر رمز عبور (هر دو پنل)'}
    if 'order' in d:
        for k in ('Store-Employee.dc.html', 'SW5-Password.dc.html'):
            if k not in d['order']: d['order'].append(k)
if 'Store-FixConflict.dc.html' in B: B['Store-FixConflict.dc.html']['title'] = 'SCR-21 · اطلاعات متعارض — فقط پایلوت (DEC-314)'
json.dump(d, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
print('gen6 ok')
