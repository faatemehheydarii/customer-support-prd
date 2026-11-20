"""v2 — CH-62: architecture addendum (P1 parts 3, 4). DEC-340, DEP-25 pointer. Master Index."""
from v2lib import *
from rtl_fix import fix
p = B + '05 - Architecture/architecture-v2.md'
s = open(p, encoding='utf-8').read(); open(p, 'w', encoding='utf-8').write(fix(s))
DECS = [row('DEC-340', '**v2 — معماری کمک به خرید:** ماژول تازه `catalog` (جست‌وجو، پیشنهاد، جایگزین؛ قطعی؛ ورودی متن و ویژگی، تصویر رزرو)، لایه `tools` با سطح دسترسی و تأیید (همه خواندنی جز `handoff.create`؛ ابزار خرید فقط تعریف و غیرفعال)، `MediaStoragePort`، خروجی گسترده `understand` و `tone` در `compose`؛ جدول‌های `attribute_def*`، `product_image`، `product_relation` و ستون‌های تازه. همان برنامه ماژولار واحد (DEC-275)؛ بی فراخوانی مدل تازه', D, '05 - Architecture/architecture-v2.md؛ پیشنهاد ChatGPT P1؛ منتظر مسئول فنی', 'CH-62')]
def mi(s):
    s = re.sub(r'^version: .*$', 'version: 1.19', s, count=1, flags=re.M)
    s = mi_dec(s, DECS)
    s = after_line(s, '| ‏`05 - Architecture/tech-stack.md` (P-03) |', row('`05 - Architecture/architecture-v2.md` *(v2)*', 'Pending Review — افزوده معماری و طرح داده کمک به خرید؛ منتظر مسئول فنی؛ پس از پذیرفتن v2 در architecture.md و data-model.md ادغام می‌شود', '**0.1 (CH-62 v2)**', D, 'v2'))
    s = mi_ch(s, row('CH-62', D, '**v2 — پیشنهاد ChatGPT، مورد P1 (معماری):** DEC-340. افزوده تازه `05 - Architecture/architecture-v2.md` 0.1: نگاشت ۱۲ مسئولیت P1 به ماژول‌ها، ماژول `catalog`، خروجی فهم، لایه ابزار با سطح دسترسی، درگاه فایل تصویر، API و جدول‌های تازه، ریسک‌های فنی. architecture.md و data-model.md دست نخوردند (هنوز با CH-54 هم همگام نیستند)', '05 - Architecture (تازه: architecture-v2.md)، Master Index'))
    return s
rw(M, mi)
