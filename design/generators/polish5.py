"""polish5 (CH-49): team-test fixes on admin panel. Idempotent. Run after polish4 on canvas dir and on proto/screens."""
import re, glob, os, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
EXT = '.dc.html' if DIR.endswith('project') else '.html'

CSS5 = '''/*polish5*/
.cause{display:block;margin-top:4px;font-size:13px;line-height:20px;color:#4f6260}
tr.is-new{background:#f3faf8}
tr.is-new>td:first-child{box-shadow:inset -3px 0 0 #0f766e}
.own0{color:#7d8e8c}
.own{display:inline-flex;align-items:center;gap:8px}
.av{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:#e7f4f1;color:#0b3b38;font-size:12px;font-weight:700}
.legend{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;font-size:13px;line-height:20px;color:#4f6260;margin-top:-8px}
.legend .wait{font-weight:500}
.legend details{margin-inline-start:auto;position:relative}
.legend summary{cursor:pointer;color:#0f766e;font-weight:600;list-style:none;display:inline-flex;align-items:center;gap:6px;min-height:32px}
.legend summary::-webkit-details-marker{display:none}
.legend summary::before{content:"?";display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;border:1.5px solid currentColor;font-size:12px}
.legend details[open]>div{position:absolute;inset-inline-end:0;top:calc(100% + 4px);z-index:6;width:400px;padding:14px 16px;background:#fff;border:1px solid #d3dcda;border-radius:12px;box-shadow:0 8px 24px rgba(11,59,56,.12);display:grid;gap:10px;color:#142624}
.legend dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:8px 12px;align-items:start}
.legend dd{margin:0;color:#4f6260}
.rv{font-variant-numeric:tabular-nums;white-space:nowrap}
.rv.done{color:#166534;font-weight:600}
.rv.none{color:#7d8e8c}
.sample{display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 16px;border-radius:12px;background:#e7f4f1;color:#0b3b38;font-size:14px;line-height:22px}
/*endpolish5*/'''

def add_css(s):
    s = re.sub(r'/\*polish5\*/.*?/\*endpolish5\*/\n?', '', s, flags=re.S)
    return s.replace('</style>', CSS5 + '\n</style>', 1)

Q_HELP = ('<dl><dt><span class="badge s3">نیازمند انسان</span></dt><dd>دستیار گفت‌وگو را به صف فرستاده و هنوز ادمینی آن را تحویل نگرفته است.</dd>'
          '<dt><span class="badge s4">در حال رسیدگی</span></dt><dd>یک ادمین مسئول گفت‌وگوست و پاسخ می‌دهد.</dd>'
          '<dt><span class="badge s5">بسته</span></dt><dd>رسیدگی تمام شده است.</dd></dl>'
          '<p style="margin:0;font-size:13px;line-height:20px;color:#4f6260">متن کم‌رنگ زیر وضعیت، علت آمدن گفت‌وگو به صف است. «پیام تازه» یعنی مشتری پیامی فرستاده که شما هنوز ندیده‌اید.</p>')
B_HELP = ('<dl><dt><span class="badge s1">پاسخ‌گویی دستیار</span></dt><dd>دستیار در حال گفت‌وگو با مشتری است.</dd>'
          '<dt><span class="badge s2">منتظر مشتری</span></dt><dd>دستیار پاسخ داده و منتظر پاسخ یا تأیید مشتری است.</dd>'
          '<dt><span class="badge s5">حل‌شده</span></dt><dd>مشتری حل‌شدن را تأیید کرده است.</dd></dl>'
          '<p style="margin:0;font-size:13px;line-height:20px;color:#4f6260">«بازبینی» یعنی چند پاسخ دستیار در این گفت‌وگو را یک ادمین بررسی کرده است. «نوع پاسخ» پاسخ‌هایی را نشان می‌دهد که باید زودتر دیده شوند.</p>')
TABLE = '<div style="overflow-x:auto;background:#ffffff;border:1px solid #d3dcda;border-radius:14px">'

def legend(kind):
    if kind == 'q':
        return ('<div class="legend"><span>انتظار مشتری از زمان ارجاع به صف:</span><span class="wait w1">۱۵ تا ۳۰ دقیقه</span><span class="wait w2">بیش از ۳۰ دقیقه</span>'
                '<details><summary>راهنمای وضعیت‌ها</summary><div>' + Q_HELP + '</div></details></div>')
    return '<div class="legend"><details><summary>راهنمای وضعیت‌ها و ستون‌ها</summary><div>' + B_HELP + '</div></details></div>'

def queue(s, name):
    s = s.replace('<th>وضعیت</th><th>علت</th>', '<th>وضعیت</th>').replace('<th>زمان انتظار</th>', '<th>انتظار مشتری</th>')
    s = re.sub(r'(<td><span class="badge s\d">[^<]*</span>)</td><td>([^<]*)</td>', r'\1<span class="cause">\2</span></td>', s)
    s = s.replace('<td><span style="color:#4f6260">بدون مسئول</span></td>', '<td><span class="own0" title="بدون مسئول">—<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">بدون مسئول</span></span></td>')
    for n in ('سارا', 'مریم'):
        s = s.replace(f'<td>{n}</td></tr>', f'<td><span class="own"><span class="av" aria-hidden="true">{n[0]}</span>{n}</span></td></tr>')
    s = re.sub(r'<tr>(?=(?:(?!</tr>).)*class="unread")', '<tr class="is-new">', s, flags=re.S)
    if 'class="legend"' not in s:
        s = s.replace(TABLE, legend('q') + TABLE, 1)
    if name.startswith('Queue-Stopped') and 'جست‌وجو در صف' not in s:
        main = open(os.path.join(DIR, 'Main' + EXT), encoding='utf-8').read()
        m = re.search(r'<label style="flex:1;min-width:240px.*?</label>', main, flags=re.S)
        if m:
            s = re.sub(r'(<option>من</option></select></label>)', lambda mm: mm.group(1) + '\n' + m.group(0), s, count=1)
    return s

def bots(s):
    s = s.replace('<th>پاسخ‌های دستیار</th><th>بازبینی‌شده</th><th>پاسخ‌های حساس</th>', '<th>بازبینی</th><th>نوع پاسخ</th>')
    def cell(m):
        n, r = m.group(1), m.group(2)
        cls = 'done' if n == r else ('none' if r == '۰' else '')
        return f'<td><span class="rv {cls}">{r} از {n}</span></td><td>'
    s = re.sub(r'<td style="font-variant-numeric:tabular-nums">([۰-۹]+)</td><td style="font-variant-numeric:tabular-nums">([۰-۹]+)</td><td>', cell, s)
    if 'class="legend"' not in s:
        s = s.replace(TABLE, legend('b') + TABLE, 1)
    return s

EXTRA_ROWS = [('s2', 'منتظر مشتری', 'ارسال به شیراز معمولاً ۳ تا ۵ روز کاری طول می‌کشد.', '۱ ساعت', '۰', '۲', ''),
              ('s5', 'حل‌شده', 'بله، ممنون', '۲ ساعت', '۰', '۳', ''),
              ('s2', 'منتظر مشتری', 'مرجوعی تا ۷ روز پس از تحویل ممکن است.', '۳ ساعت', '۰', '۲', ''),
              ('s5', 'حل‌شده', 'بله، ممنون', 'دیروز', '۰', '۴', '<span style="display:inline-block;padding:0 6px;border-radius:6px;font-size:12px;line-height:20px;background:#edf1f0;color:#3f4e4c;margin-inline-end:4px">پاسخ قالبی</span>')]

def sample(bots_html):
    s = bots_html.replace('<title>پنل ادمین — گفت‌وگوهای دستیار</title>', '<title>پنل ادمین — نمونه بازبینی</title>')
    s = s.replace('<p style="margin:0;color:#4f6260;font-size:14px">گفت‌وگوهایی که دستیار پاسخ داده؛ برای بازبینی نمونه‌ای.</p>',
                  '<p style="margin:0;color:#4f6260;font-size:14px">نمونه تصادفی برای بازبینی پاسخ‌های دستیار.</p>')
    bar = '<div class="sample" role="status"><b>نمونه تصادفی از «همه» · امروز</b><span>۰ از ۱۰ گفت‌وگو بازبینی شده. هر گفت‌وگو را باز کنید و برای هر پاسخ دستیار یک نشانه بگذارید.</span><span style="margin-inline-start:auto;display:flex;gap:8px"><button class="btn btn-o" style="min-height:36px">نمونه تازه</button><button class="btn btn-o" style="min-height:36px">بازگشت به فهرست</button></span></div>'
    s = s.replace(TABLE, bar + TABLE, 1)
    s = re.sub(r'<span class="rv[^"]*">([۰-۹]+) از ([۰-۹]+)</span>', r'<span class="rv none">۰ از \2</span>', s)
    rows = ''.join(f'<tr><td><span class="badge {c}">{st}</span></td><td style="white-space:normal;width:100%"><a href="Conversation-Bot{EXT}" style="color:#142624;text-decoration:none;display:block;max-width:420px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{t}</a></td><td style="font-variant-numeric:tabular-nums">{a}</td><td><span class="rv none">{r} از {n}</span></td><td>{b}</td></tr>' for c, st, t, a, r, n, b in EXTRA_ROWS)
    s = s.replace('</tbody>', rows + '</tbody>', 1)
    s = re.sub(r'<div class="legend">.*?</details></div>', '', s, flags=re.S)
    s = s.replace('<div class="sample"', '<div class="sample"', 1)
    return s

n = 0
for f in glob.glob(os.path.join(DIR, '*' + EXT)):
    name = os.path.basename(f)
    if 'Chat-' in name or name.startswith('Bots-Sample'): continue
    s = open(f, encoding='utf-8').read(); o = s
    s = add_css(s)
    if name.startswith(('Main', 'Queue-Stopped')): s = queue(s, name)
    if name.startswith('Bots'): s = bots(s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
if EXT == '.dc.html':
    b = open(os.path.join(DIR, 'Bots' + EXT), encoding='utf-8').read()
    open(os.path.join(DIR, 'Bots-Sample' + EXT), 'w', encoding='utf-8').write(sample(b))
print('polish5', n)
