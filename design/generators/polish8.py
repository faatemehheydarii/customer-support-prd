"""polish8 (CH-54): Saeed round-3 fixes. Text/markup patches on store + admin screens, toast style,
and (proto dir only) an interaction script: settings validation and day switches, per-section save
messages, permission switches, add-variant row, manual admin reply, password dialog, carry-over toasts.
Idempotent. Run after polish7 on canvas dir and on proto/screens."""
import re, glob, os, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/canvas/project'
PROTO = not DIR.endswith('project')
CSS8 = '''/*polish8*/
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:90;display:flex;align-items:center;gap:8px;max-width:min(560px,calc(100vw - 32px));padding:10px 16px;border-radius:12px;background:#0b3b38;color:#fff;font-size:14px;line-height:22px;box-shadow:0 8px 24px rgba(11,59,56,.25);transition:opacity .25s}
.toast svg{color:#99e2d6;flex:none}.toast.err{background:#b42318}.toast.err svg{color:#fff}
.err{color:#b42318}
input[aria-invalid="true"]{border-color:#b42318!important}
.seg .tab{min-height:34px;padding:0 12px}
/*endpolish8*/'''
USER_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>'
STORE_FOOT_OLD = USER_SVG + 'مریم<span class="help">مالک</span><a href="#" style="margin-inline-start:auto;color:#0f766e">خروج</a>'
STORE_FOOT_V1 = USER_SVG + 'مریم احمدی<span class="help">مدیر</span><span style="margin-inline-start:auto;display:flex;gap:12px"><a href="#" style="color:#0f766e">تغییر رمز</a><a href="#" style="color:#0f766e">خروج</a></span>'
STORE_FOOT_NEW = USER_SVG + 'مریم احمدی<span class="help">مدیر</span><span style="flex-basis:100%;display:flex;gap:16px;padding-inline-start:26px"><a href="#" style="color:#0f766e">تغییر رمز</a><a href="#" style="color:#0f766e">خروج</a></span>'
FOOT_BOX_OLD = 'margin-top:auto;display:flex;align-items:center;gap:8px;padding:12px;border-top:1px solid #d3dcda;font-size:14px">' + USER_SVG + 'مریم'
FOOT_BOX_NEW = 'margin-top:auto;display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:12px;border-top:1px solid #d3dcda;font-size:14px">' + USER_SVG + 'مریم'
ADMIN_USER_OLD = USER_SVG + 'سارا</span>\n<a href="#" style="color:#99e2d6;font-size:14px">خروج</a>'
ADMIN_USER_NEW = USER_SVG + 'سارا رحیمی</span>\n<a href="#" style="color:#99e2d6;font-size:14px">تغییر رمز</a>\n<a href="#" style="color:#99e2d6;font-size:14px">خروج</a>'
THR_BANNER = re.compile(r'<div role="status" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;padding:12px (?:32|16)px;background:#fdf1dc;[^"]*">(?:(?!</div>).)*?آستانه اعتبار موجودی تنظیم نشده(?:(?!</div>).)*?</div>\n?', re.S)

def store(name, s):
    s = s.replace(STORE_FOOT_OLD, STORE_FOOT_NEW).replace(STORE_FOOT_V1, STORE_FOOT_NEW).replace(FOOT_BOX_OLD, FOOT_BOX_NEW)
    s = s.replace('</svg>دانش و سیاست<', '</svg>دانشنامه فروشگاه<').replace('</svg>مجوزها</a>', '</svg>کاربران و مجوزها</a>')
    s = s.replace('<h1>دانش و سیاست</h1>', '<h1>دانشنامه فروشگاه</h1>').replace('</svg>دانش و سیاست</a>', '</svg>دانشنامه فروشگاه</a>')
    s = s.replace('<title>دانش و سیاست</title>', '<title>دانشنامه فروشگاه</title>')
    s = THR_BANNER.sub('', s)
    s = s.replace('آستانه اعتبار ۲۴ ساعت است', 'آستانه اعتبار ۶۰ دقیقه است').replace('۳۰ ساعت پیش', '۲ ساعت پیش')
    if name.startswith('Store-Discrepancies'):
        s = s.replace('<span class="tag t-dang">اطلاعات متعارض</span>', '<span class="tag t-warn">قدیمی شده</span>')
        s = s.replace('<span class="tag t-neu">منبع ندارد</span>', '<span class="tag t-warn">قدیمی شده</span>')
        s = s.replace('>رکورد درست را انتخاب کنید<', '>دوباره تأیید یا اصلاح کنید<').replace('>موجودی را ثبت کنید<', '>دوباره تأیید یا اصلاح کنید<')
        s = s.replace('دو رکورد فعال: موجود / ناموجود', 'ناموجود · تأیید ۳ ساعت پیش · نسخه ۲')
        s = s.replace('<span style="font-size:14px">موجودی ثبت نشده</span>', '<span style="font-size:14px">موجود · تأیید ۱ روز پیش · نسخه ۱</span>')
    if name.startswith('Store-Products'):
        s = re.sub(r'(<strong style="font-weight:600">مانتو ب</strong></td><td><span class="num">)۶(</span>)', r'\g<1>۵\2', s)
        s = s.replace('<th></th>', '<th>تغییرات</th>', 1)
    if name.startswith('Store-Knowledge') and not name.startswith('Store-KnowledgeEdit'):
        s = s.replace('<th></th>', '<th>وضعیت</th>', 1)
    if name.startswith('Store-ProductEdit') and 'گونه تازه تا موجودی' not in s:
        s = s.replace('«نامشخص» یعنی دستیار درباره این گونه جواب قطعی نمی‌دهد.', '«نامشخص» یعنی دستیار درباره این گونه جواب قطعی نمی‌دهد. گونه تازه تا موجودی تأییدشده نداشته باشد فعال نمی‌شود.')
    if name.startswith('SW3-Grant'):
        s = s.replace('نگار می‌تواند اطلاعاتی را که دستیار به مشتری می‌گوید اصلاح و تأیید کند. ادامه می‌دهید؟',
                      'سارا رحیمی اجازه ویرایش «دانشنامه فروشگاه» را می‌گیرد و می‌تواند متن‌هایی را که دستیار از آن‌ها جواب می‌دهد تغییر دهد. ادامه می‌دهید؟')
    return s

def admin(name, s):
    s = s.replace(ADMIN_USER_OLD, ADMIN_USER_NEW)
    s = s.replace('نام شما به مشتری نشان داده نمی‌شود؛ مشتری «پشتیبان فروشگاه» را می‌بیند.', 'مشتری نام و نام خانوادگی شما را با برچسب «پشتیبان فروشگاه» می‌بیند.')
    s = s.replace('>سارا گفت‌وگو را تحویل گرفت', '>سارا رحیمی گفت‌وگو را تحویل گرفت')
    return s

JS = r'''<script data-p8>
(function(){
var page=location.pathname.split("/").pop().replace(".html","");
var CK='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/></svg>';
function T(m,err){var t=document.getElementById("p8t");if(!t){t=document.createElement("div");t.id="p8t";t.setAttribute("role","status");document.body.appendChild(t)}t.className="toast"+(err?" err":"");t.innerHTML=CK+"<span>"+m+"</span>";t.style.opacity="1";clearTimeout(T.h);T.h=setTimeout(function(){t.style.opacity="0"},3400)}
function later(m){try{sessionStorage.setItem("p8t",m)}catch(e){}}
function ss(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){}}
document.querySelectorAll(".toast.demo").forEach(function(e){e.remove()});
var q=ss("p8t");if(q){try{sessionStorage.removeItem("p8t")}catch(e){}setTimeout(function(){T(q)},250)}
function tx(el){return (el.textContent||"").replace(/\s+/g," ").trim()}
function live(el,fn){if(!el)return;el.dataset.live="1";el.style.cursor="pointer";el.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();fn(e,el)})}
function fa2n(v){return +String(v).replace(/[۰-۹]/g,function(d){return "۰۱۲۳۴۵۶۷۸۹".indexOf(d)}).replace(/[^0-9]/g,"")||NaN}
function ask(title,text,ok,cb){var o=document.createElement("div");o.setAttribute("style","position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(11,59,56,.38)");
o.innerHTML='<div role="dialog" aria-modal="true" style="width:100%;max-width:480px;box-sizing:border-box;display:flex;flex-direction:column;gap:16px;padding:24px;background:#fff;border-radius:14px;box-shadow:0 12px 32px rgba(11,59,56,.16)"><h2 style="margin:0;font-size:18px;line-height:28px;font-weight:600">'+title+'</h2><p style="margin:0;font-size:14px;line-height:24px">'+text+'</p><div style="display:flex;gap:8px"><button class="btn btn-p">'+ok+'</button><button class="btn btn-o">انصراف</button></div></div>';
document.body.appendChild(o);var bs=o.querySelectorAll("button");bs.forEach(function(b){b.dataset.live="1"});bs[0].focus();
bs[0].onclick=function(e){e.stopPropagation();o.remove();cb()};bs[1].onclick=function(e){e.stopPropagation();o.remove()};o.onclick=function(e){if(e.target===o)o.remove()}}
/* messages carried to the next screen or shown when a dialog button is pressed */
var NAV={
"Store-FixInventory":{"تأیید":"تأیید شد. از پرسش بعدی مشتری، دستیار از این اطلاعات استفاده می‌کند.","بله، هنوز درست است":"دوباره تأیید شد. اعتبار داده از همین لحظه شروع شد.","بستن مورد":"مورد بدون اصلاح بسته شد."},
"Store-Settings":{"ذخیره@dlg":"آستانه اعتبار ذخیره شد."},
"Store-Employee":{"ذخیره":"اطلاعات کارمند ذخیره شد."},
"Conversation-Queue":{"تحویل می‌گیرم":"این گفت‌وگو حالا با شماست."},
"Conversation-Bot":{"تحویل از دستیار@dlg":"این گفت‌وگو حالا با شماست.","بستن بدون تأیید@dlg":"گفت‌وگو بدون تأیید بسته شد."},
"Conversation":{"بستن — حل شد@dlg":"گفت‌وگو با وضعیت «حل‌شده» بسته شد.","بستن بدون تأیید@dlg":"گفت‌وگو بدون تأیید بسته شد.","واگذاری به دستیار@dlg":"گفت‌وگو به دستیار سپرده شد.","درخواست تأیید از مشتری":"درخواست تأیید برای مشتری فرستاده شد."},
"Main":{"توقف پاسخ خودکار@dlg":"پاسخ خودکار متوقف شد؛ پیام‌های تازه مستقیم به صف می‌آیند."},
"Queue-Stopped":{"فعال‌سازی پاسخ خودکار":"پاسخ خودکار دوباره فعال شد."},
"*":{"تغییر رمز@dlg":"رمز عبور تغییر کرد."}};
document.addEventListener("click",function(e){var b=e.target.closest("button,a,label");if(!b)return;var t=tx(b),inDlg=!!b.closest("#pmodal");
[NAV[page]||{},NAV["*"]].forEach(function(M){Object.keys(M).forEach(function(k){var kk=k.replace("@dlg",""),wantDlg=k.indexOf("@dlg")>0;if(wantDlg!==inDlg)return;if(t===kk||t.indexOf(kk)===0&&!wantDlg){if(inDlg&&kk==="تغییر رمز")setTimeout(function(){T(M[k])},60);else later(M[k])}})})},true);
/* settings */
if(page==="Store-Settings"){
 var thr=document.getElementById("thr"),te=document.getElementById("thr-err");
 document.addEventListener("click",function(e){var b=e.target.closest("#thr-save");if(!b)return;var v=fa2n(thr.value);if(!(v>=15&&v<=60)){e.preventDefault();e.stopPropagation();te.style.display="";thr.setAttribute("aria-invalid","true");thr.focus();T("ذخیره نشد؛ آستانه را اصلاح کنید.",1)}else{te.style.display="none";thr.removeAttribute("aria-invalid")}},true);
 document.querySelectorAll("section[data-sec] .btn-p").forEach(function(b){if(b.id==="thr-save")return;live(b,function(){var sec=b.closest("section"),name=sec.getAttribute("data-sec");
  if(b.id==="alt-save"){var a=document.getElementById("alt"),ae=document.getElementById("alt-err");if(!a.value.trim()){ae.style.display="";a.setAttribute("aria-invalid","true");a.focus();T("ذخیره نشد؛ مسیر تماس را بنویسید.",1);return}
   ae.style.display="none";a.removeAttribute("aria-invalid");ss("p8alt",a.value.trim());altDone()}
  var last=sec.querySelector(".help[style*='margin-inline-start:auto']");if(last)last.textContent="آخرین تغییر: مریم احمدی، همین حالا";T("«"+name+"» ذخیره شد.")})});
 function altDone(){var w=document.querySelector(".alt-warn");if(w)w.remove();var a=document.getElementById("alt");if(a&&!a.value)a.value=ss("p8alt")}
 if(ss("p8alt"))altDone();
 document.querySelectorAll(".day-sw").forEach(function(sw){live(sw,function(){var on=!sw.classList.contains("on");sw.classList.toggle("on",on);sw.setAttribute("aria-checked",on);sw.lastChild.nodeValue=on?"باز":"تعطیل";var tm=sw.parentNode.querySelector(".times");if(tm)tm.style.display=on?"flex":"none"})});
 live(document.getElementById("renew"),function(){T("تمدید در نسخه نمایشی فعال نیست؛ با تیم محصول تماس بگیرید.")});
 document.querySelectorAll("main input,main select").forEach(function(i){i.dataset.live="1"});
}
if(page==="Store-Discrepancies"&&ss("p8alt")){var c=document.querySelector(".card.setup");if(c)c.remove()}
/* users & permissions */
if(page==="Store-Permissions"){document.querySelectorAll("tbody .sw").forEach(function(sw){live(sw,function(){var tr=sw.closest("tr"),td=sw.closest("td"),i=[].indexOf.call(tr.children,td),g=tx(document.querySelectorAll("thead th")[i]),n=tx(tr.querySelector("strong")),on=!sw.classList.contains("on");
 function apply(){sw.classList.toggle("on",on);sw.lastChild.nodeValue=on?"ویرایش":"فقط دیدن";var h=td.querySelector(".help");if(h)h.textContent="مریم احمدی · همین حالا";T(on?"اجازه ویرایش «"+g+"» به "+n+" داده شد.":"اجازه ویرایش «"+g+"» از "+n+" گرفته شد؛ از این به بعد فقط می‌بیند.")}
 if(on)ask("اجازه ویرایش",n+" اجازه ویرایش «"+g+"» را می‌گیرد. ادامه می‌دهید؟","اجازه می‌دهم",apply);else apply()})})}
/* employee form */
if(page==="Store-Employee"){document.querySelectorAll(".seg").forEach(function(g){var bs=g.querySelectorAll("button");bs.forEach(function(b){live(b,function(){bs.forEach(function(x){x.setAttribute("aria-selected",x===b);x.setAttribute("aria-checked",x===b)})})})});
 document.querySelectorAll("main .sw").forEach(function(sw){live(sw,function(){var on=!sw.classList.contains("on");sw.classList.toggle("on",on);sw.lastChild.nodeValue=on?"حساب فعال":"حساب غیرفعال"})});
 document.querySelectorAll("main button").forEach(function(b){if(tx(b)==="ساخت رمز تازه")live(b,function(){T("رمز موقت تازه ساخته شد.")})});
 document.querySelectorAll("main input").forEach(function(i){i.dataset.live="1"})}
/* products */
if(page==="Store-ProductEdit"){document.querySelectorAll("main button").forEach(function(b){var t=tx(b);
 if(t==="افزودن گونه")live(b,function(){var tb=b.closest("section").querySelector("tbody");if(!tb)return;var tr=document.createElement("tr");tr.innerHTML='<td><input class="inp" placeholder="سایز" style="width:80px"></td><td><input class="inp" placeholder="رنگ" style="width:110px"></td><td><span class="tag t-neu">غیرفعال</span></td><td><span class="help">موجودی ثبت نشده</span></td><td><a href="Store-FixInventory.html" style="color:#0f766e">ثبت موجودی</a></td>';tb.insertBefore(tr,tb.firstChild);tr.querySelectorAll("input,a").forEach(function(x){x.dataset.live="1"});tr.querySelector("input").focus();T("گونه تازه اضافه شد؛ تا موجودی تأییدشده نداشته باشد فعال نمی‌شود.")});
 if(t==="تأیید")live(b,function(){T("تأیید شد. از پرسش بعدی مشتری، دستیار از این اطلاعات استفاده می‌کند.")});
 if(t==="ذخیره پیش‌نویس")live(b,function(){T("پیش‌نویس ذخیره شد. تا تأییدش نکنید، دستیار از آن استفاده نمی‌کند.")})});document.querySelectorAll("main input,main textarea").forEach(function(i){i.dataset.live="1"})}
if(page==="Store-KnowledgeEdit"||page==="Store-FixInventory"){document.querySelectorAll("main button").forEach(function(b){var t=tx(b);
 if(t==="ذخیره پیش‌نویس")live(b,function(){T("پیش‌نویس ذخیره شد. تا تأییدش نکنید، دستیار از آن استفاده نمی‌کند.")});
 if(t==="تأیید"&&page==="Store-KnowledgeEdit")live(b,function(){T("تأیید شد. از پرسش بعدی مشتری، دستیار از این متن استفاده می‌کند.")})})}
if(page==="Store-Report"){document.querySelectorAll("main button").forEach(function(b){if(tx(b)==="استخراج CSV")live(b,function(){T("فایل CSV همه داده‌های این صفحه آماده شد (نمایشی).")})})}
/* admin manual reply */
if(page==="Conversation"){var ta=document.getElementById("reply"),hist=document.querySelector('section[aria-label="تاریخچه گفت‌وگو"]>div');if(ta){ta.dataset.live="1";document.querySelectorAll("button").forEach(function(b){if(tx(b)==="ارسال")live(b,function(){var v=ta.value.trim();if(!v){ta.focus();T("ابتدا پاسخ را بنویسید.",1);return}var d=document.createElement("div");d.className="grp them";var bub=document.createElement("div");bub.className="bub tail";bub.textContent=v;var m=document.createElement("span");m.className="meta";m.textContent="سارا رحیمی · پشتیبان فروشگاه · همین حالا";d.appendChild(bub);d.appendChild(m);hist.appendChild(d);hist.scrollTop=hist.scrollHeight;ta.value=""})})}}
})();
</script>'''

n = 0
for f in glob.glob(os.path.join(DIR, '*.html')):
    name = os.path.basename(f)
    if 'Chat-' in name or name == 'index.html': continue
    s = open(f, encoding='utf-8').read(); o = s
    if re.match(r'(M-)?(Store-|SW\d|Login-Store|Denied)', name): s = store(name, s)
    else: s = admin(name, s)
    s = re.sub(r'/\*polish8\*/.*?/\*endpolish8\*/\n?', '', s, flags=re.S)
    i = s.find('</style>'); s = s[:i] + CSS8 + '\n' + s[i:]
    if PROTO:
        s = re.sub(r'<script data-p8>.*?</script>\n?', '', s, flags=re.S)
        s = s.replace('</body>', JS + '\n</body>')
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('polish8', n)
