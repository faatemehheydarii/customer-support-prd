import os, json
exec(open('/home/claude/work/gen2.py',encoding='utf-8').read().replace("for k,(html,_,_,_,_) in F.items(): open","for k,(html,_,_,_,_) in {}.items(): open").replace("json.dump({k:","_x=({k:").replace(",open('/home/claude/work/batch2.json','w',encoding='utf-8'),ensure_ascii=False)",")"))
F={}
HIST_H=HIST_Q+'''
'''+sysl('سارا گفت‌وگو را تحویل گرفت · ۱۰:۴۸')+'''
<div class="grp them"><div class="bub tail">سلام، وقت بخیر. همین الان از انبار پرسیدم؛ مانتو ب سرمه‌ای سایز L دو عدد موجود است.</div><span class="meta who-h">پشتیبان فروشگاه · ۱۰:۴۹</span></div>
<div class="grp me"><div class="bub tail">عالیه، ممنون</div><span class="meta">مشتری · ۱۰:۵۰</span></div>'''
obs_notice=f'<div role="status" style="display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:12px;background:{C["muted"]};color:{C["fg"]};font-size:14px">{I("user",18)}این گفت‌وگو را سارا تحویل گرفته است.</div>'
co=conv_variant('<span class="badge s4">در حال رسیدگی</span>','سارا','علت: پاسخ معتبر نبود',obs_notice,'',HIST_H,ASIDE,reply=False)
co=co.replace(f'<div style="display:flex;flex-wrap:wrap;gap:8px;padding:12px;background:{C["card"]};border:1px solid {C["border"]};border-radius:14px"></div>','')
F['Conversation-Observer.dc.html']=(doc('نمای مکالمه — ناظر',page(co).replace('سارا</span>\n<a href="#" style','علی</span>\n<a href="#" style'),1440,1000,ADM_CSS),'SCR-11 · نمای ناظر (S4، مالک دیگر)',1440,1000,True)
CLOSED=f'''<div style="display:flex;flex-wrap:wrap;gap:24px;padding:16px 20px;background:{C['card']};border:1px solid {C['border']};border-radius:14px">
<dl style="margin:0;display:flex;flex-wrap:wrap;gap:24px 40px">{kv('نتیجه','حل‌شده')}{kv('مبنا','بستن مستند توسط سارا · ۱۰:۵۵')}{kv('کار انجام‌شده','موجودی از انبار پرسیده و به مشتری اعلام شد.')}{kv('برچسب بازگشایی','—')}</dl></div>'''
HIST_C=HIST_H+'\n'+sysl('بسته شد — حل شد · سارا · ۱۰:۵۵')
cc=conv_variant('<span class="badge s5">حل‌شده</span>','سارا','علت ارجاع: پاسخ معتبر نبود',CLOSED,'',HIST_C,ASIDE,reply=False)
cc=cc.replace(f'<div style="display:flex;flex-wrap:wrap;gap:8px;padding:12px;background:{C["card"]};border:1px solid {C["border"]};border-radius:14px"></div>','')
F['Conversation-Closed.dc.html']=(doc('نمای مکالمه — بسته',page(cc),1440,1060,ADM_CSS),'SCR-11 · نمای بسته (S5)',1440,1060,True)
# store dialogs
def dlg(title, body, primary, kind='btn-p', h=320, cancel='انصراف'):
    return doc(title, f'''<div style="width:520px;height:{h}px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;background:rgba(11,59,56,0.32);padding:24px">
<div role="dialog" aria-modal="true" aria-labelledby="t" style="width:100%;box-sizing:border-box;display:flex;flex-direction:column;gap:16px;padding:24px;background:{C['card']};border-radius:14px;box-shadow:0 12px 32px rgba(11,59,56,0.16)">
<h2 id="t" style="margin:0;font-size:18px;line-height:28px;font-weight:600">{title}</h2>{body}
<div style="display:flex;gap:8px"><button class="btn {kind}">{primary}</button><button class="btn btn-o">{cancel}</button></div></div></div>''',520,h,ADM_CSS)
P=lambda t: f'<p style="margin:0;font-size:14px;line-height:24px">{t}</p>'
F['SW1-CloseDiscrepancy.dc.html']=(dlg('بستن مغایرت بدون اصلاح',f'''<label style="display:grid;gap:6px;font-size:14px;font-weight:500">چرا این مورد بدون اصلاح بسته می‌شود؟<textarea rows="3" placeholder="مثلاً این گونه دیگر فروخته نمی‌شود" style="resize:none;box-sizing:border-box;padding:8px 12px;border:1px solid {C['input']};border-radius:10px;font-family:inherit;font-size:14px;line-height:24px;font-weight:400"></textarea></label><p style="margin:0;font-size:12px;line-height:20px;color:{C['mutedfg']}">مانتو ب · سرمه‌ای · L — قدیمی شده</p>''','بستن مغایرت',h=380),'W1 فروشگاه · بستن مغایرت بدون اصلاح',520,380,False)
F['SW2-Threshold.dc.html']=(dlg('تأیید تغییر آستانه',P('آستانه از <strong class="num">۲۴</strong> به <strong class="num">۴۸</strong> ساعت تغییر می‌کند. از پرسش بعدی مشتری اعمال می‌شود.'),'ذخیره',h=260),'W2 فروشگاه · تأیید آستانه',520,260,False)
F['SW3-Grant.dc.html']=(dlg('اعطای مجوز',P('نگار می‌تواند اطلاعاتی را که دستیار به مشتری می‌گوید اصلاح و تأیید کند. ادامه می‌دهید؟'),'اعطای مجوز',h=260),'W3 فروشگاه · تأیید اعطای مجوز',520,260,False)
F['SW4-Leave.dc.html']=(dlg('ترک صفحه',P('تغییرات ذخیره نشده‌اند. صفحه را ترک می‌کنید؟'),'ماندن','btn-p',h=240,cancel='ترک صفحه'),'W4 فروشگاه · ترک صفحه با تغییر ذخیره‌نشده',520,240,False)
OUTP='/home/claude/canvas/project'
for k,(html,_,_,_,_) in F.items(): open(os.path.join(OUTP,k),'w',encoding='utf-8').write(html)
json.dump({k:{'title':t,'w':w,'h':h,'page':p} for k,(_,t,w,h,p) in F.items()},open('/home/claude/work/batch4.json','w',encoding='utf-8'),ensure_ascii=False)
print(list(F))
