import os, json
exec(open('/home/claude/work/gen.py',encoding='utf-8').read())
OUT='/home/claude/canvas/project'
def topbar2(active, stopped=False):
    def nav(label,key,count):
        cur=' aria-current="page"' if key==active else ''
        return f'<a class="nav" href="#"{cur}>{label}<span style="font-size:12px;color:{C["deepmuted"]}">{count}</span></a>'
    if stopped:
        st=f'<span style="display:flex;align-items:center;gap:8px;font-size:14px"><span style="width:8px;height:8px;border-radius:2px;background:#f2b46d"></span>پاسخ خودکار: متوقف</span>'
        btn=''
    else:
        st=f'<span style="display:flex;align-items:center;gap:8px;font-size:14px"><span style="width:8px;height:8px;border-radius:50%;background:{C["mint"]}"></span>پاسخ خودکار: فعال</span>'
        btn=f'<button class="btn" style="background:transparent;color:{C["deepfg"]};border-color:{C["deepmuted"]}">{I("pause",16)}توقف پاسخ خودکار</button>'
    bar=f'''<header style="display:flex;flex-wrap:wrap;align-items:center;gap:16px;padding:10px 24px;background:{C['deep']};color:{C['deepfg']}">
<div style="font-weight:700;font-size:16px;line-height:24px;margin-inline-end:16px">دستیار پشتیبانی<span style="display:block;font-weight:400;font-size:12px;line-height:18px;color:{C['deepmuted']}">پنل ادمین · فروشگاه نمایشی</span></div>
<nav aria-label="پنل ادمین" style="display:flex;gap:4px">{nav('صف اقدام','queue','۹' if stopped else '۶')}{nav('گفت‌وگوهای دستیار','bot','۱۲')}</nav>
<div style="margin-inline-start:auto;display:flex;align-items:center;gap:12px">{st}{btn}
<span style="width:1px;height:24px;background:{C['active']}"></span>
<span style="display:flex;align-items:center;gap:6px;font-size:14px">{I('user',18)}سارا</span>
<a href="#" style="color:{C['mint']};font-size:14px">خروج</a></div></header>'''
    if stopped:
        bar+=f'''<div role="status" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px 24px;background:{C['warns']};color:{C['warn']}">{I('alert',20)}
<div style="flex:1;min-width:240px"><strong style="font-weight:600">پاسخ خودکار متوقف است — از ۱۱:۰۵ توسط سارا.</strong><span style="display:block;font-size:14px;line-height:22px;color:{C['fg']}">پیام‌های تازه مشتریان مستقیم به صف می‌آیند.</span></div>
<button class="btn btn-o">فعال‌سازی پاسخ خودکار</button></div>'''
    return bar
def page(inner, active='queue', stopped=False):
    return f'''<div style="min-height:100vh;display:flex;flex-direction:column;background:{C['bg']}">
{topbar2(active,stopped)}
<main style="width:100%;max-width:1280px;margin:0 auto;box-sizing:border-box;padding:32px 24px;display:flex;flex-direction:column;gap:20px">
{inner}
</main></div>'''
def title_block(t, sub, right=''):
    return f'''<div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px">
<div><h1 style="margin:0;font-size:28px;line-height:40px;font-weight:700">{t}</h1><p style="margin:0;color:{C['mutedfg']};font-size:14px">{sub}</p></div>{right}</div>'''
REFRESH=f'<div style="display:flex;align-items:center;gap:8px;color:{C["mutedfg"]};font-size:12px">آخرین به‌روزرسانی: ۳ دقیقه پیش<button class="btn btn-o" style="min-height:36px">{I("refresh",16)}تازه‌سازی</button></div>'
def tabs(items, sel=0, label='فیلتر وضعیت'):
    return f'<div role="tablist" aria-label="{label}" style="display:flex;gap:4px;padding:4px;background:{C["card"]};border:1px solid {C["border"]};border-radius:12px">'+''.join(f'<button class="tab" role="tab" aria-selected="{"true" if i==sel else "false"}">{t}</button>' for i,t in enumerate(items))+'</div>'
def select(label, opts):
    return f'<label style="display:flex;align-items:center;gap:8px;font-size:14px">{label}<select style="min-height:40px;padding:0 12px;border:1px solid {C["input"]};border-radius:10px;font-family:inherit;font-size:14px;background:{C["card"]};color:{C["fg"]}">'+''.join(f'<option>{o}</option>' for o in opts)+'</select></label>'
def tbl(heads, body):
    return f'<div style="overflow-x:auto;background:{C["card"]};border:1px solid {C["border"]};border-radius:14px"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in heads)+f'</tr></thead><tbody>{body}</tbody></table></div>'
def tag(t, kind='warn'):
    bg,fg={'warn':(C['warns'],C['warn']),'info':(C['infos'],C['info']),'neu':(C['neus'],C['neu'])}[kind]
    return f'<span style="display:inline-block;padding:0 6px;border-radius:6px;font-size:12px;line-height:20px;background:{bg};color:{fg};margin-inline-end:4px">{t}</span>'
F={}
# --- Queue with bot stopped
rows_st=[('s3','نیازمند انسان','دستیار متوقف است','قیمت شلوار جین چنده؟','#۱۰۵۲','۴ دقیقه','بدون مسئول',True),
('s3','نیازمند انسان','دستیار متوقف است','ارسال به کرج چند روز طول می‌کشه؟','#۱۰۵۳','۲ دقیقه','بدون مسئول',True)]+rows[:4]
q_inner=title_block('صف اقدام','قدیمی‌ترین درخواست بالای صف است.',REFRESH)+f'''<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">{tabs(['همه (۹)','نیازمند انسان (۷)','در حال رسیدگی (۲)','بسته'])}{select('مسئول',['همه','بدون مسئول','من'])}
<label style="flex:1;min-width:240px;display:flex;align-items:center;gap:8px;min-height:40px;padding:0 12px;border:1px solid {C['input']};border-radius:10px;background:{C['card']};color:{C['mutedfg']}">{I('search',18)}<input aria-label="جست‌وجو در صف" placeholder="شناسه، متن پیام یا نام محصول" style="flex:1;border:0;outline:0;font-family:inherit;font-size:14px;background:transparent;color:{C['fg']}"></label></div>'''+tbl(['وضعیت','علت','آخرین پیام','زمان انتظار','مسئول','<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">خوانده‌نشده</span>'],''.join(row(r) for r in rows_st))
F['Queue-Stopped.dc.html']=(doc('صف اقدام — پاسخ خودکار متوقف',page(q_inner,'queue',True),1440,900,ADM_CSS),'SCR-10 · پاسخ خودکار متوقف (R0-b)',1440,900,True)
# --- empty queue
e_inner=title_block('صف اقدام','قدیمی‌ترین درخواست بالای صف است.',REFRESH)+f'''<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">{tabs(['همه (۰)','نیازمند انسان (۰)','در حال رسیدگی (۰)','بسته'])}{select('مسئول',['همه'])}</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:64px 24px;background:{C['card']};border:1px solid {C['border']};border-radius:14px;text-align:center">
<div style="width:48px;height:48px;border-radius:999px;background:{C['sec']};color:{C['pri']};display:flex;align-items:center;justify-content:center">{I('check',24)}</div>
<h2 style="margin:8px 0 0;font-size:18px;line-height:28px;font-weight:600">صف خالی است</h2>
<p style="margin:0;max-width:420px;color:{C['mutedfg']};font-size:14px">هیچ گفت‌وگویی منتظر پشتیبان نیست. گفت‌وگوهایی که دستیار پاسخ داده در «گفت‌وگوهای دستیار» هستند.</p>
<a href="Bots.dc.html" class="btn btn-g" style="text-decoration:none;margin-top:4px">رفتن به گفت‌وگوهای دستیار</a></div>'''
F['Queue-Empty.dc.html']=(doc('صف اقدام — خالی',page(e_inner),1440,640,ADM_CSS),'SCR-10 · صف خالی',1440,640,True)
# --- Bots SCR-12
brows=[('s2','منتظر مشتری','جواب سؤالتان را گرفتید؟','۴۲ دقیقه','۳','۰',''),
('s2','منتظر مشتری','این مانتو در سایزهای S، M، L هست. کدام را می‌خواهید؟','۲۵ دقیقه','۱','۰',''),
('s1','پاسخ‌گویی دستیار','هزینه ارسال به تهران برای سفارش‌های بالای…','۲ دقیقه','۲','۱',''),
('s1','پاسخ‌گویی دستیار','برای این سؤال اطلاعات تأییدشده‌ای ندارم.','۵ دقیقه','۴','۰',tag('نبود پاسخ')),
('s5','حل‌شده','بله، ممنون','۱ ساعت','۵','۲',''),
('s1','پاسخ‌گویی دستیار','وضعیت سفارش نمونه ۱۲۳۴: ارسال‌شده','۹ دقیقه','۲','۰',tag('پاسخ قالبی','neu'))]
def brow(r):
    cls,st,last,ago,n,rv,flags=r
    return f'<tr><td><span class="badge {cls}">{st}</span></td><td style="white-space:normal;width:100%"><a href="Conversation-Bot.dc.html" style="color:{C["fg"]};text-decoration:none;display:block;max-width:420px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{last}</a></td><td style="font-variant-numeric:tabular-nums">{ago}</td><td style="font-variant-numeric:tabular-nums">{n}</td><td style="font-variant-numeric:tabular-nums">{rv}</td><td>{flags}</td></tr>'
b_inner=title_block('گفت‌وگوهای دستیار','گفت‌وگوهایی که دستیار پاسخ داده؛ برای بازبینی نمونه‌ای.',f'<div style="display:flex;gap:8px;align-items:center">{REFRESH}<button class="btn btn-s">۱۰ گفت‌وگوی تصادفی برای بازبینی</button></div>')+f'''<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">{tabs(['همه','پاسخ‌گویی دستیار','منتظر مشتری','بسته'])}{select('نوع پاسخ',['همه','نبود پاسخ','پاسخ قالبی','موجودی نامشخص','خارج از اختیار'])}{select('بازه',['امروز','۷ روز','۳۰ روز','دلخواه'])}</div>'''+tbl(['وضعیت','آخرین پیام','از آخرین پیام','پاسخ‌های دستیار','بازبینی‌شده','پاسخ‌های حساس'],''.join(brow(r) for r in brows))
F['Bots.dc.html']=(doc('پنل ادمین — گفت‌وگوهای دستیار',page(b_inner,'bot'),1440,860,ADM_CSS),'SCR-12 · گفت‌وگوهای دستیار',1440,860,True)
# --- conversation variants
def conv_variant(status_badge, owner, reason, notice, actions, history, aside, reply=True, back='Main.dc.html'):
    replybox=f'''<div style="padding:16px;border-top:1px solid {C['border']};display:grid;gap:8px">
<label for="reply" style="font-size:14px;font-weight:500">پاسخ به مشتری</label>
<textarea id="reply" rows="3" placeholder="پاسخ را بنویسید…" style="resize:vertical;box-sizing:border-box;width:100%;padding:10px 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;line-height:24px;color:{C['fg']}"></textarea>
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;color:{C['mutedfg']}">مشتری «پشتیبان فروشگاه» را می‌بیند، نه نام شما را.</span><button class="btn btn-p">ارسال</button></div></div>''' if reply else ''
    return f'''<div style="display:flex;flex-wrap:wrap;align-items:center;gap:12px">
<a href="{back}" class="btn btn-g" style="text-decoration:none;padding:0 8px">{I('back',16)}بازگشت</a>
<span style="width:1px;height:24px;background:{C['border']}"></span>
<span style="font-variant-numeric:tabular-nums;color:{C['mutedfg']}">#۱۰۴۴</span>{status_badge}
<span style="font-size:14px">مسئول: <strong>{owner}</strong></span>
<span style="font-size:14px;color:{C['mutedfg']}">{reason}</span></div>
{notice}
<div style="display:flex;flex-wrap:wrap;gap:8px;padding:12px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">{actions}</div>
<div style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start">
<section aria-label="تاریخچه گفت‌وگو" style="flex:999 1 560px;min-width:0;display:flex;flex-direction:column;background:{C['card']};border:1px solid {C['border']};border-radius:14px;overflow:hidden">
<div style="display:flex;flex-direction:column;gap:20px;padding:24px 20px;min-height:360px;justify-content:flex-end;background:{C['bg']}">{history}</div>{replybox}</section>
{aside}</div>'''
ASIDE=f'''<aside aria-label="خلاصه درخواست" style="flex:1 1 320px;min-width:0;max-width:380px;display:flex;flex-direction:column;gap:14px;padding:20px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<h2 style="margin:0;font-size:18px;line-height:28px;font-weight:600">خلاصه درخواست</h2>
<p style="margin:0;padding:10px 12px;border-radius:10px;background:{C['muted']};font-size:14px;line-height:24px">مشتری موجودی مانتو ب، سرمه‌ای، سایز L را می‌خواهد. دستیار به‌دلیل قدیمی‌بودن داده موجودی پاسخ قطعی نداد.<span style="display:block;margin-top:4px;font-size:12px;line-height:18px;color:{C['mutedfg']}">خلاصه خودکار — برای جزئیات دقیق، تاریخچه را ببینید.</span></p>
<dl style="margin:0;display:grid;gap:12px">{kv('آخرین درخواست مشتری','«ممنون، منتظرم»')}{kv('گونه مرتبط','مانتو ب · سرمه‌ای · L')}{kv('علت ارجاع','پاسخ معتبر نبود')}{kv('اطلاعات ناقص','ندارد')}</dl></aside>'''
HIST_Q='''<div class="grp me"><div class="bub tail">مانتو ب سرمه‌ای سایز L موجوده؟</div><span class="meta">مشتری · ۱۰:۴۰</span></div>
<div class="grp them"><div class="bub">الان نمی‌توانم با اطمینان بگویم مانتو ب، سرمه‌ای، L موجود است یا نه، چون اطلاعات موجودی آن به‌روز نیست. از همکارانم در پشتیبانی می‌پرسم.<span class="src">پاسخ قالبی · موجودی: قدیمی شده</span></div><div class="bub tail">درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد.<span class="src">پاسخ قالبی</span></div><span class="meta">دستیار · ۱۰:۴۰</span></div>
'''+sysl('ارجاع ثبت شد · علت: پاسخ معتبر نبود · ۱۰:۴۰')+'''
<div class="grp me"><div class="bub tail">ممنون، منتظرم</div><span class="meta">مشتری · ۱۰:۴۱</span></div>'''
cq=conv_variant('<span class="badge s3">نیازمند انسان</span>','<span style="color:'+C['mutedfg']+';font-weight:400">بدون مسئول</span>','علت: پاسخ معتبر نبود · ۱۸ دقیقه در انتظار','',
 f'<button class="btn btn-p">{I("headset",16)}تحویل می‌گیرم</button><span style="align-self:center;font-size:14px;color:{C["mutedfg"]}">با تحویل، دستیار دیگر در این گفت‌وگو پاسخ نمی‌دهد و پاسخ‌ها با شماست.</span>',HIST_Q,ASIDE,reply=False)
F['Conversation-Queue.dc.html']=(doc('نمای مکالمه — صف',page(cq),1440,980,ADM_CSS),'SCR-11 · نمای صف (S3)',1440,980,True)
REV=f'''<div role="group" aria-label="نشانه بازبینی" style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">
<button class="btn btn-o" style="min-height:32px;padding:0 10px;font-size:12px">پاسخ درست بود</button><button class="btn btn-o" style="min-height:32px;padding:0 10px;font-size:12px">پاسخ نادرست بود</button><button class="btn btn-o" style="min-height:32px;padding:0 10px;font-size:12px">باید به پشتیبان می‌رسید</button></div>'''
REV_DONE=f'<span style="display:inline-flex;align-items:center;gap:4px;margin-top:8px;font-size:12px;line-height:18px;color:{C["succ"]}">{I("check",14)}بازبینی: پاسخ درست بود · سارا</span>'
HIST_B=f'''<div class="grp me"><div class="bub tail">هزینه ارسال به تهران چقدره؟</div><span class="meta">مشتری · ۱۱:۱۰</span></div>
<div class="grp them"><div class="bub">هزینه ارسال به تهران برای سفارش‌های بالای ۲ میلیون تومان رایگان و برای بقیه ۸۰ هزار تومان است.<span class="src">منبع: سیاست ارسال — نسخه ۳</span>{REV_DONE}</div><div class="bub tail">جواب سؤالتان را گرفتید؟<span class="src">پاسخ قالبی</span>{REV}</div><span class="meta">دستیار · ۱۱:۱۰</span></div>'''
cb=conv_variant('<span class="badge" style="background:'+C['infos']+';color:'+C['info']+'">منتظر مشتری</span>','دستیار','در انتظار: تأیید حل · ۴۲ دقیقه از آخرین پیام','',
 f'<button class="btn btn-s">تحویل از دستیار</button><button class="btn btn-o">بستن بدون تأیید</button>',HIST_B,
 f'''<aside aria-label="درباره این گفت‌وگو" style="flex:1 1 320px;min-width:0;max-width:380px;display:flex;flex-direction:column;gap:14px;padding:20px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<h2 style="margin:0;font-size:18px;line-height:28px;font-weight:600">بازبینی</h2>
<p style="margin:0;font-size:14px;line-height:24px;color:{C['mutedfg']}">برای هر پاسخ دستیار یک نشانه بگذارید. نشانه‌ها در گزارش سنجش شمرده می‌شوند.</p>
<dl style="margin:0;display:grid;gap:12px">{kv('پاسخ‌های دستیار','۲')}{kv('بازبینی‌شده','۱ از ۲')}</dl></aside>''',reply=False,back='Bots.dc.html')
F['Conversation-Bot.dc.html']=(doc('نمای مکالمه — دستیار',page(cb,'bot'),1440,860,ADM_CSS),'SCR-11 · نمای دستیار (S2) با بازبینی',1440,860,True)
# --- dialogs
def dialog(title, body, primary, primary_kind='btn-p', disabled=False, h=320):
    dis=' disabled style="opacity:1;background:'+C['muted']+';color:'+C['mutedfg']+';cursor:not-allowed"' if disabled else ''
    return doc(title, f'''<div style="width:520px;height:{h}px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;background:rgba(11,59,56,0.32);padding:24px">
<div role="dialog" aria-modal="true" aria-labelledby="t" style="width:100%;box-sizing:border-box;display:flex;flex-direction:column;gap:16px;padding:24px;background:{C['card']};border-radius:14px;box-shadow:0 12px 32px rgba(11,59,56,0.16)">
<h2 id="t" style="margin:0;font-size:18px;line-height:28px;font-weight:600">{title}</h2>
{body}
<div style="display:flex;gap:8px;justify-content:flex-start"><button class="btn {primary_kind}"{dis}>{primary}</button><button class="btn btn-o">انصراف</button></div>
</div></div>''',520,h,ADM_CSS)
def radio(name,opts,checked=None):
    return '<div role="radiogroup" style="display:grid;gap:8px">'+''.join(f'<label style="display:flex;align-items:center;gap:8px;min-height:32px;font-size:14px"><input type="radio" name="{name}"{" checked" if o==checked else ""} style="width:18px;height:18px;accent-color:{C["pri"]}">{o}</label>' for o in opts)+'</div>'
P=lambda t: f'<p style="margin:0;font-size:14px;line-height:24px">{t}</p>'
F['W1-Takeover.dc.html']=(dialog('تحویل از دستیار',P('این گفت‌وگو از دستیار گرفته می‌شود و پاسخ‌ها با شما خواهد بود. ادامه می‌دهید؟'),'تحویل از دستیار',h=260),'W1 · تحویل از دستیار',520,260,False)
F['W2-Resolve.dc.html']=(dialog('بستن — حل شد',f'''<label style="display:grid;gap:6px;font-size:14px;font-weight:500">چه کاری انجام شد؟ (کوتاه)<textarea rows="2" style="resize:none;box-sizing:border-box;padding:8px 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;line-height:24px;font-weight:400"></textarea></label>
<fieldset style="margin:0;padding:0;border:0;display:grid;gap:6px"><legend style="font-size:14px;font-weight:500;margin-bottom:6px">این گفت‌وگو بازگشایی شده بود؛ پیام تازه:</legend>{radio('reopen',['موضوع جدید','ادامه'])}</fieldset>''','بستن — حل شد',disabled=True,h=440),'W2 · بستن مستند (دکمه تا پرشدن غیرفعال)',520,440,False)
F['W3-CloseUnconfirmed.dc.html']=(dialog('بستن بدون تأیید',f'''<fieldset style="margin:0;padding:0;border:0;display:grid;gap:6px"><legend style="font-size:14px;font-weight:500;margin-bottom:6px">دلیل</legend>{radio('why',['پاسخ مشتری نیامد','مشتری منصرف شد','دیگر'],'پاسخ مشتری نیامد')}</fieldset>
<p style="margin:0;font-size:12px;line-height:20px;color:{C['mutedfg']}">این گفت‌وگو در شمار «حل‌شده» حساب نمی‌شود.</p>''','بستن بدون تأیید',h=400),'W3 · بستن بدون تأیید',520,400,False)
F['W4-Stop.dc.html']=(dialog('توقف پاسخ خودکار',P('پاسخ خودکار برای همه گفت‌وگوهای فروشگاه متوقف می‌شود و پیام‌های تازه مستقیم به صف می‌آیند. ادامه می‌دهید؟'),'توقف پاسخ خودکار','btn-p',h=260),'W4 · توقف پاسخ خودکار',520,260,False)
F['W5-Handback.dc.html']=(dialog('واگذاری به دستیار',P('گفت‌وگو به دستیار سپرده می‌شود و از صف بیرون می‌رود.'),'واگذاری به دستیار',h=240),'W5 · واگذاری به دستیار',520,240,False)
for k,(html,_,_,_,_) in F.items(): open(os.path.join(OUT,k),'w',encoding='utf-8').write(html)
json.dump({k:{'title':t,'w':w,'h':h,'page':p} for k,(_,t,w,h,p) in F.items()},open('/home/claude/work/batch2.json','w',encoding='utf-8'),ensure_ascii=False)
print(list(F))
