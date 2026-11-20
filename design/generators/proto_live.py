"""proto_live (CH-49): builds screens/Chat-Live.html — one interactive customer chat with continuous history.
Run after polish.py on proto/screens (uses polished chat frames as the visual source)."""
import re, json
D = '/home/claude/proto/screens'
rd = lambda n: open(f'{D}/{n}.html', encoding='utf-8').read()
base = rd('Chat-Typing')
wel = rd('Chat-Welcome')
def grab(pat, src, g=1):
    m = re.search(pat, src, flags=re.S); assert m, pat; return m.group(g)
SN = {
 's3': grab(r'</header>\s*(<div role="status".*?</div>)\s*<main', rd('Chat-Registered')),
 's4': grab(r'</header>\s*(<div role="status".*?</div>)\s*<main', rd('Chat-Human')),
 'join': grab(r'(<div class="sys">.*?</div>)', rd('Chat-Human')),
 'check': grab(r'<button class="chip on" disabled aria-pressed="true">(<svg.*?</svg>)', rd('Chat-Closed')),
 'headset': grab(r'<button class="chip cta">(<svg.*?</svg>)', rd('Chat-Error')),
 'fail': grab(r'<span class="fail"[^>]*>(<svg.*?</svg>)', rd('Chat-SendFailed')),
 'retry': grab(r'<button class="chip">(<svg.*?</svg>)دوباره', rd('Chat-RegisterFailed')),
 'typing': grab(r'(<div class="grp them" role="status".*?</div></div>)', base),
 'regsys': grab(r'(<div class="sys" role="status".*?</div>)', rd('Chat-Registering')),
 'altc': grab(r'(<span style="display:block;margin:8px 0;padding:8px 12px;border-radius:12px;background:#fff;font-weight:600">.*?</span>)', rd('Chat-RegisterFailed')),
}
LONG = grab(r'<textarea rows="4"[^>]*>(.*?)</textarea>', rd('Chat-TooLong'))
main_inner = grab(r'<main[^>]*>(.*?)</main>', wel)
s = re.sub(r'<script>\s*\(function\(\)\{var RULES=.*?</script>', '', base, flags=re.S)
s = re.sub(r'(<main[^>]*>).*?(</main>)', lambda m: m.group(1) + main_inner + m.group(2), s, count=1, flags=re.S)
s = s.replace('<title>صفحه گفت‌وگو — در حال پاسخ</title>', '<title>صفحه گفت‌وگو — پروتوتایپ تعاملی</title>')
CSS = '''<style>
main{overflow-y:auto!important;justify-content:flex-start!important;scroll-behavior:smooth}
main>.grp:first-of-type{margin-top:0}
button[aria-label="ارسال"]:not([disabled]){background:#0f766e!important;color:#fff!important;cursor:pointer}
textarea{max-height:120px;overflow-y:auto}
#cnt{display:none;justify-content:space-between;align-items:center;gap:8px;padding:6px 4px 0;font-size:12px;line-height:18px}
#cnt.show{display:flex}
#cnt .n{white-space:nowrap;flex:none;padding:0 8px;border-radius:999px;background:#eef3f2;color:#4f6260;font-weight:600;font-variant-numeric:tabular-nums;margin-inline-start:auto}
#cnt.over .n{background:#fdecea;color:#b42318}
#cnt .e{color:#b42318}
.act .chip[disabled]{cursor:default}
</style>'''
s = s.replace('</head>', CSS + '\n</head>', 1)
JS = r'''<script>
(function(){
var SN=__SN__,LONG=__LONG__;
var M=document.querySelector("main"),HB=document.querySelector("header button"),TA=document.querySelector("textarea"),SB=document.querySelector('button[aria-label="ارسال"]');
var FAST=false,phase="bot",aw=null,miss=0,minute=31,humanReplied=false,started=false,local=null,clar={s:null,c:null,act:null};
var fa=function(x){return String(x).replace(/\d/g,function(d){return "۰۱۲۳۴۵۶۷۸۹"[d]})};
var en=function(x){return x.replace(/[۰-۹]/g,function(d){return "۰۱۲۳۴۵۶۷۸۹".indexOf(d)}).replace(/[٠-٩]/g,function(d){return "٠١٢٣٤٥٦٧٨٩".indexOf(d)})};
var norm=function(x){return en(x).replace(/ي/g,"ی").replace(/ك/g,"ک").replace(/‌/g," ")};
function tm(){return fa("۱۰:"+minute)}
function later(f,ms){if(FAST)f();else setTimeout(f,ms)}
function el(h){var d=document.createElement("div");d.innerHTML=h.trim();return d.firstChild}
function add(n){M.appendChild(n);M.scrollTop=M.scrollHeight;return n}
function sim(k){if(local===k){local=null;return true}try{if(parent.SIM===k){parent.SIM="normal";if(parent.simSync)parent.simSync();return true}}catch(e){}return false}
function me(t,failed){var g=el('<div class="grp me"><div class="bub tail"></div><span class="meta"></span></div>');g.firstChild.textContent=t;var m=g.lastChild;
 if(failed){m.setAttribute("role","alert");m.innerHTML='<span class="fail" style="display:inline-flex;align-items:center;gap:4px">'+SN.fail+'ارسال نشد. دوباره بفرستید.</span><button class="lnk">ارسال دوباره</button>'}else m.textContent=tm();return add(g)}
function grp(texts,who){var h='<div class="grp them">';texts.forEach(function(x,i){h+='<div class="bub'+(i===texts.length-1?" tail":"")+'">'+x+'</div>'});h+='<span class="meta">'+(who==="h"?'<span class="who-h">پشتیبان فروشگاه</span> · ':"دستیار · ")+tm()+'</span></div>';return add(el(h))}
function act(rowsArr,label){var s=document.createElement("section");s.className="act";s.setAttribute("aria-label",label||"پاسخ سریع");var q=document.createElement("div");q.className="qr";s.appendChild(q);
 rowsArr.forEach(function(r){if(r.hint){var p=document.createElement("p");p.className="qr-hint";p.textContent=r.hint;q.appendChild(p);return}var row=document.createElement("div");row.className="qr-row";row.setAttribute("role","group");row.setAttribute("aria-label",r.label||"پاسخ سریع");
  if(r.label){var l=document.createElement("span");l.className="qr-lab";l.textContent=r.label;row.appendChild(l)}
  r.chips.forEach(function(c){var b=document.createElement("button");b.className="chip"+(c.cta?" cta":"");b.innerHTML=(c.cta?SN.headset:c.icon||"")+c.t;b.dataset.v=c.v||c.t;b.addEventListener("click",function(){if(b.disabled)return;c.f(b)});row.appendChild(b)});q.appendChild(row)});
 return add(s)}
function freeze(sec,chosen){if(!sec)return;sec.dataset.done="1";[].forEach.call(sec.querySelectorAll("button"),function(b){var on=chosen&&chosen.indexOf(b)>=0;b.disabled=true;if(on){if(!b.classList.contains("on")){b.classList.add("on");b.innerHTML=SN.check+b.dataset.v}b.setAttribute("aria-pressed","true");b.style.opacity=""}else{b.classList.remove("on");b.style.opacity=".5";b.innerHTML=b.dataset.v}});var h=sec.querySelector(".qr-hint");if(h)h.remove()}
function retireActs(){[].forEach.call(M.querySelectorAll("section.act:not([data-done])"),function(s){if(s.getAttribute("aria-label")==="پیشنهاد شروع"){s.remove();return}freeze(s,[])})}
function typing(f){var t=add(el(SN.typing));later(function(){t.remove();f()},1000)}
function hb(state){HB.style.display=state==="hide"?"none":"";HB.disabled=state==="off";if(state==="off")HB.setAttribute("aria-disabled","true");else HB.removeAttribute("aria-disabled")}
function banner(k){var o=document.getElementById("stb");if(o)o.remove();if(!k)return;var b=el(SN[k]);b.id="stb";document.querySelector("header").after(b)}
var Q="جواب سؤالتان را گرفتید؟";
function answer(texts){var g=grp(texts.concat([Q]));var s=act([{chips:[{t:"بله، ممنون",f:function(b){freeze(s,[b]);me("بله، ممنون");typing(function(){grp(["خوشحالم که کمک کرد. اگر سؤال دیگری داشتید، همین‌جا بپرسید."])})}},{t:"نه، هنوز نه",f:function(b){freeze(s,[b]);me("نه، هنوز نه");typing(function(){grp(["متأسفم که پاسخ کامل نبود. می‌توانید سؤالتان را دقیق‌تر بپرسید یا با پشتیبان صحبت کنید."]);var c=act([{chips:[{t:"گفت‌وگو با پشتیبان",cta:1,f:function(b2){freeze(c,[b2]);register()}}]}])})}}]}]);return s}
/* ---- register to human ---- */
function register(){if(phase!=="bot")return;retireActs();phase="reg";hb("off");var sy=add(el(SN.regsys));
 later(function(){sy.remove();if(sim("regfail")){phase="bot";hb("on");grp(["متأسفانه الان نتوانستم درخواستتان را ثبت کنم. برای پیگیری می‌توانید از این راه با فروشگاه تماس بگیرید:"+SN.altc+"یا چند دقیقه بعد دوباره امتحان کنید."]);var s=act([{chips:[{t:"دوباره امتحان کنید",icon:SN.retry,f:function(b){freeze(s,[b]);register()}}]}]);return}
  grp(["درخواستتان ثبت شد. یکی از همکاران پشتیبانی همین‌جا پاسخ می‌دهد."]);phase="queued";hb("hide");banner("s3");
  if(!FAST)setTimeout(join,6000)},1600)}
function join(){if(phase!=="queued")return;phase="human";banner("s4");add(el(SN.join));minute++;grp(["سلام، پشتیبان فروشگاه هستم. پیام‌هایتان را دیدم؛ الان بررسی می‌کنم."],"h")}
/* ---- intents ---- */
var SIZES=["S","M","L"],COLORS=["مشکی","کرم"];
function pSize(t){var m=/(^|[^A-Za-z])(S|M|L|s|m|l)([^A-Za-z]|$)/.exec(t);if(m)return m[2].toUpperCase();if(/لارج/.test(t))return "L";if(/مدیوم/.test(t))return "M";if(/اسمال/.test(t))return "S";return null}
function pColor(t){for(var i=0;i<COLORS.length;i++)if(t.indexOf(COLORS[i])>=0)return COLORS[i];if(/سیاه/.test(t))return "مشکی";return null}
function stock(){var ok=!(clar.c==="کرم"&&clar.s==="L");var h="مانتو الف، "+clar.c+"، "+clar.s+" طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ "+(ok?"موجود است.":"موجود نیست.");
 h+=ok?'<span style="display:block;margin-top:6px;font-size:14px;line-height:22px;color:#4f6260">این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.</span>':'<span style="display:block;margin-top:6px">همین مدل در رنگ کرم در سایزهای S و M موجود است.</span>';
 aw=null;clar={s:null,c:null,act:null};answer([h])}
function clarSync(){var s=clar.act;if(!s)return;[].forEach.call(s.querySelectorAll(".chip"),function(b){var on=b.dataset.v===clar.s||b.dataset.v===clar.c;b.classList.toggle("on",on);b.setAttribute("aria-pressed",on?"true":"false");b.innerHTML=(on?SN.check:"")+b.dataset.v});
 var h=s.querySelector(".qr-hint");if(h)h.textContent=clar.s&&!clar.c?"رنگ را هم انتخاب کنید تا پیام فرستاده شود.":clar.c&&!clar.s?"سایز را هم انتخاب کنید تا پیام فرستاده شود.":"سایز و رنگ را انتخاب کنید؛ با انتخاب هر دو، پیام فرستاده می‌شود.";
 if(clar.s&&clar.c){var sec=s;later(function(){freeze(sec,[].filter.call(sec.querySelectorAll(".chip"),function(b){return b.classList.contains("on")}));clar.act=null;me(clar.c+"، "+clar.s);typing(stock)},350)}}
function clarify(){aw="clarify";grp(["این مانتو در سایزهای S، M، L و رنگ‌های مشکی و کرم هست. کدام سایز و رنگ را می‌خواهید؟"]);
 var pick=function(k){return function(b){clar[k]=clar[k]===b.dataset.v?null:b.dataset.v;clarSync()}};
 clar.act=act([{label:"سایز",chips:SIZES.map(function(x){return{t:x,f:pick("s")}})},{label:"رنگ",chips:COLORS.map(function(x){return{t:x,f:pick("c")}})},{hint:"x"}]);clarSync()}
var ASKO="شماره سفارشتان را بفرستید. این شماره در پیامک یا ایمیل تأیید سفارش آمده است.";
var SHIP='هزینه ارسال به تهران برای سفارش‌های بالای ۲ میلیون تومان رایگان و برای بقیه ۸۰ هزار تومان است؛ شهرهای دیگر ۱۲۰ هزار تومان.<span style="display:block;margin-top:6px">زمان تقریبی رسیدن: تهران ۱ تا ۲ روز کاری، شهرهای دیگر ۳ تا ۵ روز کاری.</span>';
function orderNo(t){var m=/\d{3,6}/.exec(t);return m?m[0]:null}
function notFound(){miss++;if(miss>=2){aw=null;miss=0;grp(["باز هم این شماره سفارش را پیدا نکردم. درخواستتان را برای همکاران پشتیبانی ثبت می‌کنم."]);register();return}
 grp(["این شماره سفارش را پیدا نکردم. لطفاً شماره را دوباره بفرستید؛ این شماره در پیامک یا ایمیل تأیید سفارش آمده است."])}
function returnItems(no){aw="returnItem";if(no==="1234"){aw=null;answer(["سفارش ۱۲۳۴ هنوز تحویل نشده است. مرجوعی تا ۷ روز پس از تحویل ممکن است؛ بعد از رسیدن سفارش دوباره بپرسید."]);return}
 grp(["در سفارش ۵۵۱ دو کالا هست. کدام را می‌خواهید مرجوع کنید؟"]);var s=act([{chips:["مانتو ب سرمه‌ای L","شلوار جین آبی ۳۲"].map(function(x){return{t:x,f:function(b){freeze(s,[b]);me(x);aw=null;typing(function(){retPolicy()})}}})}])}
function retPolicy(){var g=grp(['مرجوعی تا ۷ روز پس از تحویل ممکن است، به شرط استفاده‌نشده بودن و داشتن برچسب. سفارش ۵۵۱ دو روز پیش تحویل شده و هنوز در مهلت است.<span style="display:block;margin-top:6px">ثبت مرجوعی را همکاران پشتیبانی انجام می‌دهند؛ برای ثبت، «گفت‌وگو با پشتیبان» را بزنید.</span>',Q]);
 var s=act([{chips:[{t:"بله، ممنون",f:function(b){freeze(s,[b]);me("بله، ممنون");typing(function(){grp(["خوشحالم که کمک کرد. اگر سؤال دیگری داشتید، همین‌جا بپرسید."])})}},{t:"نه، هنوز نه",f:function(b){freeze(s,[b]);me("نه، هنوز نه");typing(function(){grp(["متأسفم که پاسخ کامل نبود. می‌توانید سؤالتان را دقیق‌تر بپرسید یا با پشتیبان صحبت کنید."]);var c=act([{chips:[{t:"گفت‌وگو با پشتیبان",cta:1,f:function(b2){freeze(c,[b2]);register()}}]}])})}}]},{chips:[{t:"گفت‌وگو با پشتیبان",cta:1,f:function(b){freeze(s,[b]);register()}}]}])}
function route(raw){var t=norm(raw);
 if(aw==="order"||aw==="returnOrder"){var n=orderNo(t);if(n==="1234"||n==="551"){var w=aw;aw=null;miss=0;if(w==="order")answer([n==="1234"?"سفارش ۱۲۳۴ طبق اطلاعات فروشگاه ۲۶ آبان ارسال شده است. زمان تقریبی رسیدن ۱ تا ۳ روز کاری است.":"سفارش ۵۵۱ طبق اطلاعات فروشگاه ۲۴ آبان تحویل شده است."]);else returnItems(n);return}
  if(n){notFound();return}aw=null}
 if(aw==="clarify"){var s0=pSize(t),c0=pColor(t);if(s0||c0){if(s0)clar.s=s0;if(c0)clar.c=c0;if(clar.s&&clar.c){if(clar.act)freeze(clar.act,[]);clar.act=null;stock()}else{grp(["کدام "+(clar.s?"رنگ":"سایز")+" را می‌خواهید؟"]);clarSync()}return}aw=null;clar.act=null}
 if(/پشتیبان|اپراتور|انسان|آدم واقعی/.test(t)){register();return}
 if(/مرجوع|برگشت|پس بد|عودت/.test(t)){aw="returnOrder";miss=0;grp([ASKO]);return}
 if(/پیگیری|کجاست|نرسیده|سفارشم/.test(t)){aw="order";miss=0;grp([ASKO]);return}
 if(/ارسال|پست|هزینه|کرایه|تحویل/.test(t)){answer([SHIP]);return}
 if(/تخفیف|قیمت ویژه/.test(t)){grp(["تصمیم درباره تخفیف با همکاران پشتیبانی است. درخواستتان را برایشان ثبت می‌کنم."]);register();return}
 if(/مانتو ب|شلوار/.test(t)){grp(["الان نمی‌توانم با اطمینان بگویم این کالا موجود است یا نه، چون اطلاعات موجودی آن به‌روز نیست. از همکارانم در پشتیبانی می‌پرسم."]);register();return}
 if(/موجود|مانتو|سایز|رنگ|دارید/.test(t)){clar.s=pSize(t);clar.c=pColor(t);if(clar.s&&clar.c)stock();else clarify();return}
 if(/^(سلام|درود)[\s!.؟]*$/.test(t)){grp(["سلام! بفرمایید، درباره موجودی، ارسال، سفارش یا مرجوعی بپرسید."]);return}
 if(/ممنون|مرسی|متشکر/.test(t)){grp(["خواهش می‌کنم. اگر سؤال دیگری داشتید، همین‌جا بپرسید."]);return}
 grp(["برای این سؤال اطلاعات تأییدشده‌ای ندارم. درخواستتان را برای همکاران پشتیبانی ثبت می‌کنم."]);register()}
function process(t){if(phase==="queued"||phase==="reg")return;if(phase==="human"){if(!humanReplied){humanReplied=true;later(function(){minute++;grp(["ممنون، پیامتان را دیدم. چند لحظه صبر کنید."],"h")},1500)}return}
 if(sim("error")){typing(function(){grp(["الان نمی‌توانم به پیامتان جواب بدهم. می‌توانید کمی بعد دوباره بپرسید یا همین حالا با پشتیبان صحبت کنید."]);var c=act([{chips:[{t:"گفت‌وگو با پشتیبان",cta:1,f:function(b){freeze(c,[b]);register()}}]}])});return}
 typing(function(){route(t)})}
function send(t){t=(t||"").trim();if(!t||t.length>1000)return;minute++;retireActs();
 if(sim("sendfail")){var g=me(t,true);g.querySelector(".lnk").addEventListener("click",function(){var m=g.querySelector(".meta");m.removeAttribute("role");m.textContent=tm();process(t)});return}
 me(t);process(t)}
/* ---- composer ---- */
var row=SB.parentNode,cnt=document.createElement("div");cnt.id="cnt";cnt.innerHTML='<span class="e" role="alert"></span><span class="n"></span>';row.parentNode.appendChild(cnt);
function sync(){TA.style.height="auto";TA.style.height=Math.min(TA.scrollHeight,120)+"px";var n=TA.value.length,over=n>1000;
 cnt.classList.toggle("show",n>=900);cnt.classList.toggle("over",over);cnt.querySelector(".n").textContent=fa(n)+" از ۱۰۰۰";cnt.querySelector(".e").textContent=over?"پیامتان طولانی است. لطفاً کوتاه‌ترش کنید یا در چند پیام بفرستید.":"";
 TA.style.borderColor=over?"#b42318":"";if(over)TA.setAttribute("aria-invalid","true");else TA.removeAttribute("aria-invalid");SB.disabled=!TA.value.trim()||over}
TA.addEventListener("input",sync);
TA.addEventListener("keydown",function(e){if(e.key==="Enter"&&!e.shiftKey&&!e.isComposing&&window.innerWidth>=600){e.preventDefault();if(!SB.disabled)SB.click()}});
SB.addEventListener("click",function(){var v=TA.value;if(!v.trim()||v.length>1000)return;TA.value="";sync();send(v);TA.focus()});
HB.addEventListener("click",function(){if(!HB.disabled)register()});
[].forEach.call(M.querySelectorAll('section.act button'),function(b){b.dataset.v=b.textContent.trim();b.addEventListener("click",function(){send(b.dataset.v)})});
sync();
/* ---- presets (from the prototype menu) ---- */
var QS="";try{QS=(parent.P&&parent.P.q!=null)?parent.P.q:location.search}catch(e){QS=location.search}
var p=new URLSearchParams(QS).get("s")||"welcome";
function starter(t){var b=[].filter.call(M.querySelectorAll("section.act button"),function(x){return x.dataset.v===t})[0];if(b)b.click()}
function chipClick(t){var bs=[].filter.call(M.querySelectorAll("section.act:not([data-done]) button"),function(x){return x.dataset.v===t});if(bs.length)bs[bs.length-1].click()}
var ASK="مانتو الف مشکی، سایز M موجوده؟";
FAST=true;
({clarify:function(){send("سلام، مانتو الف رو دارید؟")},partial:function(){send("سلام، مانتو الف رو دارید؟");chipClick("M")},
 answer:function(){send(ASK)},closed:function(){send(ASK);chipClick("بله، ممنون")},notyet:function(){send(ASK);chipClick("نه، هنوز نه")},
 shipping:function(){starter("هزینه و زمان ارسال")},order:function(){starter("پیگیری سفارش");send("۱۲۳۴")},
 ret:function(){starter("مرجوعی کالا");send("۵۵۱");chipClick("مانتو ب سرمه‌ای L")},
 registered:function(){send("مانتو ب سرمه‌ای سایز L موجوده؟");FAST=false;setTimeout(join,6000)},human:function(){send("مانتو ب سرمه‌ای سایز L موجوده؟");join();send("ممنون، منتظرم")},
 error:function(){local="error";send("هزینه ارسال به شیراز چقدره؟")},regfail:function(){local="regfail";register()},
 sendfail:function(){local="sendfail";send(ASK)},toolong:function(){TA.value=(LONG+" "+LONG).slice(0,1042);sync()}}[p]||function(){})();
FAST=false;M.scrollTop=M.scrollHeight;
try{parent.postMessage({proto:"screen",name:"Chat-Live"},"*")}catch(e){}
})();
</script>'''
JS = JS.replace('__SN__', json.dumps(SN, ensure_ascii=False)).replace('__LONG__', json.dumps(LONG, ensure_ascii=False))
s = s.replace('</body>', JS + '\n</body>', 1)
open(f'{D}/Chat-Live.html', 'w', encoding='utf-8').write(s)
print('Chat-Live', len(s))
