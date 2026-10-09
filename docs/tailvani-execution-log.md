# Tailvani Execution Log (checkpoint file)

Source docs: Tailvani_Backend_Master_Plan_2026-10-08.txt, Tailvani_Implementation_Master_Checklist_v1.0.txt
Started: 2026-10-08 21:51 ET
Mandate from Suri: work all phases at Claude's discretion; keep checkpoints; audit and iterate; don't stop and wait.

## Standing rules for whoever resumes this
- NO live Shopify changes, purchases, supplier applications, app removals, or tax/resale submissions without Suri's explicit approval (checklist §BA + Level 3/4). Shopify is used READ-ONLY until approvals land.
- Each phase writes its output to claude/ in this project, then updates this log.

## Status
| Phase | Status | Output file |
|---|---|---|
| 0 Audit | v2 DONE from live Shopify data; owner-only checks remain (notifications, DNS, payments, MFA, DSers shipping costs) | claude/phase0-audit-register.md |
| 1 Design foundation | READY FOR APPROVAL (revised 3x: Printify 24h, DD MAP, floor $5, WELCOME options) | claude/phase1-design-foundation.md |
| 2 Supplier research | DONE (Mirage terms → VERIFY list) | claude/phase2-supplier-research.md |
| 3 Build specs | DONE — READY FOR APPROVAL (fix list F1–F12, metaobjects, metafields, 8 Flow workflows, KB, emails, run order) | claude/phase3-build-specs.md |
| Control Center | DONE — Dashboard artifact https://claude.ai/artifact/W5MBhiQcnqKQAkw4LXnuBR (live Shopify funnel, sales, catalog margin calc + registries as JSON files) | artifact |
| 4+ Pilot/migration | BLOCKED on approvals | - |

## Top findings (live data, 2026-10-08)
1. 13 checkouts started, 0 completed in last 90 days (290 sessions). Lifetime orders: 2.
2. WELCOME 20% (all items) puts all 14 products under the 30% margin floor; 2 products under floor even at full price (Rainwell coat, Summer Pup Shirt). Recommend WELCOME10.
3. Judge.me widget on product template set to review_data "sample_data" — verify live; possible fake reviews showing.
4. Product pages have no shipping/returns/care info (tabs disabled).
5. Apps to review: Shopify ChatGPT MCP App (broad write), Make (write_products), Melio Bill Pay (money movement).
6. Flow and Search & Discovery not installed.
7. Custom tailvani-* theme package in project is NOT live; it contradicts live policies (30-day returns, $50, 5–8 days, 4.9★, fake reviews) — must be fixed before any deploy.
8. Hoodie at 9,999 stock on all variants; SKUs are AliExpress property codes.
9. Doggie Design dropship at MAP is thin; Printify approval delay 24h.

## Shopify read queries used (validated): products+variants+costs, discountNodes, deliveryProfiles, shop.shopPolicies, appInstallations (no billing scope), orders (no PII), themes(MAIN) files + bodies, ShopifyQL sessions funnel.

## Checkpoint history
- 21:51 — Log created.
- Phase 0 v1 (theme files) saved.
- Environment changed; Shopify reconnected.
- Phase 1 saved → Phase 2 saved → Phase 1 revised.
- Phase 0 v2 (live data) saved; Phase 1 D11/D13 revised from live numbers.
- Phase 3 saved. Found existing shopify.* category metafields → reused instead of new ones. FL-07 margin rule corrected & verified variant-by-variant.
- Control Center built (Dashboard type; no Sheets type available, no Google Sheets connector). To update registries: re-upload JSON asset and update datasets/<id> url+updated.
- Verification pass: stale "$6 floor" labels fixed in Phase 1 & 2 (values unchanged — 30% was binding).

## APPROVALS FROM SURI (2026-10-08, via question prompts)
- F1 Judge.me real reviews: APPROVED
- F2 WELCOME → 10% once per customer + announcement bar: APPROVED
- F3 Shipping & Returns tab with policy text: APPROVED
- F4 delete duplicate automatic FREE SHIPPING discount: APPROVED
- F5 Waterproof → Water-Resistant (2 titles): APPROVED
- F6 Dog/Pup → Pet in 5 titles: APPROVED
- F7 Rainwell $21.99, Summer Pup Shirt $18.99: APPROVED
- F8 cap Cozy Collar Puppy Hoodie at 50/variant: APPROVED
- F9 apps: Suri USES ChatGPT connector, Make, Melio → KEEP all three (record owner purpose in App Registry later)
- F10 install Flow + Search & Discovery: APPROVED (Suri taps Install)
- F11 header country/language selectors off: APPROVED
- F12 social links: LATER — accounts are empty; Suri wants a socials/marketing manager. NOTE: plan covers Meta/Google catalog channels but no social-content manager tool → raise as a new item.
- D1 Shopify master: APPROVED · D2 SKU format: APPROVED · D3 supplier codes: APPROVED · D4 lifecycle: APPROVED
- D5 fields: APPROVED · D6 size charts: APPROVED · D7 shipping classes: APPROVED · D8 return classes (keep live 14-day policy; Fit-Exchange waits): APPROVED
- D9 buffer as asked (0–3 don't sell for ALL suppliers, 4–10 −2, 11–50 −3, >50 cap 50; POD unlimited): APPROVED · D10 stale feed: APPROVED · D11 floor 30% & $5: APPROVED · D12 MAP: APPROVED
- D13 discount classes: APPROVED · D14 fraud gate: APPROVED · D15 return thresholds: APPROVED · D16 tags: APPROVED
- D17 Mirage (email first, samples ≤$120): APPROVED · D18 Doggie Design (≤$150): APPROVED · D19 Printify Free (≤$60): APPROVED · D20 Control Center = dashboard: APPROVED
=> ALL 20 decisions approved; fixes F1–F8, F10, F11 approved; F9 keep all apps; F12 later.
Spending (samples) and account/tax submissions are still done BY SURI; Claude drafts emails.

## EXECUTION (live changes) — backup: claude/backups/products-2026-10-08-before-changes.json
- F1: NO CHANGE NEEDED — Judge.me docs say sample reviews show only in the theme editor, not the live store. Suri to eyeball a live product page.
- Theme writes to the live (MAIN) theme are blocked for Claude's connector → F3 (Shipping tab), F11 (header pickers) and the F2 announcement text must be done by Suri in Theme editor (steps given in chat).
- DONE F5+F6+F7: Rainwell → "Rainwell Water-Resistant Pet Coat", 16 variants $21.99 · Summer Pup Shirt → "Tailvani Summer Pet Shirt", 12 variants $18.99 · Cloudbreak → "Cloudbreak Water-Resistant Pet Raincoat" · Cable Knit → "Tailvani Cable Knit Pet Sweater" · Cozy Cotton → "Cozy Cotton Pet Hoodie". Handles unchanged.
- F8 PARTIAL (stopped by Suri): Cozy Collar Puppy Hoodie set to 50 on 6 of 9 variants (Baby Blue L/M/S, Lemon L/M/S). Chocolate L/M/S still 9,999. Location = dsers-fulfillment-service.
- 22:32 SURI DECISION: "we are removing AliExpress and DSers". All product updates PAUSED. This overrides Plan §15/§68 "SKU by SKU" migration. All 14 current products are AliExpress/DSers-sourced. Clarifying questions pending: timing, what happens to the 14 products, replacement supply.
- 22:35 SURI ANSWERS: set all 14 products to DRAFT (not delete), NOW (store empty until new suppliers ready), skip remaining approved product/theme work on them, DSers app ALREADY UNINSTALLED by Suri.
- DONE 22:36: all 13 ACTIVE products set to DRAFT (13/13 succeeded). Monogram was already Draft. Storefront now has 0 sellable products. Reverse: set status ACTIVE.
- VERIFIED: DSers app gone; DSers fulfillment location gone (only Suri's own location remains). Drafted products' inventory lived at the DSers location → if ever reactivated they will show sold out until restocked/re-sourced.
- DONE F2: WELCOME code now 10% (all items, once per customer). Announcement bar still says 20% → Suri edits in Theme editor.
- DONE F4: automatic "FREE SHIPPING" discount deleted. Free shipping still applies via the $0 Standard rate on orders ≥ $35.
- PLAN CHANGE: Phases 4–5 (SKU-by-SKU AliExpress migration) replaced by building a new catalog from Mirage / Doggie Design / Printify. Control Center updated.
- OPEN: store is live with 0 products → recommend password page ("coming soon") until new catalog; Suri to decide.

## 23:13 — SURI: FULL REVAMP REQUESTED (plan being redefined)
- Wants: new discounts, new products, new suppliers, new theme(s), plus a customizable theme layer/overlay for seasonal & holiday themes, on top of everything in the plan.
- Gap noted: plan has seasonal collections only (§25), no visual seasonal theme layer → new workstream needed (proposed: base theme + "season skin" metaobjects with colors/banners/decor/announcement/collection/discount + date-based auto switch).
- 23:14 SURI: not all planned suppliers usable (Mirage confirmed out). Asked Claude to hold everything.
- 23:29 SURI — NEW SUPPLIER LINEUP (replaces Plan §15 / Phase 2):
  · Shopify Collective = automation and assortment
  · Printify = Tailvani-branded merchandise
  · The Worthy Dog = direct U.S. fashion supplier
  · Doggie Design = add only if approved
  · No AliExpress dependency. Mirage dropped (D17 void).
- Theme questions (base theme, switching, seasons, discount link) still unanswered.
- 23:35 Research saved: claude/phase2b-supplier-lineup-v2.md. Key: Collective needs Shopify Payments w/ active payouts + Network Intelligence + possible ID check; Shopify lists METAFIELDS as incompatible with Collective (risk to D5 design). Worthy Dog sells wholesale on Faire; dropship unknown.
- 23:48 SURI: DROPSHIP ONLY for every supplier (no held inventory). Suppliers may be added/removed over time → implementation must be modular ("clean"): adding/removing a supplier must not require rework. The Worthy Dog stays only if it offers dropship (VERIFY). Doggie Design question unanswered (on hold).
- 23:55 SURI THEME ANSWERS: base = rebuild on Dawn · skins switch auto by date + manual override · skins for 4 seasons + major retail holidays + pet & brand days + other US holidays · each skin can link a promo, margin-checked (only products above 30% floor).
- 00:05 (Oct 9) Revamp Plan v2 saved: claude/revamp-plan-v2.md — overlays the Master Plan. Covers modular supplier registry, Dawn rebuild on an unpublished copy, seasonal skin layer (metaobject tailvani_season_skin, auto by date + override, priorities), 2026–27 skin calendar, margin-checked promo collections, revised phases R0–R7. AWAITING SURI APPROVAL + anniversary date + R1 owner steps.
- 00:19 SURI: REVAMP PLAN v2 APPROVED. Anniversary = March 17 (same day as St. Patrick's → brand skin priority 30 wins that day). Theme was set up via GitHub (repo tailvani-theme; live theme "dawn-tailvani/main").
- R1 verified from Suri's screenshots: password page ON (no visitor message yet) · Shopify Payments verified US bank, daily payouts, last payout Jun 8 2026 · CVV fraud check on, test mode off · Network Intelligence ENABLED · installed: Search & Discovery, Flow, Collective, Printify, Fulfillment Network (not in plan — ask), Claude connector, Judge.me, Messaging, Make, ChatGPT MCP. Melio Bill Pay not in list (removed?). Theme duplicate: pending — use a GitHub branch instead (needs repo owner/link).
- R2 DONE 00:25: metaobject definitions created — tailvani_supplier (gid MetaobjectDefinition/26681082135, admin-only) and tailvani_season_skin (gid MetaobjectDefinition/26681114903, storefront PUBLIC_READ, 23 fields). Next: supplier entries, then skin entries with the theme build.
- R2 supplier entries created: col (APPROVED), pfy (NOT STARTED), twd (NOT STARTED, dropship unconfirmed), dd (NOT STARTED, on hold).
- NEXT: theme build via a GitHub branch of tailvani-theme connected as an unpublished theme.
- 00:23 Repo = https://github.com/Samster0069/tailvani-theme. add_repo failed: Suri's GitHub account isn't linked to Claude. Options sent: (A) link GitHub in claude.ai settings → Claude works on a branch; (B) Suri taps Duplicate on the theme in Shopify → Claude edits the unpublished copy via the Shopify connector (works now; copy not GitHub-synced until reconnected).
- 00:27 Suri linked GitHub. Findings: TWO repos. `Samster0069/tailvani-theme` = the old custom (non-Dawn) package, NOT live. `Samster0069/dawn-tailvani` (PUBLIC repo) = the LIVE theme ("dawn-tailvani/main"). Both cloned read-only. PUSH IS REFUSED: the Claude GitHub App isn't installed on Suri's account → install at https://github.com/apps/claude/installations/select_target (select dawn-tailvani, tailvani-theme). Build base = dawn-tailvani on a new branch `revamp-seasonal`.
- 00:30 Suri installed the Claude GitHub App. PUSH WORKS. Branch `revamp-seasonal` pushed to Samster0069/dawn-tailvani with snippets/tv-skin-handle.liquid + snippets/tv-skin-styles.liquid. GitHub is now the checkpoint for theme work (commit often).
- 00:30 Suri provided plugin craft-studio (VectorCraft etc.). Not installed on account; used locally via /home/claude/craft/mcpc.py stdio client (plugin extracted to /home/claude/plugin-src/craft-studio). Works.
- THEME BRANCH `revamp-seasonal` (Samster0069/dawn-tailvani) commits: d5ff38d resolver+styles snippets · d9441bf layout wiring, settings group "Tailvani seasonal skins" (disable / override / badges), announcement override, product-card skin badge, sections/tv-seasonal-hero.liquid (replaces old hero_banner on homepage; falls back to wide_banner.png) · 99383fc 12 overlay icons (assets/tv-overlay-*.svg, made in VectorCraft).
- Skin definition updated: + field overlay_theme_asset (choices leaf, bat, pumpkin, snowflake, heart, clover, paw, star, petal, sun, confetti, egg).
- 16 SKIN ENTRIES CREATED (all enabled): fall-2026, halloween-2026, national-cat-day-2026, thanksgiving-2026, bfcm-2026, holidays-2026, winter-2026, new-year-2027, valentines-2027, st-patricks-2027, tailvani-anniversary-2027, spring-2027, easter-2027, fourth-of-july-2027, summer-2027, national-dog-day-2027. Colors/copy/icons set; hero images, collections and promo codes empty (pending catalog). Live theme does NOT read them → no live impact. Data: claude/skins-2026-27.json.
- NEXT: Suri connects branch revamp-seasonal as an unpublished theme (Themes → Add theme → Connect from GitHub). Then preview + fix, brand fonts/colors, product page.
- Design principle adopted: supplier-agnostic layer — supplier registry entry + universal SRC-<code> tag (tags work for Collective products, metafields may not) + per-supplier rules looked up from the registry; removing a supplier = deactivate registry entry → its products auto-drafted.
- Follow-up found: descriptions of Rainwell & Cloudbreak still say "Waterproof"; Summer Pet Shirt has a customer-visible "China Mainland" option (ships-from). Not changed — need Suri's OK.

## NEXT (for Suri or a resumed session)
1. Suri: approve/edit fix list F1–F12 (Phase 3 §A) and decisions D1–D20 (Phase 1 approval sheet).
2. Suri owner checks: notifications, DNS/Namecheap, payments, MFA, real DSers shipping cost per product, check live product page for sample reviews.
3. After approval: execute Phase 3 §J run order (backup export first).
4. Supplier emails: Doggie Design 4 questions, Mirage full terms (Phase 2).

## R-REBUILD (Oct 9, from 01:06) — Suri: "whole rebuild on Dawn + existing assets; colours don't captivate; logo good, visuals not; new pictures (use the plugin); holidays must change banners and other elements, not just an overlay; full access"
- Design direction saved: claude/rebuild-design-direction.md ("boutique window": logo arch frames everything; milk/olive/blush/sage/marigold; Young Serif + Figtree).
- Photos: 93 Pexels/Unsplash photos (free commercial licences) sourced into /home/claude/craft/photos2 with CREDITS per theme.
- Plugin use: VectorCraft drew 34 seasonal props (render_props.py, props_lib.py); LightCraft graded every hero and feature photo (grade.py); compose_hero.py builds the arch "window" art.
- MEDIA BRANCH `media` (orphan) on Samster0069/dawn-tailvani, commit f1a9320: upload/ (42 files), scripts/, credits/. DO NOT connect it to Shopify.
- SHOPIFY FILES: 42 images uploaded via fileCreate from raw GitHub URLs, all READY. ID map at /home/claude/craft/file_ids.json. Includes:
  - tailvani-logo.png / -light.png (1437×282, extracted from wide_banner)
  - tv-hero-<skin>.webp (17, incl. base)
  - tv-feature-<skin>.jpg (17)
  - tv-tile-{dogs,cats,accessories,toys,beds,grooming}.jpg
- Skin definition: + color_band, color_dark, feature_image, feature_heading, feature_text. Labels renamed (color_background = "Hero band color").
- ALL 16 SKINS UPDATED: new captivating palettes (no more beige), hero images (desktop + mobile), feature image + copy, and announcements without middle dots.
- NEXT: theme rebuild on revamp-seasonal: fonts, schemes, header/footer, homepage sections, skin layer for every band, garland divider.
- BACKEND (Oct 9 ~02:00):
  - 20 smart collections created and published to Online Store. Tag taxonomy:
    - pet:dog, pet:cat
    - type:apparel / type:accessories / type:toys / type:beds / type:grooming
    - season:fall / winter / spring / summer
    - occasion:halloween / holidays / valentines / st-patricks / easter / july4
    - disc:all and disc:max10 → "Promo – up to 20%" / "Promo – up to 10%"
    - New arrivals = every product, newest first.
  - Old manual collections renamed apparel-old-catalog / accessories-old-catalog (handles freed).
  - Skin → collection links:
    - fall and thanksgiving → fall
    - halloween → halloween
    - cat day → cats; dog day → dogs
    - bfcm and holidays → holiday-gifts
    - winter, spring, summer → the matching season
    - new year and anniversary → new-arrivals
    - valentines, st-patricks, easter, july4 → matching collection
- PAGES: /pages/about (template page.about) and /pages/faq (template page.faq, accordion answers taken from live policies).
- MENUS (note: the live theme uses these too; store is password-protected, so no customer impact):
  - main-menu = New arrivals, Dogs, Cats, Clothing, Accessories (Toys, Beds, Grooming), Help
  - new footer-shop
  - footer = FAQ, Contact, policies, Search
- FILES: + tailvani-mark.png (favicon).
- THEME BRANCH revamp-seasonal commits:
  - 6e2bf13: rebuild
  - a024a1e: url-default fix (Shopify rejects url defaults other than /collections)
  - f6de4a3: FAQ/About templates + favicon
  - f59d7c4: rotating announcement
  - e88c19e: QA fixes
- Suri had already connected the branch as unpublished theme "dawn-tailvani/revamp-seasonal" (OnlineStoreTheme/193429897495). Sync confirmed. index.json initially failed sync because of the feature-band schema error and was pushed via themeFilesUpsert; Shopify committed it back (b66d773).
- Theme check: 0 errors (warnings only: Dawn stock scheme_classes, font preloads).
- Fonts are self-hosted (assets/tv-*.woff2, OFL).
- VISUAL QA:
  - Static mock of the homepage (qa/mock.py) rendered in Playwright for 8 skins on desktop and mobile. Overview at /home/claude/qa/overview-desk.jpg.
  - Fixes applied: trust strip goes single-column on phones, garland 28px.
  - WCAG contrast: all 17 palettes pass AA (lowest 5.9:1, thanksgiving); sale badge 5.4:1.
- Judge.me product block has review_data "sample_data". Judge.me docs say samples show only in the theme editor, never live. OK.
- PENDING (Suri):
  - Storefront password, so Claude can screenshot the real preview.
  - Review the preview theme, then publish when happy (Claude never publishes).
- 02:58 SURI: "doesn't need to be too fancy but should target the right audiences: pet owners, especially cats and small dogs; other pets accommodated but not hard-targeted."
  - Photos retargeted. 13 new Unsplash photos (july4b, dogdayb, easterb) with credits on the media branch.
  - Heroes swapped:
    - thanksgiving → dachshund in blanket
    - holidays → spitz
    - new year → cat with champagne
    - valentines → tortie cat
    - spring → yorkie
    - july4 → frenchie (stripe wall)
    - summer → yorkie in sunglasses
    - dog day → Shih Tzu mix
  - Features swapped to cats/small dogs:
    - fall: ginger cat; thanksgiving: grey cat; holidays: black cat
    - new year: frenchie; spring: kitten; easter: Shih Tzu
    - july4: Persian cat; summer: ginger cat; dog day: chihuahua
    - valentines: doodle (the one "other" pet)
  - Same filenames and file IDs replaced in Shopify Files (fileCreate REPLACE from media commit 6ede578); alts updated.
  - Copy now leads with "cats and small dogs, with picks for every pet":
    - hero default, feature band, footer, password page, About page
    - Dogs/Cats collection descriptions; winter feature text
  - Tiles reordered: For cats, For small dogs, Walk and play.
  - Menus: Cats before Dogs. New "Other pets" collection (tag pet:other) appears only under Accessories and in the footer, not top level.
  - Theme commit 1262740.
- 03:23 Repo completeness check on Suri's request:
  - Theme branch revamp-seasonal @1262740: everything pushed, working tree clean.
  - Media branch @64e7fb1 adds records/ (Shopify admin setup: skin and collection GraphQL, file IDs, menus, pages, tag taxonomy), qa/ (mock + screenshot scripts) and docs/ (log, design direction, revamp plan, banner sheets).
  - Collection images for new-arrivals, fall, spring, summer, holiday-gifts, valentines, easter, fourth-of-july and other-pets updated to the cat/small-dog photos.
  - Not in the repo, by design: the ~170 raw stock photos (originals are on Pexels/Unsplash/Openverse; credits are in the repo).
