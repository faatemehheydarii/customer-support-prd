import os, json
s=open('/home/claude/work/gen3.py',encoding='utf-8').read()
exec(s.split('F={}')[0])   # helpers, CSS, shell, navlinks
OUTP='/home/claude/canvas/project'
F={}
def login(title, sub, notice=''):
    return f'''<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:{C['bg']};padding:24px;box-sizing:border-box">
<main style="width:100%;max-width:400px;display:flex;flex-direction:column;gap:24px">
<div style="text-align:center"><div style="display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:14px;background:{C['deep']};color:{C['mint']};margin-bottom:12px">{I('headset',24)}</div>
<h1 style="font-size:22px;line-height:34px">{title}</h1><p class="help" style="margin:2px 0 0;font-size:14px">{sub}</p></div>
<form class="card" style="padding:24px;display:grid;gap:16px" onsubmit="return false">
{notice}
<label style="display:grid;gap:6px"><span class="lbl">نام کاربری</span><input class="inp" autocomplete="username" dir="ltr" value="sara" style="text-align:left"></label>
<label style="display:grid;gap:6px"><span class="lbl">رمز عبور</span><input class="inp" type="password" autocomplete="current-password" value="••••••••"></label>
<button class="btn btn-p" style="justify-content:center;min-height:44px">ورود</button>
</form>
<p class="help" style="margin:0;text-align:center;font-size:13px">برای دریافت حساب یا رمز تازه با تیم محصول تماس بگیرید.</p>
</main></div>'''
ERR=f'<div role="alert" style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:10px;background:{C["dangs"]};color:{C["dang"]};font-size:14px;line-height:22px">{I("alert",18)}<span>نام کاربری یا رمز عبور درست نیست.</span></div>'
EXP=f'<div role="status" style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:10px;background:{C["infos"]};color:{C["info"]};font-size:14px;line-height:22px">{I("clock",18)}<span>نشست شما به پایان رسید. دوباره وارد شوید.</span></div>'
F['Login-Admin.dc.html']=('ورود · پنل ادمین (ورود ناموفق)',doc('ورود به پنل ادمین',login('ورود به پنل ادمین','دستیار پشتیبانی · فروشگاه نمایشی',ERR),1440,900,CSS))
F['Login-Store.dc.html']=('ورود · پنل فروشگاه (پایان نشست)',doc('ورود به پنل مدیریت فروشگاه',login('ورود به پنل مدیریت فروشگاه','دستیار پشتیبانی · فروشگاه نمایشی',EXP),1440,900,CSS))
def denied(text, action, kind):
    return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:72px 24px;text-align:center" class="card">
<div style="width:48px;height:48px;border-radius:999px;background:{C['muted']};color:{C['neu']};display:flex;align-items:center;justify-content:center">{I('key',24)}</div>
<h1 style="font-size:22px;line-height:34px;margin-top:6px">دسترسی رد شد</h1>
<p style="margin:0;max-width:420px;color:{C['mutedfg']};font-size:14px;line-height:24px">{text}</p>
<button class="btn {kind}" style="margin-top:8px">{action}</button></div>'''
d1=f'<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:{C["bg"]};padding:24px;box-sizing:border-box"><div style="width:100%;max-width:520px">'+denied('حساب شما به این پنل دسترسی ندارد.','خروج','btn-o')+'</div></div>'
F['Denied-Role.dc.html']=('دسترسی رد شد · نقش ورودی را ندارد',doc('دسترسی رد شد',d1,1440,900,CSS))
# admin with source-edit permission opening SCR-24: shell shows only 3 menu items
sh=shell('dis',denied('شما به این صفحه دسترسی ندارید.','رفتن به صفحه اصلی','btn-p'))
cut=sh.find('<a href="#"><svg'); 
import re
items=re.findall(r'<a href="#"[^>]*>.*?</a>',sh[sh.find('<nav'):sh.find('</nav>')])
keep=''.join(items[:3])
navpart=sh[sh.find('<nav'):sh.find('</nav>')]
newnav=navpart[:navpart.find('>')+1]+keep
sh=sh.replace(navpart,newnav).replace('مریم<span class="help">مالک</span>','سارا<span class="help">ادمین</span>').replace(' aria-current="page"','')
F['Denied-Page.dc.html']=('دسترسی رد شد · صفحه بی‌مجوز (ادمین در پنل فروشگاه)',doc('دسترسی رد شد',sh,1440,900,CSS))
for k,(t,h) in F.items(): open(os.path.join(OUTP,k),'w',encoding='utf-8').write(h)
json.dump({k:t for k,(t,h) in F.items()},open('/home/claude/work/batch6.json','w'),ensure_ascii=False)
print(len(items),list(F))
