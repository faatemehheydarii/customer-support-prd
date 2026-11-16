import json
G={
'customer':('مشتری','صفحه گفت‌وگو',[('Chat-Welcome','ح۱ خوش‌آمد'),('Chat-Clarify','ح۴ رفع ابهام'),('Chat-Typing','ح۲ در حال پاسخ'),('Chat-Answer','ح۳ پاسخ و تأیید حل'),('Chat-Closed','ح۸ بسته'),('Chat-Registering','ح۵ در حال ثبت'),('Chat-Registered','ح۶ درخواست ثبت شد'),('Chat-Human','ح۷ پشتیبان در گفت‌وگو'),('Chat-Error','ح۹ خطای سرویس'),('Chat-RegisterFailed','ح۱۰ شکست ثبت'),('Chat-SendFailed','ح۱۱ ارسال نشد'),('Chat-TooLong','ح۱۲ پیام بلند')]),
'admin':('ادمین','پنل ادمین',[('Login-Admin','ورود'),('Main','صف اقدام'),('Queue-Stopped','صف — پاسخ خودکار متوقف'),('Queue-Empty','صف خالی'),('Conversation-Queue','مکالمه — نمای صف'),('Conversation','مکالمه — نمای مالک'),('Conversation-Observer','مکالمه — نمای ناظر'),('Conversation-Closed','مکالمه — بسته'),('Bots','گفت‌وگوهای دستیار'),('Conversation-Bot','مکالمه — نمای دستیار'),('Conversation-Bot?modal=W1-Takeover','W1 تحویل از دستیار'),('Conversation?modal=W2-Resolve','W2 بستن مستند'),('Conversation?modal=W3-CloseUnconfirmed','W3 بستن بدون تأیید'),('Main?modal=W4-Stop','W4 توقف پاسخ خودکار'),('Conversation?modal=W5-Handback','W5 واگذاری')]),
'store':('فروشگاه','پنل مدیریت فروشگاه',[('Login-Store','ورود'),('Store-Discrepancies','مغایرت‌ها'),('Store-FixInventory','اصلاح موجودی'),('Store-FixConflict','اطلاعات متعارض'),('Store-Products','محصولات و گونه‌ها'),('Store-ProductEdit','ویرایش محصول'),('Store-Knowledge','دانش و سیاست'),('Store-KnowledgeEdit','ویرایش منبع'),('Store-Settings','تنظیمات'),('Store-Permissions','مجوزها'),('Store-Report','گزارش'),('Store-FixInventory?modal=SW1-CloseDiscrepancy','W1 بستن مغایرت'),('Store-Settings?modal=SW2-Threshold','W2 تأیید آستانه'),('Store-Permissions?modal=SW3-Grant','W3 اعطای مجوز'),('Store-ProductEdit?modal=SW4-Leave','W4 ترک صفحه'),('Denied-Role','دسترسی رد شد — نقش'),('Denied-Page','دسترسی رد شد — صفحه')]),
}
html='''<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>دستیار پشتیبانی — پروتوتایپ</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap">
<style>
:root{--bg:#eef3f2;--fg:#142624;--muted:#4f6260;--card:#fff;--border:#d3dcda;--pri:#0f766e;--sec:#e7f4f1;--deep:#0b3b38}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font-family:Vazirmatn,Tahoma,sans-serif;color:var(--fg);background:var(--bg);display:grid;grid-template-rows:auto 1fr;height:100vh}
header{display:flex;align-items:center;gap:16px;padding:10px 20px;background:var(--deep);color:#e6f2ef}
header b{font-size:15px}header small{color:#9cc9c1;font-size:12px}
.seg{display:flex;gap:4px;padding:4px;border-radius:12px;background:rgba(255,255,255,.08);margin-inline-start:12px}
.seg button{min-height:36px;padding:0 16px;border:0;border-radius:9px;background:transparent;color:#e6f2ef;font:inherit;font-size:14px;cursor:pointer}
.seg button[aria-pressed=true]{background:#fff;color:var(--deep);font-weight:600}
.hint{margin-inline-start:auto;font-size:12px;color:#9cc9c1}
.wrap{display:grid;grid-template-columns:260px 1fr;min-height:0}
nav{overflow:auto;padding:16px 12px;background:var(--card);border-inline-end:1px solid var(--border)}
nav h2{margin:4px 8px 10px;font-size:13px;color:var(--muted);font-weight:500}
nav button{display:block;width:100%;text-align:start;min-height:36px;padding:6px 10px;border:0;border-radius:8px;background:transparent;font:inherit;font-size:14px;color:var(--fg);cursor:pointer}
nav button:hover{background:var(--bg)}nav button[aria-current=true]{background:var(--sec);color:#0b3b38;font-weight:600}
.stage{position:relative;min-height:0;overflow:hidden;display:flex;align-items:center;justify-content:center;padding:20px}
.phone{width:390px;height:844px;border-radius:36px;background:#0b1514;padding:10px;box-shadow:0 20px 50px rgba(11,59,56,.25)}
.phone iframe{width:100%;height:100%;border:0;border-radius:28px;background:#fff}
.desk{width:1440px;height:900px;transform-origin:center center;border-radius:10px;overflow:hidden;box-shadow:0 20px 50px rgba(11,59,56,.2);background:#fff}
.desk iframe{width:100%;height:100%;border:0}
*{scrollbar-width:thin;scrollbar-color:#0f766e transparent}::-webkit-scrollbar{width:6px}::-webkit-scrollbar-thumb{background:#0f766e;border-radius:999px}::-webkit-scrollbar-button{display:none}
.dev{display:flex;gap:4px;margin-inline-start:8px}.dev[hidden]{display:none}
</style></head><body>
<header><div><b>دستیار پشتیبانی — پروتوتایپ</b><br><small>نسخه نمایشی · داده ساختگی</small></div>
<div class="seg" role="group" aria-label="ورودی">__TABS__</div>
<div class="seg dev" id="dev" role="group" aria-label="دستگاه"><button data-d="m" aria-pressed="true">موبایل</button><button data-d="d" aria-pressed="false">دسکتاپ</button></div>
<span class="hint">روی جای خالی بزنید تا نقاط کلیک‌پذیر نشان داده شوند</span></header>
<div class="wrap"><nav id="nav"></nav><div class="stage" id="stage"></div></div>
<script>
var G=__G__,area="customer",dev="m",cur=null;
var stage=document.getElementById("stage"),nav=document.getElementById("nav");
function frame(){var mobile=area==="customer"&&dev==="m";stage.innerHTML=mobile?'<div class="phone"><iframe id="f" title="صفحه"></iframe></div>':'<div class="desk" id="dk"><iframe id="f" title="صفحه"></iframe></div>';fit()}
function fit(){var d=document.getElementById("dk");if(!d)return;var s=Math.min((stage.clientWidth-40)/1440,(stage.clientHeight-40)/900,1);d.style.transform="scale("+s+")";d.style.margin=(-(900*(1-s))/2)+"px "+(-(1440*(1-s))/2)+"px"}
function open(n){var p=n.split("?");document.getElementById("f").src="screens/"+p[0]+".html"+(p[1]?"?"+p[1]:"")}
function mark(n){cur=n;nav.querySelectorAll("button").forEach(function(b){b.setAttribute("aria-current",b.dataset.n===n)})}
function setArea(a){area=a;document.querySelectorAll("[data-a]").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.a===a)});document.getElementById("dev").hidden=a!=="customer";
var g=G[a];nav.innerHTML="<h2>"+g[1]+"</h2>"+g[2].map(function(s){return'<button data-n="'+s[0]+'">'+s[1]+"</button>"}).join("");
nav.querySelectorAll("button").forEach(function(b){b.onclick=function(){open(b.dataset.n)}});frame();open(g[2][0][0]);mark(g[2][0][0])}
document.querySelectorAll("[data-a]").forEach(function(b){b.onclick=function(){setArea(b.dataset.a)}});
document.querySelectorAll("[data-d]").forEach(function(b){b.onclick=function(){dev=b.dataset.d;document.querySelectorAll("[data-d]").forEach(function(x){x.setAttribute("aria-pressed",x===b)});var n=cur;frame();open(n)}});
addEventListener("message",function(e){if(e.data&&e.data.proto==="screen")mark(e.data.name)});
addEventListener("resize",fit);
setArea("customer");
</script></body></html>'''
tabs=''.join(f'<button data-a="{k}" aria-pressed="{"true" if k=="customer" else "false"}">{v[0]}</button>' for k,v in G.items())
html=html.replace('__TABS__',tabs).replace('__G__',json.dumps(G,ensure_ascii=False))
open('/home/claude/proto/index.html','w',encoding='utf-8').write(html)
print('ok')
