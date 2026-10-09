# Tailvani Revamp Plan v2 — overlay on the Backend Master Plan
Tailvani · 2026-10-08 · Status: APPROVED by Suri 2026-10-09 00:19
This document sits ON TOP of the Backend Master Plan and Implementation Checklist. Where they conflict, this one wins. Everything not mentioned here (Shopify as master system, margin floor, fraud gate, approval gates, governance) still applies.

=====================================================================
## 1. What changed (Suri, 2026-10-08)
| Area | Before | Now |
|---|---|---|
| Sourcing | AliExpress via DSers + Mirage + Doggie Design + Printify | **Dropship only.** Shopify Collective (automation + assortment), Printify (Tailvani-branded), The Worthy Dog (US fashion, if it dropships), Doggie Design (only if approved). No AliExpress. |
| Catalog | 14 AliExpress products | All 14 in Draft (kept, not deleted). New catalog built from scratch. |
| Theme | Stock Dawn + small CSS polish | **Full Tailvani rebuild on Dawn** + a **seasonal skin layer** on top |
| Promotions | WELCOME (now 10%) + free shipping ≥ $35 | WELCOME 10% + promos tied to seasonal skins, margin-checked |
| Migration | Replace AliExpress SKU by SKU | Replaced by "build new catalog" — no migration |

=====================================================================
## 2. Design rule: everything is swappable
Suri will add and remove suppliers, skins and promos over time. So nothing is hard-coded:
- **Suppliers** live in a Supplier Registry (one Shopify entry each). Products link to a supplier by a tag `SRC-<CODE>`. Tags work on Collective products; per-product custom fields may not (Shopify lists metafields as incompatible with Collective).
- **Seasonal skins** are content entries, not code. Adding a holiday = adding an entry. No theme edit, no republish.
- **Promos** are normal Shopify discounts, scheduled with the same dates as their skin, aimed at an "eligible" collection that only holds products above the margin floor.

=====================================================================
## 3. Supplier layer (modular)
### 3.1 Supplier Registry — metaobject `tailvani_supplier` (admin-only)
Fields: code (COL, PFY, TWD, DD …), name, channel (COLLECTIVE / APP / EMAIL-ORDER), active (yes/no), processing days, transit days, return rule, defect-report window, contact, notes, onboarding gate (NOT STARTED → APPROVED → LIVE → PAUSED → REMOVED).

### 3.2 Add a supplier (runbook, ~1 hour + supplier approval time)
1. Create registry entry (gate NOT STARTED). 2. Confirm dropship terms in writing: fees, shipping, SLA, returns, blind packaging. 3. Gate 2 checks (Checklist §B), including one test order to Suri. 4. Import products → tag `SRC-<CODE>` → Draft. 5. Margin check → set discount tag. 6. Suri approves → Active.

### 3.3 Remove or pause a supplier (one action)
Set registry entry to PAUSED/REMOVED → bulk-set all `SRC-<CODE>` products to Draft (Claude can run this as one bulk update; later a Flow manual-trigger). Order history stays. Reverse = set back to Active.

### 3.4 Current lineup
| Code | Supplier | Channel | Status / blocker |
|---|---|---|---|
| COL | Shopify Collective | Collective app (free) | Needs Shopify Payments with active payouts, Network Intelligence on, possible ID check. US suppliers only (same country/currency). |
| PFY | Printify | Printify app (Free plan) | Open account; don't connect to Shopify until §5 controls exist. 24h approval delay. |
| TWD | The Worthy Dog | TBD | **Must confirm they dropship.** They sell wholesale on Faire (buy-and-hold), which is out under dropship-only. Also check whether they're on Collective. |
| DD | Doggie Design | Email order | On hold until approved. $3 dropship fee + Priority Mail; MAP = 2× wholesale. |

=====================================================================
## 4. Theme: Tailvani rebuild on Dawn
- Work happens on an **unpublished copy** of the live theme (Suri taps Duplicate once; Claude can write to unpublished themes, not the live one). Suri previews, then publishes.
- Brand from the existing build: Cormorant Garamond + DM Sans, warm palette (espresso, mocha, cream, sage, blush), "pet" not "dog", no fake reviews, Judge.me via app blocks.
- Product page structure from Plan §58, filled from the shipping/return rules (supplier-aware), with no hardcoded promises.
- The pre-deploy blockers from the audit (30-day returns, $50 free shipping, 5–8 days, 4.9★, invented reviews, "tested fabrics") are not carried over. Copy matches the live policies.

=====================================================================
## 5. Seasonal skin layer
### 5.1 How it works
One base theme. On every page load the theme picks the **active skin**:
1. If Suri has chosen a skin in **Theme settings → Seasonal skin override**, use it.
2. Otherwise use the skin whose start ≤ today ≤ end. If several match, the highest priority wins: brand/pet days 30 > holidays 20 > seasons 10.
3. If none match, show the base Tailvani look.
Caveat: Shopify caches pages, so an automatic switch can take effect a few hours late. Use the override for exact-minute launches (e.g., Black Friday midnight).

### 5.2 Skin entry — metaobject `tailvani_season_skin` (storefront-readable)
| Field | Type | Use |
|---|---|---|
| name, handle | text | "Halloween 2026" |
| start_date, end_date | date | Auto window |
| priority | integer | 10 / 20 / 30 |
| enabled | boolean | Kill switch per skin |
| accent, background, text, button colors | color | Overrides Dawn color variables |
| hero_image_desktop / hero_image_mobile | file | Homepage hero |
| hero_heading, hero_subtext, hero_button_label | text | Hero copy |
| hero_collection | collection reference | Button target + featured grid |
| announcement_text | text | Announcement bar |
| overlay_asset | file (SVG/PNG) | Decoration layer (falling leaves, snow, hearts…) |
| overlay_density, overlay_motion | integer / boolean | How much, and whether it moves; always off with "reduce motion" and lighter on phones |
| badge_text | text | Small product-card badge on hero-collection items ("Holiday pick") |
| promo_code, promo_label | text | Shown only while the skin is active; must match a scheduled Shopify discount (§6) |

### 5.3 Theme code (to be built on the unpublished copy)
- `snippets/tv-skin-resolver.liquid`: picks the active skin, writes CSS variables onto `:root`.
- `snippets/tv-skin-overlay.liquid`: decorative layer (pointer-events off, reduced-motion aware, capped size for speed).
- `sections/tv-seasonal-hero.liquid`, plus announcement-bar and card-badge hooks reading the active skin.
- Theme setting: "Seasonal skin override" (metaobject picker) + "Disable all skins" toggle.
- Verified against shopify.dev (2026-10-09): Liquid loops a definition's entries with `metaobjects.tailvani_season_skin.values` (the older `shop.metaobjects` form is deprecated). Themes support a `metaobject` setting type for the override picker. Compare dates as Unix timestamps (`| date: '%s' | times: 1`), not as strings. Still to be tested on the copy before publish.

### 5.4 Skin calendar 2026–27 (all four groups Suri chose)
Seasons (priority 10): Fall Sep 22–Dec 20 · Winter Dec 21–Mar 19 · Spring Mar 20–Jun 20 · Summer Jun 21–Sep 21
Retail holidays (priority 20):
| Skin | Window | Notes |
|---|---|---|
| Halloween | Oct 10–Oct 31, 2026 | First skin to ship (it's Oct 8) |
| Black Friday / Cyber Monday | Nov 26–Nov 30, 2026 | Thanksgiving Nov 26; BF Nov 27; CM Nov 30 |
| Holidays / Christmas | Dec 1–Dec 26, 2026 | Shipping-cutoff banner needed (7–12 day delivery → cutoff ~Dec 10, confirm per supplier) |
| Valentine's | Feb 1–Feb 14, 2027 | |
| Other US: Thanksgiving | Nov 16–Nov 25, 2026 | Hands off to BFCM |
| Other US: New Year | Dec 27, 2026–Jan 3, 2027 | |
| Other US: St. Patrick's | Mar 10–Mar 17, 2027 | |
| Other US: Easter | Mar 21–Mar 28, 2027 | Easter Mar 28 |
| Other US: 4th of July | Jun 27–Jul 5, 2027 | |
Pet & brand days (priority 30): National Dog Day Aug 26 (Aug 22–26) · National Cat Day Oct 29 (Oct 27–29, overrides Halloween for 3 days) · Tailvani anniversary Mar 17 (Mar 15–17, 2027; same day as St. Patrick's — the brand skin wins on Mar 17, St. Patrick's runs Mar 10–14).

=====================================================================
## 6. Promotions (margin-checked, linked to skins)
- Every product carries a discount tag: `disc:all` (survives 20% off), `disc:max10` (survives 10%), `disc:none`. Set at import by the margin check (30% and $5 floor, Phase 1 D11).
- Two automated collections: **Promo – up to 20%** (tag disc:all) and **Promo – up to 10%** (tag disc:all OR disc:max10).
- A skin's promo = a Shopify discount code scheduled with the skin's dates and pointed at the matching collection. Promo depth is capped by that collection.
- WELCOME stays 10%, first order. Rule: one code per order (Shopify combination settings off), so WELCOME doesn't stack with skin promos.
- Free shipping ≥ $35: re-check once real dropship shipping costs are known. Collective/Printify charge shipping per supplier, so a mixed cart pays more than one shipment (Plan §18).
- MAP-protected products (Doggie Design) never get promo tags.

=====================================================================
## 7. Revised phases
| Phase | What | Who | Blocked by |
|---|---|---|---|
| R0 | AliExpress removed, products Drafted, DSers gone, WELCOME 10%, duplicate free-shipping discount deleted | Done | — |
| R1 | Owner prerequisites: password page on; Shopify Payments payouts active; Network Intelligence on; install Flow, Search & Discovery, Shopify Collective; duplicate theme | Suri (~20 min) | — |
| R2 | Registries: supplier + skin metaobject definitions; discount tags + promo collections | Claude | R1 approval |
| R3 | Theme rebuild on the copy: brand, product page, skin resolver/overlay/hero, Halloween + Fall skins | Claude builds, Suri previews and publishes | R1 (theme copy) |
| R4 | Suppliers: Collective first (instant), then Printify, The Worthy Dog (if dropship), DD (if approved) | Suri accounts; Claude curates and margin-checks | R1 |
| R5 | Catalog: 15–30 launch products, margin-checked, tagged, drafted, then Suri approves | Both | R4 |
| R6 | Launch: password off; Halloween/Fall skin live; Flow alerts (fraud, tracking-late, margin) | Both | R3 + R5 |
| R7 | BFCM + Holiday skins and promos scheduled by Nov 20 | Claude | R6 |
Timing: BFCM is 7 weeks away. R1–R6 by about Nov 1 makes BFCM realistic; Halloween (Oct 31) is tight, so expect Fall to be the launch skin.

=====================================================================
## 8. Changes to earlier approvals
- D3 supplier codes → COL, PFY, TWD, DD (MIR and ALI retired).
- D5 product fields → Collective products use tags + collections. Admin-only metafields are used only where they work for that supplier.
- D9/D10 stock buffers → apply to suppliers whose stock syncs automatically (Collective syncs in real time; Printify is made-to-order, no buffer).
- D17 Mirage test → void. D18 DD → on hold. D19 Printify → unchanged.
- F3/F11/F12 theme items → folded into R3.

## 9. Needed from Suri
1. Approve this plan (or mark changes).
2. ~~Anniversary date~~ — received: March 17.
3. Do the R1 owner steps (list in chat).
