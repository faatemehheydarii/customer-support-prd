import os,re
D='/home/claude/proto/screens'; idx=open('/home/claude/proto/index.html').read()
def patch(h,name):
    h=h.replace('history.back();return','parent.P.back();return')
    h=h.replace('location.href=t+".html"','parent.P.go(t)').replace('location.href=r[1]+".html"','parent.P.go(r[1])')
    h=h.replace('fetch(t+".html").then(function(r){return r.text()})','Promise.resolve(parent.P.src(t))')
    h=h.replace('new URLSearchParams(location.search).get("modal")','parent.P.modal')
    h=h.replace('location.pathname.split("/").pop().replace(".html","")',repr(name).replace("'",'"'))
    h=h.replace('"hint_"+location.pathname','"hint_'+name+'"')
    return h.replace('</script','<\\/script')
blocks=[]
for f in sorted(os.listdir(D)):
    n=f[:-5]; blocks.append(f'\n<!-- ===== SCREEN: {n} ===== -->\n<script type="text/html" id="s-{n}">\n{patch(open(os.path.join(D,f)).read(),n)}\n</script>')
note='''<!--
  دستیار پشتیبانی مشتری — پروتوتایپ کلیک‌پذیر (نسخهٔ تک‌فایل)
  Single-file bundle of the clickable prototype. Fictional demo data.
  STRUCTURE (for readers / AI tools):
  - The viewer (header + left nav + stage) is at the top. Nav groups: customer (mobile/desktop chat), admin panel, store management panel.
  - Every screen is a full HTML document stored below in <script type="text/html" id="s-SCREEN_NAME"> blocks
    (inside them "<\\/script" stands for a closing script tag).
  - Each screen's RULES array maps visible button/label text -> target screen; MODALS maps dialog buttons -> targets.
  - Screen names starting with W*/SW* are dialogs shown on top of a base screen.
-->'''
idx=idx.replace('<html lang="fa" dir="rtl">', note+'\n<html lang="fa" dir="rtl">',1)
js='''var P={modal:null,q:"",cn:null,hist:[],src:function(n){var e=document.getElementById("s-"+n);return e?e.textContent.replace(/<\\\\\\/script/g,"<\\/script"):""},
load:function(n,q){q=q||"";P.q=q;var mm=/modal=([^&]+)/.exec(q);P.modal=mm?mm[1]:null;var f=document.getElementById("f");f.removeAttribute("src");f.srcdoc=P.src(n)},
go:function(n){P.hist.push([P.cn,P.q]);P.cn=n;P.load(n)},back:function(){var h=P.hist.pop();if(h){P.cn=h[0];P.load(h[0],h[1])}}};
function open(n){var p=n.split("?");P.hist=[];P.cn=p[0];P.load(p[0],p[1]?"?"+p[1]:"")}'''
idx=re.sub(r'function open\(n\)\{[^\n]*\}\n', lambda m: js+'\n', idx,1)
assert 'P.load' in idx
idx=idx.replace('setArea("customer");\n</script>','addEventListener("DOMContentLoaded",function(){setArea("customer")});\n</script>',1)
assert 'DOMContentLoaded' in idx
idx=idx.replace('</body></html>',''.join(blocks)+'\n</body></html>')
open('/home/claude/bundle/Prototype-single-file.html','w').write(idx)
