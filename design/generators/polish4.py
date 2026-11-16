"""polish4: senior-review fixes (admin + store markup). Idempotent. Run after polish.py on canvas dir."""
import re, glob, os, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
EXT = '.dc.html' if DIR.endswith('project') else '.html'

def fa2int(t):
    return int(t.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')))

CLOCK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
CHECK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 4 4 10-10"/></svg>'
WARN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4"/><path d="M12 17h.01"/></svg>'
CHEV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

CSS4 = '''/*polish4*/
.wait{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:6px;font-weight:600}
.wait.w1{background:#fdf1dc;color:#8a4b06}
.wait.w2{background:#fdecea;color:#b42318}
td span[style*="font-size:12px"]{font-size:13px!important}
.unread{display:inline-flex;align-items:center;gap:6px;margin-inline-start:8px;color:#0f766e;font-weight:600;font-size:13px}
.unread::before{content:"";width:8px;height:8px;border-radius:50%;background:#0f766e}
section[aria-label="تاریخچه گفت‌وگو"]{height:calc(100vh - 300px);min-height:520px}
section[aria-label="تاریخچه گفت‌وگو"]>div:first-child{flex:1;min-height:0!important;overflow:auto;justify-content:flex-start!important}
section[aria-label="تاریخچه گفت‌وگو"]>div:first-child>:first-child{margin-top:auto}
details.more{position:relative}
details.more>summary{list-style:none}
details.more>summary::-webkit-details-marker{display:none}
details.more[open]>div{position:absolute;inset-inline-start:0;top:calc(100% + 4px);z-index:5;min-width:200px;padding:6px;background:#fff;border:1px solid #d3dcda;border-radius:12px;box-shadow:0 8px 24px rgba(11,59,56,.12)}
details.more>div .btn{width:100%;justify-content:flex-start;border:0}
.setup{display:grid;gap:12px;padding:16px 20px}
.setup ol{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:8px 24px}
.setup li{display:flex;align-items:center;gap:8px;font-size:14px;line-height:22px}
.setup li.ok{color:#166534}
.setup li.todo{color:#8a4b06;font-weight:600}
.choice{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.choice label{display:grid;gap:2px;padding:12px 14px;border:1px solid #7d8e8c;border-radius:12px;background:#fff;cursor:pointer}
.choice label.on{border:2px solid #0f766e;background:#e7f4f1;padding:11px 13px}
.choice b{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600}
.choice span{font-size:13px;line-height:20px;color:#4f6260}
/*endpolish4*/'''

def add_css(s):
    s = re.sub(r'/\*polish4\*/.*?/\*endpolish4\*/\n?', '', s, flags=re.S)
    return s.replace('</style>', CSS4 + '\n</style>', 1)

def queue(s):
    # drop the separate unread column
    s = s.replace('<th>مسئول</th><th><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">خوانده‌نشده</span></th>', '<th>مسئول</th>')
    UN = r'<td><span style="display:inline-flex;align-items:center;gap:6px;color:#0f766e;font-weight:600;font-size:12px"><span style="width:8px;height:8px;border-radius:50%;background:#0f766e"></span>پیام تازه</span></td>'
    def fix_row(m):
        tr = m.group(0)
        unread = re.search(UN, tr) is not None
        tr = re.sub(UN, '', tr)
        tr = tr.replace('<td></td></tr>', '</tr>')
        if unread and 'class="unread"' not in tr:
            tr = re.sub(r'(tabular-nums">#[۰-۹]+</span>)', r'\1<span class="unread">پیام تازه</span>', tr, count=1)
        def w(mm):
            n = fa2int(mm.group(1))
            if n >= 30: return f'<td style="font-variant-numeric:tabular-nums"><span class="wait w2">{CLOCK}{mm.group(1)} دقیقه</span></td>'
            if n >= 15: return f'<td style="font-variant-numeric:tabular-nums"><span class="wait w1">{CLOCK}{mm.group(1)} دقیقه</span></td>'
            return mm.group(0)
        tr = re.sub(r'<td style="font-variant-numeric:tabular-nums">([۰-۹]+) دقیقه</td>', w, tr)
        return tr
    return re.sub(r'<tr><td><span class="badge s[34]">.*?</tr>', fix_row, s, flags=re.S)

def more_menu(s):
    if 'class="more"' in s: return s
    b = '<button class="btn btn-o">بستن بدون تأیید</button>'
    if b not in s: return s
    menu = f'<details class="more"><summary class="btn btn-o">بیشتر{CHEV}</summary><div role="menu"><button class="btn btn-o" role="menuitem" style="color:#b42318">بستن بدون تأیید</button></div></details>'
    return s.replace(b, menu, 1)

def login(s):
    old = re.search(r'<div style="display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:14px;background:#0b3b38;color:#99e2d6;margin-bottom:12px"><svg.*?</svg></div>', s, flags=re.S)
    if old:
        s = s.replace(old.group(0), '<div aria-hidden="true" style="display:inline-block;width:48px;height:48px;border-radius:50%;background:#14b8a6;margin-bottom:12px"></div>')
    return s

def denied(s):
    return s.replace('<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px"><div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:72px 24px;text-align:center" class="card">',
                     '<main style="max-width:1120px;min-height:calc(100vh - 64px);margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;justify-content:center;gap:20px"><div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:56px 24px;text-align:center;max-width:560px;width:100%;align-self:center" class="card">')

BANNER = re.compile(r'<div role="status" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 32px;background:#fdf1dc;color:#8a4b06;border-bottom:1px solid #f3dfb8">.*?</div>\n?', re.S)

SETUP = f'''<section class="card setup" aria-label="راه‌اندازی فروشگاه"><div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px"><h2 style="margin:0;font-size:16px;line-height:24px">راه‌اندازی فروشگاه <span class="help num" style="font-weight:400">۲ از ۳ انجام شده</span></h2><a href="Store-Settings{EXT}" class="btn btn-o" style="min-height:36px;text-decoration:none">رفتن به تنظیمات</a></div><ol><li class="ok">{CHECK}آستانه اعتبار موجودی</li><li class="ok">{CHECK}ساعت‌های کاری</li><li class="todo">{WARN}مسیر تماس جایگزین — اگر ثبت درخواستی شکست بخورد، مشتری راه دیگری برای تماس ندارد.</li></ol></section>'''

def store_banners(name, s):
    if name.startswith('Store-Discrepancies'):
        s = BANNER.sub('', s, count=1)
        if 'class="card setup"' not in s:
            s = re.sub(r'(<main style="max-width:1120px;margin:0 auto;box-sizing:border-box;padding:32px;display:flex;flex-direction:column;gap:20px">)', r'\1' + SETUP.replace('\\', '\\\\'), s, count=1)
    if name.startswith('Store-Settings'):
        # alt-contact banner (3) leaves the shell; threshold banner (2) stays (AC-02-03-1)
        s = re.sub(BANNER, lambda m: m.group(0) if 'آستانه' in m.group(0) else '', s)
        if 'آستانه اعتبار موجودی تنظیم نشده است؛' not in s.split('<main')[0] and os.path.exists('/home/claude/work/thr_banner.html'):
            s = s.replace('<main', open('/home/claude/work/thr_banner.html', encoding='utf-8').read() + '<main', 1)
    return s

def report(s):
    s = re.sub(r'<span class="help num">KM-[0-9]+</span>', '', s)
    s = s.replace('grid-template-columns:repeat(4,minmax(0,1fr))', 'grid-template-columns:repeat(auto-fit,minmax(220px,1fr))')
    two = re.search(r'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;gap:8px"><span class="lbl">صحت پاسخ</span></div>.*?</div><div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;gap:8px"><span class="lbl">ادعای حساس</span></div>.*?</span></div>', s, flags=re.S)
    if two:
        merged = ('<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:8px"><span class="lbl">نیازمند برچسب</span>'
                  '<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span style="font-size:14px">صحت پاسخ</span><span class="tag t-neu">در انتظار برچسب</span></div>'
                  '<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span style="font-size:14px">ادعای حساس</span><span class="tag t-neu">در انتظار برچسب</span></div>'
                  '<span class="help">این دو شاخص با برچسب آزمون یا بازبینی محاسبه می‌شوند.</span></div>')
        s = s.replace(two.group(0), merged)
    return s

def fixinv(s):
    if 'class="choice"' in s: return s
    m = re.search(r'<section class="card" style="padding:20px;display:grid;gap:16px"><h2>اصلاح موجودی</h2>\n?<div style="display:grid;gap:6px"><span class="lbl">وضعیت</span>', s)
    if not m: return s
    choice = ('<section class="card" style="padding:20px;display:grid;gap:16px"><h2>این داده هنوز درست است؟</h2>'
              '<div class="choice" role="radiogroup" aria-label="بررسی داده">'
              '<label><input type="radio" name="ok" class="sr-only" style="position:absolute;opacity:0"><b>بله، هنوز درست است</b><span>همین داده دوباره تأیید می‌شود و اعتبارش از نو شروع می‌شود.</span></label>'
              '<label class="on"><input type="radio" name="ok" checked class="sr-only" style="position:absolute;opacity:0"><b>نه، باید اصلاح شود</b><span>وضعیت یا تعداد تازه را وارد کنید.</span></label></div>'
              '<div style="display:grid;gap:16px;padding:16px;border-radius:12px;background:#f7faf9"><div style="display:grid;gap:6px"><span class="lbl">وضعیت</span>')
    s = s.replace(m.group(0), choice, 1)
    s = s.replace('<p class="help" style="margin:0">با «تأیید»، از پرسش بعدی مشتری دستیار از این اطلاعات استفاده می‌کند.</p><div style="display:flex;flex-wrap:wrap;gap:8px;padding-top:4px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button><button class="btn btn-o">هنوز درست است — تأیید دوباره</button></div>',
                  '</div><p class="help" style="margin:0">با «تأیید»، از پرسش بعدی مشتری دستیار از این اطلاعات استفاده می‌کند.</p><div style="display:flex;flex-wrap:wrap;gap:8px"><button class="btn btn-p">تأیید</button><button class="btn btn-o">ذخیره پیش‌نویس</button></div>')
    return s

n = 0
for f in glob.glob(os.path.join(DIR, '*' + EXT)):
    name = os.path.basename(f)
    if 'Chat-' in name: continue
    s = open(f, encoding='utf-8').read(); o = s
    s = add_css(s)
    if name.startswith(('Main', 'Queue-Stopped')): s = queue(s)
    if name.startswith('Conversation.') or name == 'Conversation.html': s = more_menu(s)
    if name.startswith('Conversation-Bot'): s = re.sub(r'<details class="more">.*?</details>', '<button class="btn btn-o">بستن بدون تأیید</button>', s, flags=re.S)
    if name.startswith('Login-'): s = login(s)
    if name.startswith('Denied-Page'): s = denied(s)
    if name.startswith('Store-'): s = store_banners(name, s)
    if name.startswith('Store-Report'): s = report(s)
    if name.startswith('Store-FixInventory'): s = fixinv(s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('polish4', n)
