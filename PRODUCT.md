# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

shadcn/ui (React + Tailwind + Radix) for UI components — recommended by Claude and accepted by the product owner on 2026-11-15. Framework, database and hosting are decided in the architecture document (BACKLOG P-03).

## Users

- **Customer** of an online shop (mobile, in a browser, no login) asking pre- and post-purchase questions: product details, size, stock, shipping, order status, returns.
- **Support admin** of the shop (desktop panel) who must find every request that needs a human within 60 seconds, take ownership and reply.
- **Store owner / data owner** (desktop panel) who keeps products, stock, policies and settings correct and reads the measurement report.

Persona IDs PER-01..03 in `prd/03 - PRD Sections/PRD-01 - Goals.md`.

## Product Purpose

Reliable answers from the store's approved sources, safe handling of stale or conflicting stock data, and a clear queue for requests that need a human — so no request is lost. Current release: a 10-day interactive Prototype with synthetic data (PRD-11).

## Positioning

The assistant informs, asks and records; it never acts (no reservations, order changes, delivery promises, refunds). Stock is answered per variant with a validity window; anything uncertain is said as uncertain and routed to a human. Replaces both manual replies and unreliable chatbots (DEC-28).

## Operating Context

Small and medium Persian-language online shops, focus on Instagram shops (assumption A-01). Prototype: one demo store, a stand-alone chat page linked from a demo storefront, two desktop panels with separate entry points.

## Capabilities and Constraints

7 epics / 34 stories (PRD-04). Persian, text only, RTL. Jalali dates with Persian digits. Light theme only in v1. Product name undecided (Q-08). Full rules: `prd/`, constitution: `.specify/memory/constitution.md`.

## Brand Commitments

Font: Vazirmatn. Colour: Modern Teal (#0f766e). Interface name for the bot: «دستیار». No logo yet.

## Evidence on Hand

No real customers, data, testimonials or metrics exist yet (DEC-27). All demo content is synthetic and labelled as such.

## Product Principles

1. Only answer from approved sources; say "I don't know" plainly.
2. Uncertainty is never shown as certainty.
3. One owner at a time: assistant or a named human.
4. Answered is not resolved.
5. Everything measurable and auditable.

## Accessibility & Inclusion

WCAG AA contrast; status never by colour alone (NFR-03); 44px touch targets on the chat page; visible focus.
