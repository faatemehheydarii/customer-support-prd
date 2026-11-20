import os, re, json, glob
SRC='/home/claude/canvas/project'; OUT='/home/claude/proto'
B='back'
ADMIN_NAV=[('صف اقدام','Main'),('گفت‌وگوهای دستیار','Bots'),('توقف پاسخ خودکار','W4-Stop'),('خروج','Login-Admin')]
STORE_NAV=[('مغایرت‌ها','Store-Discrepancies'),('محصولات و گونه‌ها','Store-Products'),('دانش و سیاست','Store-Knowledge'),('تنظیمات','Store-Settings'),('مجوزها','Store-Permissions'),('گزارش','Store-Report'),('خروج','Login-Store')]
CHAT_HDR=[('گفت‌وگو با پشتیبان','Chat-Registering')]
R={
# customer
'Chat-Welcome':{'rules':CHAT_HDR+[('@send','Chat-Clarify'),('@composer','Chat-Clarify'),('موجودی محصول','Chat-Clarify'),('هزینه و زمان ارسال','Chat-Error'),('پیگیری سفارش','Chat-Typing'),('مرجوعی کالا','Chat-Typing')]},
'Chat-Clarify':{'rules':CHAT_HDR+[('S','Chat-Typing'),('M','Chat-Typing'),('L','Chat-Typing'),('مشکی','Chat-Typing'),('کرم','Chat-Typing')]},
'Chat-Typing':{'rules':CHAT_HDR,'auto':('Chat-Answer',1800)},
'Chat-Answer':{'rules':CHAT_HDR+[('بله، ممنون','Chat-Closed'),('نه، هنوز نه','Chat-Registering')]},
'Chat-Registering':{'rules':[],'auto':('Chat-Registered',1800)},
'Chat-Registered':{'rules':[('@main','Chat-Human')]},
'Chat-Human':{'rules':[]},
'Chat-Closed':{'rules':CHAT_HDR+[('@composer','Chat-Typing'),('@send','Chat-Typing')]},
'Chat-Error':{'rules':[('گفت‌وگو با پشتیبان','Chat-Registering')]},
'Chat-RegisterFailed':{'rules':CHAT_HDR+[('دوباره امتحان کنید','Chat-Registering')]},
'Chat-SendFailed':{'rules':CHAT_HDR+[('ارسال دوباره','Chat-Typing')]},
'Chat-TooLong':{'rules':CHAT_HDR},
# admin
'Login-Admin':{'rules':[('ورود','Main')]},
'Main':{'filters':1,'rules':ADMIN_NAV+[('@row1','Conversation-Queue'),('@row2','Conversation-Queue'),('@row3','Conversation-Queue'),('@row4','Conversation-Queue'),('@row5','Conversation'),('@row6','Conversation-Observer')]},
'Queue-Stopped':{'filters':1,'rules':ADMIN_NAV+[('@row1','Conversation-Queue'),('@row2','Conversation-Queue'),('@row3','Conversation-Queue'),('@row4','Conversation-Queue'),('فعال‌سازی پاسخ خودکار','Main')]},
'Queue-Empty':{'rules':ADMIN_NAV+[('رفتن به گفت‌وگوهای دستیار','Bots')]},
'Bots':{'rules':ADMIN_NAV+[('۱۰ گفت‌وگوی تصادفی برای بازبینی','Bots-Sample')],'filters':1},
'Bots-Sample':{'rules':ADMIN_NAV+[('بازگشت به فهرست','Bots'),('نمونه تازه','Bots-Sample')]},
'Conversation-Queue':{'rules':ADMIN_NAV+[('تحویل می‌گیرم','Conversation'),('بازگشت','Main')]},
'Conversation':{'rules':ADMIN_NAV+[('بستن — حل شد','W2-Resolve'),('بستن بدون تأیید','W3-CloseUnconfirmed'),('واگذاری به دستیار','W5-Handback'),('بازگشت','Main'),('درخواست تأیید از مشتری','Conversation-Closed')]},
'Conversation-Bot':{'rules':ADMIN_NAV+[('تحویل از دستیار','W1-Takeover'),('بستن بدون تأیید','W3-CloseUnconfirmed'),('بازگشت','Bots')]},
'Conversation-Observer':{'rules':ADMIN_NAV+[('بازگشت','Main')]},
'Conversation-Closed':{'rules':ADMIN_NAV+[('بازگشت','Main')]},
'W1-Takeover':{'rules':[('تحویل از دستیار','Conversation'),('انصراف',B)]},
'W2-Resolve':{'rules':[('بستن — حل شد','Conversation-Closed'),('انصراف',B)]},
'W3-CloseUnconfirmed':{'rules':[('بستن بدون تأیید','Main'),('انصراف',B)]},
'W4-Stop':{'rules':[('توقف پاسخ خودکار','Queue-Stopped'),('انصراف',B)]},
'W5-Handback':{'rules':[('واگذاری به دستیار','Main'),('انصراف',B)]},
'Denied-Role':{'rules':[('خروج','Login-Store')]},
# store
'Login-Store':{'rules':[('ورود','Store-Discrepancies')]},
'Store-Discrepancies':{'rules':STORE_NAV+[('@row1','Store-FixInventory'),('@row2','Store-FixConflict'),('@row3','Store-FixInventory'),('رفتن به تنظیمات','Store-Settings')]},
'Store-FixInventory':{'rules':STORE_NAV+[('بستن مغایرت بدون اصلاح','SW1-CloseDiscrepancy'),('تأیید','Store-Discrepancies'),('@ok','Store-Discrepancies')]},
'Store-FixConflict':{'rules':STORE_NAV+[('این رکورد درست است','Store-Discrepancies'),('بستن مغایرت بدون اصلاح','SW1-CloseDiscrepancy')]},
'Store-Products':{'rules':STORE_NAV+[('@row1','Store-ProductEdit'),('@row2','Store-ProductEdit'),('@row3','Store-ProductEdit'),('@row4','Store-ProductEdit')]},
'Store-ProductEdit':{'rules':STORE_NAV+[('اصلاح موجودی','Store-FixInventory')]},
'Store-Knowledge':{'rules':STORE_NAV+[('@row1','Store-KnowledgeEdit'),('@row2','Store-KnowledgeEdit'),('@row3','Store-KnowledgeEdit'),('@row4','Store-KnowledgeEdit')]},
'Store-KnowledgeEdit':{'rules':STORE_NAV},
'Store-Settings':{'rules':STORE_NAV+[('ذخیره','SW2-Threshold')]},
'Store-Permissions':{'rules':STORE_NAV+[('@sw','SW3-Grant')]},
'Store-Report':{'rules':STORE_NAV},
'Denied-Page':{'rules':STORE_NAV+[('رفتن به صفحه اصلی','Store-Discrepancies')]},
'SW1-CloseDiscrepancy':{'rules':[('بستن مغایرت','Store-Discrepancies'),('انصراف',B)]},
'SW2-Threshold':{'rules':[('ذخیره','Store-Settings'),('انصراف',B)]},
'SW3-Grant':{'rules':[('اعطای مجوز','Store-Permissions'),('انصراف',B)]},
'SW4-Leave':{'rules':[('ماندن',B),('ترک صفحه','Store-Discrepancies')]},
}
RT='''<style>@keyframes pf{from{opacity:0}to{opacity:1}}[data-hot]{cursor:pointer}.hl [data-hot],.hl [data-live]{outline:2px solid #f2a33a!important;outline-offset:2px;border-radius:8px;transition:outline-color .2s}</style>
<script>
(function(){var RULES=__R__,AUTO=__A__;
var MODALS=__M__;
function go(t){if(t==="back"){history.back();return}if(MODALS[t]){openModal(t);return}location.href=t+".html"}
function closeModal(){var o=document.getElementById("pmodal");if(o)o.remove()}
function openModal(t){fetch(t+".html").then(function(r){return r.text()}).then(function(h){var d=new DOMParser().parseFromString(h,"text/html");var dlg=d.querySelector("[role=dialog]");if(!dlg)return;closeModal();
var o=document.createElement("div");o.id="pmodal";o.setAttribute("style","position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(11,59,56,.38);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);animation:pf .16s ease-out");
dlg=document.importNode(dlg,true);dlg.style.maxWidth="480px";dlg.style.width="100%";o.appendChild(dlg);document.body.appendChild(o);
o.addEventListener("click",function(e){if(e.target===o)closeModal()});
var cs=[].slice.call(dlg.querySelectorAll("button"));MODALS[t].forEach(function(r){cs.forEach(function(b){var tx=b.textContent.replace(/\s+/g," ").trim();if(tx===r[0]){b.style.cursor="pointer";b.onclick=function(e){e.stopPropagation();if(r[1]==="back")closeModal();else{closeModal();location.href=r[1]+".html"}}}})});
var f=dlg.querySelector("button:not([disabled])");if(f)f.focus()})}
document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal()});
function bind(el,t){if(!el||el.dataset.hot)return;el.dataset.hot=t;el.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();go(t)})}
var cands=[].slice.call(document.querySelectorAll("button,a,label.sw,.sw,.nav,.chip,.tab,.lnk"));
RULES.forEach(function(r){var k=r[0],t=r[1];
 if(k==="@send"){bind(document.querySelector('button[aria-label="ارسال"]'),t);return}
 if(k==="@composer"){bind(document.querySelector("textarea"),t);return}
 if(k==="@main"){bind(document.querySelector("main"),t);return}
 if(k==="@ok"){bind(document.querySelector(".choice label"),t);return}
 if(k==="@sw"){bind(document.querySelectorAll(".sw")[5]||document.querySelector(".sw"),t);return}
 var m=/^@row(\\d)$/.exec(k);if(m){var tr=document.querySelectorAll("tbody tr")[+m[1]-1];if(tr){tr.querySelectorAll("a").forEach(function(a){bind(a,t)});bind(tr,t)}return}
 cands.forEach(function(el){var tx=(el.textContent||"").replace(/\\s+/g," ").trim();if(tx===k||tx.indexOf(k)===0&&tx.length<k.length+6)bind(el,t)});
});
document.querySelectorAll('a[href$=".dc.html"]').forEach(function(a){var t=a.getAttribute("href").replace(".dc.html","");bind(a,t)});
function toast(m){var t=document.getElementById("ptoast");if(!t){t=document.createElement("div");t.id="ptoast";t.setAttribute("role","status");t.setAttribute("style","position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:80;padding:10px 16px;border-radius:12px;background:#0b3b38;color:#fff;font-size:14px;line-height:22px;box-shadow:0 8px 24px rgba(11,59,56,.25);transition:opacity .2s");document.body.appendChild(t)}t.textContent=m;t.style.opacity="1";clearTimeout(t._h);t._h=setTimeout(function(){t.style.opacity="0"},1800)}
document.addEventListener("click",function(e){var t=e.target;if(t.closest("[data-hot],[data-live],#pmodal,details,input,textarea,select,label"))return;var el=t.closest("button,a,[role=tab]");if(!el)return;e.preventDefault();e.stopPropagation();toast("این بخش در نسخه نمایشی فعال نیست")},true);
if(__F__){var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));function applyF(){var tb=document.querySelector("tbody");if(!tb)return;var rows=[].slice.call(tb.querySelectorAll("tr:not(.empty)"));var tab=document.querySelector('[role=tab][aria-selected=true]');var tl=tab?tab.textContent.replace(/\\(.*\\)/,"").trim():"همه";var sels=[].slice.call(document.querySelectorAll("main select"));var inp=document.querySelector("main input[placeholder]");var q=inp?inp.value.trim():"";var shown=0;
rows.forEach(function(tr){var b=tr.querySelector(".badge");var st=b?b.textContent.trim():"";var ok=tl==="همه"||st===tl||(tl==="بسته"&&/بسته|حل‌شده/.test(st));sels.forEach(function(se){var lab=se.closest("label")?se.closest("label").textContent:"";var v=se.value;if(/مسئول/.test(lab)){if(v==="بدون مسئول")ok=ok&&!!tr.querySelector(".own0");if(v==="من")ok=ok&&tr.textContent.indexOf("سارا")>=0}if(/نوع پاسخ/.test(lab)&&v!=="همه")ok=ok&&tr.textContent.indexOf(v)>=0});if(q)ok=ok&&tr.textContent.indexOf(q)>=0;tr.style.display=ok?"":"none";if(ok)shown++});
var em=tb.querySelector("tr.empty");if(!em){em=document.createElement("tr");em.className="empty";em.innerHTML='<td colspan="9" style="text-align:center;padding:32px;color:#4f6260">گفت‌وگویی با این فیلتر نیست.</td>';tb.appendChild(em)}em.style.display=shown?"none":""}
tabs.forEach(function(b){b.dataset.live="1";b.addEventListener("click",function(){tabs.forEach(function(x){x.setAttribute("aria-selected",x===b)});applyF()})});document.querySelectorAll("main select").forEach(function(se){se.addEventListener("change",applyF)});var ii=document.querySelector("main input[placeholder]");if(ii)ii.addEventListener("input",applyF)}
try{if(parent.HL)document.documentElement.classList.add("hl")}catch(e){}
var q=new URLSearchParams(location.search).get("modal");if(q)setTimeout(function(){openModal(q)},150);
if(AUTO)setTimeout(function(){go(AUTO[0])},AUTO[1]);
try{parent.postMessage({proto:"screen",name:location.pathname.split("/").pop().replace(".html","")},"*")}catch(e){}
})();
</script>'''
def convert(name):
    s=open(f'{SRC}/{name}.dc.html',encoding='utf-8').read()
    s=s.replace('<script src="./support.js"></script>\n','').replace('<x-dc>\n','').replace('</x-dc>\n','').replace('<helmet>\n','').replace('</helmet>\n','')
    s=re.sub(r'<script type="text/x-dc" data-dc-script.*?</script>\n','',s,flags=re.S)
    s=s.replace('html,body{overflow:hidden}','')
    if name.startswith('Chat-'):  # mobile frame fits iframe: fill viewport
        s=s.replace('width:390px;height:844px;box-sizing:border-box;display:flex;flex-direction:column;','width:100%;height:100vh;box-sizing:border-box;display:flex;flex-direction:column;max-width:560px;margin:0 auto;')
    if name.startswith('Login-'):
        s=re.sub(r'<div role="(alert|status)" style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:10px;.*?</span></div>','',s,count=1,flags=re.S)
    if name.startswith('Chat-'):
        pass
    r=R[name]
    rt=RT.replace('__M__',json.dumps({k:v['rules'] for k,v in R.items() if k.startswith(('W','SW'))},ensure_ascii=False)).replace('__R__',json.dumps(r['rules'],ensure_ascii=False)).replace('__F__','true' if r.get('filters') else 'false').replace('__A__',json.dumps(list(r['auto']) if 'auto' in r else None))
    s=s.replace('</body>',rt+'\n</body>')
    open(f'{OUT}/screens/{name}.html','w',encoding='utf-8').write(s)
for n in R: convert(n)
print(len(R))
