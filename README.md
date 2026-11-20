<div dir="rtl">

# دستیار هوشمند پشتیبانی مشتری — مخزن PRD، Spec Kit و بک‌لاگ

‏AI-Powered Customer Support Assistant for E-commerce *(نام کاری — Q-08)*

این مخزن سه لایه دارد:

| ‏لایه | ‏پوشه | ‏نقش |
|---|---|---|
| ‏PRD (منبع حقیقت) | ‏`prd/` | ‏Master Index، ۳۸ سند بخش‌ها و PRD نهایی 0.9 — نسخه همگام‌شده پس از Q-42 |
| ‏Spec Kit | ‏`.specify/`، `specs/` | ‏اصول پروژه (constitution)، spec و plan و tasks هر اپیک، ساخته‌شده **از روی PRD** |
| ‏بک‌لاگ | ‏`BACKLOG.md` + GitHub Issues | ‏کارها، مایلستون‌ها و زمان‌بندی؛ Issues از `tasks.md` هر اپیک ساخته می‌شوند |

## ‏قواعد

1. ‏**PRD منبع حقیقت است.** هیچ spec یا task تصمیم تازه نمی‌گیرد؛ هر تفاوت با PRD باید با شناسه CH در `prd/00 - Master Project Index.md` ثبت شود.
2. ‏**ردیابی:** هر spec و task به شناسه‌های PRD ارجاع می‌دهد (US، AC، FR، RULE، NFR، ENV، DEP، EC، FS).
3. ‏**انتشارهای ۳ و ۴** (Shopping Assistant و Agentic Commerce) «جهت، تعهدنشده»‌اند (DEC-205)؛ در بک‌لاگ فقط کار کشف و تصمیم دارند، نه ساخت.
4. ‏متن فارسی راست‌به‌چپ نوشته می‌شود (DEC-18).

## ‏ساختار

```
prd/
  00 - Master Project Index.md      ← منبع حقیقت تصمیم‌ها
  03 - PRD Sections/                 ← ۳۸ سند Approved
  04 - Final PRD.md / .docx          ← PRD نهایی 0.9
.specify/memory/constitution.md      ← اصول پروژه (برگرفته از SP، ND، CR)
specs/                               ← یک پوشه برای هر اپیک: spec.md، plan.md، tasks.md
BACKLOG.md                           ← نقشه بک‌لاگ و زمان‌بندی
```

> ‏منابع ورودی (BRD، سند ایده، تمپلیت، تحقیقات بازار) و نسخه‌های Markdown آن‌ها در Claude Project «Customer Support» می‌مانند؛ Source Index در `prd/` ارجاع داده می‌شود.

## ‏گردش کار Spec Kit

‏`/speckit-specify` ← `/speckit-clarify` ← `/speckit-plan` ← `/speckit-tasks` ← `/speckit-analyze` ← ‏Issues ← `/speckit-implement`

## ‏نسخه‌های پایه

| ‏برچسب | ‏معنا |
|---|---|
| ‏`v1` | ‏PRD تا CH-53 (پوشه `design/` در این برچسب هنوز در حالت CH-52 است) |
| ‏`v2` | ‏PRD تا CH-55، همراه طراحی (`design/screens`)، پروتوتایپ (`design/prototype`) و اسکریپت‌های ساخت (`design/generators`) |

‏هر تغییر پس از v2 یک CH در یک commit جداست و در Master Index با «پایه: v2» ثبت می‌شود؛ برگرداندن آن با `git revert` همان commit انجام می‌شود (Master Index §5.1).

</div>
