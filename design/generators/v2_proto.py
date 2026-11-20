"""v2 — CH-61: prototype build. Runs the v1 chain (proto, polish, polish4..8, proto_live, proto_index)
with v2 additions: store nav item and SCR-28, static chat screens for EP-08, and a live-chat catalog
(search with reasons, alternatives for an out-of-stock variant, cheaper options, comparison). Reads
/home/claude/canvas/project; writes /home/claude/proto."""
import os, re, json, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, G)
from v2_catalog import CAT, REL
PS = '/home/claude/proto/screens'
os.makedirs(PS, exist_ok=True)

# ---- 1. proto.py with v2 rules
src = open(f'{G}/proto.py', encoding='utf-8').read()
src = src.replace("('محصولات و گونه‌ها','Store-Products'),", "('محصولات و گونه‌ها','Store-Products'),('ویژگی‌های کاتالوگ','Store-Attributes'),", 1)
assert "('ویژگی‌های کاتالوگ','Store-Attributes')" in src
V2R = ("\n'Store-Attributes':{'rules':STORE_NAV},\n"
       "'Chat-Products':{'rules':CHAT_HDR+[('بله، ممنون','Chat-Closed'),('نه، هنوز نه','Chat-Registering')]},\n"
       "'Chat-Alternative':{'rules':CHAT_HDR+[('بله، ممنون','Chat-Closed'),('نه، هنوز نه','Chat-Registering')]},\n"
       "'Chat-Rescue':{'rules':CHAT_HDR+[('بله، ممنون','Chat-Closed'),('نه، هنوز نه','Chat-Registering')]},\n"
       "}\nRT=" + "\'\'\'")
src = src.replace("\n}\nRT='''", V2R, 1)
assert "'Store-Attributes':{'rules':STORE_NAV}" in src
exec(compile(src, 'proto.py', 'exec'), {'__name__': '__main__'})

# ---- 2. polish chain
for sc in ['polish.py', 'polish4.py', 'polish5.py', 'polish6.py', 'polish7.py', 'polish8.py']:
    subprocess.run([sys.executable, f'{G}/{sc}', PS], check=True, stdout=subprocess.DEVNULL)

# ---- 3. live chat with catalog
L = open(f'{G}/proto_live.py', encoding='utf-8').read()
CSS = '''.pc{display:grid;gap:8px;margin-top:10px}
.pcard{display:flex;gap:10px;align-items:stretch;padding:8px;border-radius:14px;background:#ffffff;border:1px solid #d3dcda;color:#142624}
.pimg{flex:none;width:60px;height:76px;border-radius:10px;background:#eef3f2;display:flex;align-items:center;justify-content:center;color:#7d8e8c}
.pbody{display:grid;gap:2px;min-width:0;align-content:start}
.pname{font-weight:600;font-size:15px;line-height:22px}
.pprice{font-size:14px;line-height:20px}
.pwhy{font-size:13px;line-height:20px;color:#4f6260}
.pdiff{font-size:13px;line-height:20px;color:#0b3b38;background:#e7f4f1;border-radius:8px;padding:2px 8px;justify-self:start}
</style>'''
L = L.replace("#cnt .e{color:#b42318}\n.act .chip[disabled]{cursor:default}\n</style>", "#cnt .e{color:#b42318}\n.act .chip[disabled]{cursor:default}\n" + CSS, 1)
assert '.pcard{' in L
V2JS = r'''/* ---- v2 (CH-61): catalog, recommendation, alternatives, purchase rescue ---- */
var CAT=__CAT__,REL=__REL__,lastShown=[];
var GAR='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3 4 6l1.5 4L8 9v12h8V9l2.5 1L20 6l-5-3a3 3 0 0 1-6 0z"/></svg>';
var NOTE='<span style="display:block;margin-top:8px;font-size:14px;line-height:22px;color:#4f6260">';
function money(n){return fa(String(n).replace(/\B(?=(\d{3})+(?!\d))/g,"٬"))+" تومان"}
function th(n){return fa(String(Math.round(n/1000)))+" هزار تومان"}
function card(p,v,line,dif){return '<div class="pcard"><span class="pimg" role="img" aria-label="تصویر '+p.n+'">'+GAR+'</span><span class="pbody"><span class="pname">'+p.n+(v?" · "+v:"")+'</span><span class="pprice">'+money(p.p)+'</span><span class="'+(dif?"pdiff":"pwhy")+'">'+line+'</span></span></div>'}
function cards(a){return '<div class="pc">'+a.join("")+'</div>'}
function keys(p,c,z){return Object.keys(p.st).filter(function(k){var a=k.split("|");return(!c||norm(a[0])===c)&&(!z||a[1]===z)})}
function allOut(p,c,z){var k=keys(p,c,z);return k.length>0&&k.every(function(x){return p.st[x]==="out"})}
var SEAS=[["تابستان","تابستان|تابستون"],["زمستان","زمستان|زمستون"],["پاییز","پاییز|پائیز"],["بهار","بهار"]];
var USES=[["اداری","محل کار|اداری|اداره|سر ?کار"],["مهمانی","مهمانی|مهمونی|مجلسی"],["روزمره","روزمره|روزانه"]];
var MATS=["لینن ترکیبی","لینن","نخی","کتان","کرپ","جین","پشمی","چرم","ابریشم"];
var COLS=["مشکی","کرم","سرمه ای","زیتونی","سفید","طوسی","آبی روشن","آبی","صورتی","قرمز"];
var NUMW={"یک":1,"یه":1,"دو":2,"سه":3,"چهار":4,"پنج":5};
function parseQ(t){var q={},i;
 if(/مانتو/.test(t))q.cat="مانتو";else if(/شلوار/.test(t))q.cat="شلوار";else if(/شال|روسری/.test(t))q.cat="شال و روسری";
 SEAS.forEach(function(x){if(new RegExp(x[1]).test(t))q.s=x[0]});
 USES.forEach(function(x){if(!q.u&&new RegExp(x[1]).test(t))q.u=x[0]});
 for(i=0;i<MATS.length;i++)if(t.indexOf(MATS[i])>=0){q.m=MATS[i];break}
 for(i=0;i<COLS.length;i++)if(t.indexOf(COLS[i])>=0){q.c=COLS[i];break}
 if(/سیاه/.test(t))q.c="مشکی";
 var m=/(تا|زیر|کمتر از|حداکثر|حدود)\s*(\d+(?:[.\/]\d+)?|یک|یه|دو|سه|چهار|پنج)\s*(میلیون|تومن|تومان|هزار)?/.exec(t);
 if(m){var v=NUMW[m[2]]||parseFloat(m[2].replace("/","."));if(m[3]==="هزار")v*=1000;else if(v<100)v*=1e6;q.b=v}
 q.z=pSize(t);return q}
function search(q){var r=CAT.filter(function(p){if(q.cat&&p.cat!==q.cat)return false;if(q.s&&p.s.indexOf(q.s)<0)return false;if(q.u&&p.u.indexOf(q.u)<0)return false;if(q.m&&p.m!==q.m)return false;
 if((q.c||q.z)&&!keys(p,q.c,q.z).length)return false;if(q.b&&p.p>q.b)return false;if(allOut(p,q.c,q.z))return false;return true});
 if(q.b)r.sort(function(a,b){return Math.abs(q.b-a.p)-Math.abs(q.b-b.p)});return r}
function why(p,q){var w=[];if(q.s)w.push(p.s.length>1?p.s.join(" و "):(p.s[0]==="تابستان"?"تابستانه":p.s[0]));w.push(p.m);if(q.u)w.push(q.u==="اداری"?"مناسب محل کار":q.u==="مهمانی"?"مناسب مهمانی":"روزمره");if(q.c)w.push("رنگ "+q.c.replace("سرمه ای","سرمه‌ای"));if(q.b)w.push("در بودجه شما");return w.join(" · ")}
function nameIn(t){return CAT.filter(function(p){return new RegExp("(^|\\s)"+norm(p.n)+"($|\\s|[،؟?.!])").test(t)})}
function show(q){var r=search(q);
 if(!r.length){var miss=q.m&&!CAT.some(function(p){return p.m===q.m})?" جنس «"+q.m+"» در کاتالوگ این فروشگاه نیست.":"";
  grp(["در کاتالوگ فروشگاه محصولی با همه این ویژگی‌ها پیدا نکردم."+miss+" اگر یکی از ویژگی‌ها را تغییر بدهید، دوباره می‌گردم."]);return}
 var more=r.length>3;r=r.slice(0,3);lastShown=r;
 answer([(more?"چند گزینه با خواسته شما جور درمی‌آیند؛ این سه تا:":"این‌ها با خواسته شما جور درمی‌آیند:")+cards(r.map(function(p){return card(p,"",why(p,q))}))+NOTE+(more?"رنگ یا بازه قیمت خاصی مد نظرتان است؟":"برای موجودی هرکدام، رنگ و سایز را بگویید.")+"</span>"])}
function isRel(a,b){return REL.some(function(r){return r[0]===a.id&&r[1]===b.id&&r[2]==="جایگزین"})}
function simi(ref,p){return(p.m===ref.m?1:0)+(p.s.some(function(x){return ref.s.indexOf(x)>=0})?1:0)+(p.u.some(function(x){return ref.u.indexOf(x)>=0})?1:0)+(p.l===ref.l?1:0)+(p.f===ref.f?1:0)+(isRel(ref,p)?1:0)}
function alts(ref,col,size){var c=[];
 Object.keys(ref.st).forEach(function(k){var a=k.split("|");if(a[1]===size&&a[0]!==col&&ref.st[k]==="in")c.push({p:ref,col:a[0],sc:100})});
 CAT.forEach(function(p){if(p===ref||p.cat!==ref.cat)return;var cs=Object.keys(p.st).filter(function(k){return k.split("|")[1]===size&&p.st[k]==="in"}).map(function(k){return k.split("|")[0]});if(!cs.length)return;
  var cc=cs.indexOf(col)>=0?col:cs[0];c.push({p:p,col:cc,sc:simi(ref,p)+(cc===col?2:0)-Math.abs(p.p-ref.p)/1e7})});
 c.sort(function(a,b){return b.sc-a.sc});return c.slice(0,3)}
function fdiff(ref,p,n){var d=[];if(p.m!==ref.m)d.push(p.m);if(p.l&&p.l!==ref.l)d.push("قد "+p.l+(n?" به‌جای "+ref.l:""));if(p.f&&p.f!==ref.f)d.push("فرم "+p.f+(n?" به‌جای "+ref.f:""));return d}
function adiff(ref,x,col){var d=[];if(x.col!==col)d.push("رنگ "+x.col+" به‌جای "+col);if(x.p!==ref){var f=fdiff(ref,x.p,true);if(f.length&&f[0]===x.p.m)f.push(f.shift());d=d.concat(f.slice(0,2));var dp=ref.p-x.p.p;if(dp)d.push(th(Math.abs(dp))+(dp>0?" ارزان‌تر":" گران‌تر"))}return d.join(" · ")}
function cheaper(ref){var c=CAT.filter(function(p){return p!==ref&&p.cat===ref.cat&&p.p<ref.p&&Object.keys(p.st).some(function(k){return p.st[k]==="in"})});
 c.sort(function(a,b){return simi(ref,b)-simi(ref,a)});c=c.slice(0,3);
 if(!c.length){grp(["گزینه موجود ارزان‌تری در همین دسته پیدا نکردم. اگر بخواهید، با پشتیبان صحبت کنید."]);return}
 lastShown=c;answer(["اگر بودجه‌تان کمتر است، این "+(ref.cat==="مانتو"?"مانتوهای":ref.cat==="شلوار"?"شلوارهای":"شال و روسری‌های")+" مشابه موجودند:"+cards(c.map(function(p){return card(p,"",fdiff(ref,p,false).slice(0,2).concat([th(ref.p-p.p)+" ارزان‌تر"]).join(" · "),true)}))])}
function compare(a,b){var row=function(l,x,y){return '<span style="display:block">'+l+": "+a.n+" "+x+" · "+b.n+" "+y+"</span>"};
 answer(["تفاوت این دو در اطلاعات فروشگاه:"+NOTE.replace("color:#4f6260","color:#142624")+row("جنس",a.m,b.m)+row("فصل",a.s.join(" و "),b.s.join(" و "))+row("کاربرد",a.u.join(" و "),b.u.join(" و "))+row("قد",a.l,b.l)+row("فرم",a.f,b.f)+row("قیمت",money(a.p),money(b.p))+"</span>"+NOTE+"انتخاب با شماست؛ اگر بگویید چه چیزی برایتان مهم‌تر است، کمکتان می‌کنم.</span>"])}
function v2route(t){var names=nameIn(t);
 if(names.length>=2&&/بهتر|کدوم|کدام|فرق|مقایسه/.test(t)){compare(names[0],names[1]);return true}
 if(/گرون|گران|ارزون|ارزان|قیمتش زیاد|بودجه ?م/.test(t)&&!/تخفیف|کد/.test(t)&&(names.length||lastShown.length)){cheaper(names[0]||lastShown[0]);return true}
 if(/مطمئن نیستم|نمی ?دونم کدوم|مرددم|دودل/.test(t)){grp(["چه چیزی برایتان مهم‌تر است: قیمت، جنس، یا زمان رسیدن؟"]);return true}
 var q=parseQ(t);if(q.cat&&!names.length&&!/موجود/.test(t)){show(q);return true}
 return false}
function stock(){var p=CAT[0],col=clar.c,size=clar.s,ok=p.st[col+"|"+size]==="in";var h="مانتو الف، "+col+"، "+size+" طبق اطلاعات فروشگاه امروز ساعت ۱۰:۳۰ "+(ok?"موجود است.":"موجود نیست.");
 var RES='<span style="display:block;margin-top:6px;font-size:14px;line-height:22px;color:#4f6260">این به معنای رزرو نیست و موجودی ممکن است تا زمان خرید تغییر کند.</span>';
 aw=null;clar={s:null,c:null,act:null};if(ok){answer([h+RES]);return}
 var a=alts(p,col,size);if(!a.length){answer([h+" گزینه موجود دیگری در همین سایز پیدا نکردم."]);return}
 lastShown=a.map(function(x){return x.p});answer([h+" این‌ها نزدیک‌ترین گزینه‌های موجود در سایز "+size+" هستند:"+cards(a.map(function(x){return card(x.p,x.col+" · "+size,adiff(p,x,col),true)}))+RES])}
'''
L = re.sub(r'^function stock\(\)\{.*?\n aw=null;clar=\{s:null,c:null,act:null\};answer\(\[h\]\)\}\n', '', L, count=1, flags=re.S | re.M)
assert 'function stock(){var ok=' not in L
L = L.replace('/* ---- intents ---- */', V2JS + '/* ---- intents ---- */', 1)
L = L.replace(" var best=null,bs=0;FAQ.forEach", " if(v2route(t))return;\n var best=null,bs=0;FAQ.forEach", 1)
assert 'if(v2route(t))return;' in L
PRE = ''' products:function(){send("سلام، یه مانتو تابستونه برای محل کار می‌خوام، تا سه میلیون")},
 alt:function(){send("مانتو الف کرم سایز L موجوده؟")},
 rescue:function(){send("سلام، یه مانتو تابستونه برای محل کار می‌خوام، تا سه میلیون");send("مانتو الف رو دیدم ولی یه کم گرونه. ارزون‌تر ندارید؟")},
 compare:function(){send("مانتو الف بهتره یا مانتو پ؟")},
 nores:function(){send("مانتو چرم دارید؟")},
'''
L = L.replace(" sendfail:function(){local=\"sendfail\";send(ASK)},", PRE + " sendfail:function(){local=\"sendfail\";send(ASK)},", 1)
assert 'products:function' in L
L = L.replace("JS = JS.replace('__FAQ__'", "JS = JS.replace('__CAT__', json.dumps(CAT, ensure_ascii=False)).replace('__REL__', json.dumps(REL, ensure_ascii=False))\nJS = JS.replace('__FAQ__'", 1)
assert "__CAT__', json.dumps" in L
exec(compile(L, 'proto_live.py', 'exec'), {'__name__': '__main__', 'CAT': CAT, 'REL': REL})

# ---- 4. index with v2 entries
I = open(f'{G}/proto_index.py', encoding='utf-8').read()
I = I.replace("('Chat-Live?s=welcome', 'ح۱ شروع گفت\\u200cوگو'),",
              "('Chat-Live?s=welcome', 'ح۱ شروع گفت\\u200cوگو'), ('#', 'کمک به خرید (v2)'), ('Chat-Live?s=products', 'ح۱۶ پیشنهاد محصول با دلیل'), ('Chat-Live?s=alt', 'ح۱۷ جایگزین برای ناموجود'), ('Chat-Live?s=rescue', 'ح۱۸ تردید در قیمت'), ('Chat-Live?s=compare', 'مقایسه دو محصول'), ('Chat-Live?s=nores', 'جست‌وجوی بی‌نتیجه'), ('#', 'مسیرهای پشتیبانی'),", 1)
assert 's=products' in I
I = I.replace("('Store-ProductEdit','ویرایش محصول'),", "('Store-ProductEdit','ویرایش محصول (ویژگی‌ها و تصویرها)'),('Store-Attributes','ویژگی‌های کاتالوگ'),", 1)
assert 'Store-Attributes' in I
exec(compile(I, 'proto_index.py', 'exec'), {'__name__': '__main__'})
print('v2 proto ok')
