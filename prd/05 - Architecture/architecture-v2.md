---
doc: docs/architecture-v2.md — افزوده معماری و طرح داده برای کمک به خرید (v2)
project: Customer Support — AI Customer Support Assistant
version: 0.1
status: "v2 — Pending Review (مسئول فنی)؛ پیشنهاد ChatGPT P1، بخش‌های سوم، چهارم و ششم"
last_updated: 2026-11-20
owner: مسئول فنی (DEP-06)
extends: [docs/architecture.md 0.2، docs/data-model.md 0.1]
change_note: "0.1 — v2 — CH-62: ماژول catalog، لایه ابزار، درگاه فایل، خروجی فهم، نگاشت ۱۲ مسئولیت P1، جدول‌های تازه (DEC-340)"
---

# ‏افزوده معماری v2 — کمک به خرید

> ‏**سطح این سند:** فقط آنچه EP-08 و زیرسازی مرحله سوم (DEC-321، DEC-324) به `architecture.md` و `data-model.md` می‌افزایند. همه اصل‌های آن دو سند برقرار می‌مانند: برنامه ماژولار واحد (DEC-275)، قواعد پیش از مدل و مستقل از مدل، مسیر انسان بی‌نیاز از مدل، هسته بی‌خبر از بستر. این سند جای خود را در آن دو سند نمی‌گیرد؛ پس از پذیرفتن v2 در آن‌ها ادغام می‌شود.
‏>
> ‏**همگام نبودن:** `architecture.md` و `data-model.md` هنوز با CH-54 همگام نشده‌اند (آستانه به دقیقه، نقش‌ها و مجوزهای پنل فروشگاه). این افزوده بر پایه PRD-04-DD 1.7 نوشته شده است.

## ‏۱. نگاشت ۱۲ مسئولیت P1 به ساختار موجود

> ‏P1 خواسته این مسئولیت‌ها جدا شوند، نه اینکه هرکدام سرویس جدا باشد. در مقیاس Prototype (یک فروشگاه، ۵ مکالمه هم‌زمان) همه در همان برنامه واحد می‌مانند و جدایی با مرز ماژول و lint کنترل می‌شود (DEC-282).

| ‏مسئولیت (P1) | ‏ماژول | ‏تغییر v2 | ‏قطعی / مدل |
| --- | --- | --- | --- |
| ‏Conversation Management | ‏`conversation` | ‏فهرست موضوع‌های مکالمه | ‏قطعی |
| ‏Intent Detection & Message Understanding | ‏`assistant` (گام فهم) | ‏خروجی تازه فهم (§۳) | ‏مدل |
| ‏Clarification | ‏`rules` + `assistant` | — | ‏قطعی (تصمیم) + مدل (نگارش) |
| ‏Knowledge Retrieval | ‏`reference` | — | ‏قطعی |
| ‏Product Search | ‏**`catalog` (تازه)** | ‏جست‌وجو با ورودی متن و ویژگی | ‏قطعی |
| ‏Product Recommendation | ‏`catalog` | ‏امتیاز انطباق و دلیل | ‏قطعی (امتیاز) + مدل (نگارش دلیل) |
| ‏Alternative Product Matching | ‏`catalog` | ‏نامزدها، فیلتر موجود معتبر، امتیاز شباهت | ‏قطعی |
| ‏Purchase Rescue | ‏`rules` (جدول مانع ← اقدام) + `assistant` | ‏تابع خالص `rescueAction(obstacle, context)` | ‏مدل (تشخیص مانع) + قطعی (اقدام) |
| ‏Human Handoff | ‏`handoff` | ‏خلاصه با «کارهای دستیار» (از رویدادها) و «اقدام پیشنهادی» | ‏قطعی؛ متن خلاصه با مدل |
| ‏Admin Operations | ‏`handoff`، `settings`، `reference` | ‏ویژگی، تصویر، قابلیت‌ها، لحن | ‏قطعی |
| ‏Conversation Analytics | ‏`events` | ‏EV-28 تا EV-33، KM-21 تا KM-27 | ‏قطعی |
| ‏Tool / Integration Layer | ‏**`tools` (تازه)** + `ports/` | ‏فهرست ابزارها با سطح دسترسی (§۴)؛ `MediaStoragePort` | — |

## ‏۲. ماژول `catalog` (تازه)

| ‏موضوع | ‏تصمیم |
| --- | --- |
| ‏مسئولیت | ‏جست‌وجوی محصول، پیشنهاد با دلیل (US-08-01)، یافتن و رتبه‌بندی جایگزین (US-08-02)، گزینه ارزان‌تر (US-08-03) |
| ‏ورودی | ‏`SearchQuery { text?, attributes: {attrId: value[]}, budget?, size?, color?, image?: reserved }`؛ `image` فقط در نوع تعریف شده و در Prototype خطای «پشتیبانی نمی‌شود» می‌دهد (DEC-324) |
| ‏داده | ‏فقط نسخه تأییدشده DS-01، DS-10 تا DS-12؛ نتیجه موجودی از `rules` (نه خواندن مستقیم DS-02) |
| ‏خروجی | ‏فهرست مرتب `{productId, variantId?, score, matched[], diffs[]}`؛ `matched` و `diffs` داده‌اند، نه متن؛ متن را `assistant` با مدل می‌نویسد و با همین داده می‌سنجد (CR-05) |
| ‏پیاده‌سازی Prototype | ‏فیلتر و امتیاز در حافظه روی کاتالوگ تأییدشده (≤ چند صد محصول)؛ بدون جست‌وجوی برداری |
| ‏درگاه آینده | ‏`SearchPort` با همان ورودی و خروجی؛ پیاده‌سازی برداری یا تصویری بعداً بی‌تغییر هسته (انتشار ۳) |
| ‏کارایی | ‏هیچ فراخوانی مدل تازه‌ای نمی‌افزاید؛ فقط یک کوئری پایگاه داده در هر پاسخ. بودجه صدک ۹۵ ≤ ۱۰ ثانیه (NFR-02-1) بی‌تغییر |

## ‏۳. خروجی گام فهم (`ModelPort.understand`)

```ts
interface Understanding {
  intent: Intent            // VL-15
  topic: Topic              // VL-16
  entities: { product?: string; variant?: {color?: string; size?: string}; orderId?: string;
              budget?: {max?: number; min?: number}; use?: string; attributes?: Record<string, string[]> }
  missing: string[]         // اطلاعات ناقص برای پاسخ
  obstacles: Obstacle[]     // VL-17
}
// compose(input) اکنون tone: {style: 'formal'|'casual', note?: string} هم می‌گیرد؛ note فقط راهنمای سبک است و
// پس از سنجش متن (CR-05) هیچ ادعایی بیرون از نتیجه قواعد پذیرفته نمی‌شود.
```

- ‏اعتبارسنجی با Zod مثل امروز؛ مقدار بیرون از فهرست VL = خالی.
- ‏`buildModelInput()` همچنان تنها سازنده ورودی مدل است؛ کاتالوگ کامل به مدل فرستاده نمی‌شود، فقط محصولات پیشنهادشده و ویژگی‌هایشان برای نگارش (ENV-62).

## ‏۴. لایه ابزار (`tools`) — زیرسازی Agentic

| ‏ابزار | ‏کار | ‏دسترسی | ‏تأیید لازم | ‏در Prototype |
| --- | --- | --- | --- | --- |
| ‏`catalog.search` | ‏جست‌وجو و پیشنهاد | ‏خواندنی | — | ‏فعال |
| ‏`catalog.alternatives` | ‏جایگزین | ‏خواندنی | — | ‏فعال |
| ‏`inventory.check` | ‏نتیجه موجودی از `rules` | ‏خواندنی | — | ‏فعال |
| ‏`knowledge.lookup` | ‏دانش و سیاست تأییدشده | ‏خواندنی | — | ‏فعال |
| ‏`order.sampleStatus` | ‏سفارش نمونه | ‏خواندنی | — | ‏فعال |
| ‏`handoff.create` | ‏ثبت ارجاع | ‏**نوشتنی (داخلی)** | — | ‏فعال؛ تنها کنش نوشتنی |
| ‏`order.place`، `return.request` | ‏خرید، درخواست مرجوعی | ‏نوشتنی (بیرونی) | ‏**تأیید صریح مشتری** + ابزار معتبر | ‏**فقط تعریف؛ غیرفعال** (DEC-322؛ انتشار ۴) |

- ‏هر ابزار در یک فهرست ثابت با `access: 'read'|'write'` و `confirmation: 'none'|'customer'|'human'` تعریف می‌شود. `assistant` فقط ابزارهای فعال را صدا می‌زند و ابزار نوشتنی بیرونی بدون ثبت تأیید اجرا نمی‌شود (قاعده سمت سرور، نه مدل).
- ‏مدل ابزار را انتخاب نمی‌کند: ترتیب فراخوانی را `assistant` با قاعده از روی نیت تعیین می‌کند. انتخاب ابزار با مدل (function calling) تصمیم انتشار ۴ است.

## ‏۵. تصویر محصول و درگاه فایل

| ‏موضوع | ‏تصمیم |
| --- | --- |
| ‏درگاه | ‏`MediaStoragePort { put(file) → key; url(key, size: 'card' | ‏'full') }` در `src/ports/` |
| ‏پیاده‌سازی | ‏فضای ذخیره شیء‌گرای میزبان (پیشنهاد: لیارا؛ منتظر بحث گروه، DEP-25)؛ در محیط محلی پوشه دیسک |
| ‏نسخه کوچک | ‏هنگام بارگذاری، نسخه کارت (حدود ۱۲۰×۱۵۲ با دو برابر چگالی) ساخته می‌شود؛ صفحه گفت‌وگو فقط نسخه کارت را می‌گیرد |
| ‏حدها | ‏JPG، PNG، WebP؛ ≤ ۲ مگابایت؛ ≤ ۸ تصویر (A-36)؛ بررسی نوع فایل از محتوا، نه فقط پسوند |
| ‏حریم خصوصی | ‏تصویر کاتالوگ داده عمومی فروشگاه است؛ تصویر از مشتری دریافت نمی‌شود (جست‌وجوی تصویری در Prototype نیست) |

## ‏۶. API تازه

| ‏مسیر | ‏روش | ‏دسترسی | ‏کار | ‏استوری |
| --- | --- | --- | --- | --- |
| ‏`/api/store/attributes` | ‏GET، POST | ‏مدیر؛ کارمند با مجوز «محصولات و گونه‌ها» | ‏تعریف ویژگی (پیش‌نویس، تأیید) | ‏US-08-05 |
| ‏`/api/store/products/:id/images` | ‏GET، POST، PATCH | ‏همان | ‏بارگذاری، ترتیب، اصلی، متن جایگزین | ‏US-08-05 |
| ‏`/api/store/settings` (افزوده) | ‏PUT | ‏مدیر؛ کارمند با مجوز «تنظیمات» | ‏`assistant_capabilities`، `tone` | ‏US-08-06 |
| ‏`/api/admin/conversations/:id/review` | ‏POST | ‏ادمین | ‏نشانه بازبینی و «پاسخ درست» | ‏DEC-338 |
| ‏`/api/store/report` (افزوده) | ‏GET | ‏مدیر | ‏دسته «خرید و درخواست‌ها»، موضوع‌ها | ‏DEC-336 |

## ‏۷. طرح داده (افزوده به `data-model.md`)

| ‏جدول | ‏ستون‌ها | ‏محل منطقی |
| --- | --- | --- |
| ‏`attribute_def` | ‏`id`، `created_at` | ‏DS-10 |
| ‏`attribute_def_version` | ‏`id`، `attribute_id`، `version_no`، `approval_status`، `name`، `value_type` (VL-18)، `allowed_values` (jsonb: `[{value, synonyms[]}]`)، `level` (محصول / گونه)، `searchable`، `is_active`، `approved_at`، `approved_by`، `created_at` | ‏DS-10 |
| ‏`product_version` (تغییر) | ‏`attributes` (jsonb) ← **`attribute_values` (jsonb: `{attributeId: value[]}`)**؛ اعتبارسنجی با تعریف تأییدشده هنگام ذخیره | ‏DS-01 |
| ‏`product_image` | ‏`id`، `product_id`، `version_no`، `approval_status`، `storage_key`، `card_key`، `color` (اختیاری)، `sort_order`، `is_primary`، `alt_text`، `approved_at`، `approved_by`، `created_at` · قید: یک `is_primary` تأییدشده برای هر محصول | ‏DS-11 |
| ‏`product_relation` | ‏`id`، `from_product_id`، `to_product_id`، `type` (VL-19)، `origin`، `created_at` · یکتا: (`from`، `to`، `type`) | ‏DS-12 |
| ‏`message` (تغییر) | ‏`understanding` (jsonb؛ فقط پیام مشتری؛ بدون متن آزاد مدل)، `cards` (jsonb؛ فقط پیام دستیار) | ‏DS-05 |
| ‏`conversation` (تغییر) | ‏`topics` (VL-16[])، `last_topic` | ‏DS-05 |
| ‏`review_mark` (تغییر) | ‏`location` (گفت‌وگوهای دستیار / نمای مکالمه)، `correct_answer` (اختیاری، ≤ ۲۰۰۰) | ‏DS-05 |
| ‏`store_settings` (تغییر) | ‏`assistant_capabilities` (jsonb: `{recommend, alternatives, rescue}`)، `tone_style` (VL-20)، `tone_note` (≤ ۲۰۰) | ‏DS-09 |
| ‏`event` (تغییر) | ‏`type` تا EV-33؛ `payload` برای EV-28 تا EV-33 طبق EP-06 §6.1 | ‏DS-08 |

- ‏**شاخص‌ها:** `attribute_values` با GIN برای جست‌وجوی ویژگی؛ `event(type, occurred_at)` برای KM-21 تا KM-27.
- ‏**seed:** کاتالوگ نمونه v2 (۱۲ محصول، ویژگی‌ها، رابطه‌ها) در `design/generators/v2_catalog.py` و Sample Knowledge Base §v2؛ تصویرها جای خالی‌اند تا تیم محصول تصویر ساختگی بارگذاری کند.

## ‏۸. ریسک‌های فنی تازه

| ‏ریسک | ‏پاسخ |
| --- | --- |
| ‏تشخیص نیت و مانع در فارسی ضعیف باشد (A-37) | ‏اجرای آزمایشی روز ۴ با ۲۰ پیام خرید؛ اگر نشد، US-08-03 خاموش (کلید قابلیت) و در ترتیب کاهش اول |
| ‏متن دلیل یا تفاوت ادعای بی‌پشتوانه کند | ‏`matched` و `diffs` داده قطعی‌اند؛ سنجش CR-05 هر ویژگی یا عدد بیرون از آن‌ها را رد می‌کند |
| ‏فضای ذخیره فایل در دسترس نباشد | ‏کارت بی‌تصویر (US-08-01 حالت خطا)؛ بارگذاری در پنل خطای کوتاه می‌دهد |
| ‏جست‌وجوی در حافظه با رشد کاتالوگ کند شود | ‏فقط برای Prototype؛ `SearchPort` برای پایلوت |

## ‏۹. تصمیم برای ثبت در Master Index

| ‏شناسه | ‏تصمیم | ‏وضعیت |
| --- | --- | --- |
| ‏DEC-340 | ‏**v2 — معماری کمک به خرید:** ماژول تازه `catalog` (جست‌وجو، پیشنهاد، جایگزین؛ قطعی؛ ورودی متن و ویژگی، تصویر رزرو)، لایه `tools` با سطح دسترسی و تأیید (همه خواندنی جز `handoff.create`؛ ابزار خرید فقط تعریف)، `MediaStoragePort`، خروجی گسترده `understand` و `tone` در `compose`، جدول‌های `attribute_def*`، `product_image`، `product_relation` و ستون‌های تازه | ‏پیشنهادی؛ منتظر مسئول فنی |
