# Tailvani rebuild: design direction (R-phase, 2026-10-09)

Brief (Suri, Oct 9): whole rebuild on Dawn with existing assets. Keep the logo. The current colours don't captivate; the visuals should be neither bland nor harsh. New photography is needed. Holiday themes must change the banner pictures and other parts of the site, not only an overlay.

## Concept: "The boutique window"
The logo's arch is the shop window, and every season dresses that window.
- **Arches everywhere:**
  - Hero photos sit in an arch.
  - Shop-by-pet tiles are arches.
  - Product cards get a soft domed top.
- **Seasonal props** (leaves, pumpkins, baubles, hearts, clovers, balloons…) are drawn flat in VectorCraft. They spill over the arch edge like window dressing.
- **Seasons recolour every band** on the page, not just the hero.

## Base palette (no skin active)
| Role | Name | Hex | Use |
|---|---|---|---|
| Page | Milk | #FFFDF8 | page ground (near-white, not cream) |
| Ink | Olive ink | #2B3524 | text, primary buttons, announcement/newsletter/footer band (from the wordmark) |
| Hero band | Blush | #F7D9CF | hero + feature panels |
| Band | Sage | #DCE5CF | editorial band, trust strip |
| Accent | Marigold | #F2AE3D | decorative only: props, underlines, dividers, focus ring |
| Sale | Terracotta | #C4673F | sale price + heart only |

The old visuals were beige plus terracotta blobs; the new ones are colour-blocked bands. Terracotta is demoted to sale and heart only.

## Type
- **Headings:** Young Serif (Google Fonts, 400). It is a friendly, sturdy serif with ball terminals and sits close to the wordmark's weight.
- **Body:** Figtree 400/500/600. It is a friendly geometric sans, clearly distinct from the serif.
- **Rules:**
  - Sentence case everywhere.
  - No all-caps eyebrows.
  - No single-word accent colouring in headlines.

## Layout (homepage)
```
[announcement — ink band, skin text]
[header — milk: logo left · menu · icons]
[HERO — hero band colour]
  ┌ text 5/12 ───────────┐ ┌ arch art 7/12 (photo in arch + seasonal props) ┐
  heading (Young Serif, large)
  one-line sub
  [Primary CTA]  secondary link
[seasonal garland divider: row of the skin's icon]
[Shop by pet — milk: 3 arches Dogs / Cats / Accessories]
[Featured collection — skin hero_collection or New arrivals; domed product cards]
[Editorial band — band colour: feature photo left, short story right]
[Trust strip — 4 policy-true facts]
[Newsletter — ink band: "10% off your first order" (WELCOME)]
[Footer — ink]
```
On mobile, the arch art stacks above the text and the content is left-aligned.

## How a skin changes the site
1. Hero art: a per-skin composite (photo + props) via `hero_image_desktop` / `hero_image_mobile`.
2. Hero band colour (`color_background`) → color scheme "Hero".
3. Band colour (`color_band`, new) → editorial band + trust strip.
4. Ink colour (`color_dark`, new) → announcement, newsletter, footer.
5. Feature photo (`feature_image`, new) → editorial band image. Also new: `feature_heading` and `feature_text`.
6. Accent → props, underlines, garland divider and focus ring.
7. Garland divider: the skin icon repeated in a row between sections.
8. Also: announcement text, product badges, featured collection, overlay.

## Trust facts (from live policies)
- Free US shipping on orders over $35.
- Returns within 14 days of delivery on unused items.
- Orders processed in 1–3 business days; delivery 7–12 business days.
- Questions answered within 1–2 business days at tailvaniandco@gmail.com.

## Self-review against generic defaults
- **Cream + serif + terracotta:** the risk was the old brand banners themselves.
  - Ground changed to near-white milk.
  - Colour comes from blocked bands (blush, sage, olive) plus marigold.
  - Terracotta is limited to sale.
- **Fraunces + DM Sans:** first draft. Swapped to Young Serif + Figtree; Fraunces is an overused default, and Young Serif matches the sturdier wordmark.
- **Card kit / gradient washes:** none. Hierarchy comes from the arch shape language (hero arch large, tiles medium, product dome subtle) rather than one radius everywhere.
- **Eyebrow labels / ALL CAPS / → arrows / middle-dot meta:** avoided in new copy. The announcement middle dots will be replaced with a plain separator.
- **Spent boldness:** the hero window art. Everything else stays quiet.

## Imagery
- Sources: Pexels and Unsplash (free commercial licences) via photos2/, plus Openverse CC0 via photos/. Credits are kept per folder.
- No watermarks and no visible brand text.
- Hero picks (one per skin):

| Skin | Photo |
|---|---|
| base | base-1 pomeranian, blue bandana |
| fall | fall-1 cavalier in leaves |
| halloween | halloween-1 cat costume + pumpkins |
| catday | catday-3 cream cat, burgundy |
| thanksgiving | thanksgiving-1 weimaraner harvest |
| bfcm | bfcm-1 terrier, gifts, terracotta wall |
| holidays | holidays-1 santa hat |
| winter | winter-1 boston terrier sweater |
| newyear | newyear-1 weimaraner confetti |
| valentines | valentines-1 heart floral arch |
| stpatricks | stpatricks-1 |
| anniversary | anniversary-1 frenchie party hat |
| spring | spring-1 terrier blossom |
| easter | easter-3 cat bunny ears |
| july4 | july4-1 lab RWB bandana |
| summer | summer-1 Hawaiian shirt |
| dogday | dogday-1 golden retriever |

- Feature photos use each theme's #2 pick.

## Skin palettes (as set in Shopify, Oct 9)
| Skin | Hero band | Band | Ink | Text | Accent | Button | Photo | Feature |
|---|---|---|---|---|---|---|---|---|
| base | #F7D9CF | #DCE5CF | #2B3524 | #2B3524 | #F2AE3D | #2B3524 | base/base-1 | base/base-2 |
| fall-2026 | #F7CBA6 | #F3E3BC | #4A2A1C | #3A2418 | #E8833A | #4A2A1C | fall/fall-1 | fall/fall-2 |
| halloween-2026 | #F7B46A | #E6DCF0 | #2A1F33 | #2A1F33 | #F28C28 | #2A1F33 | halloween/halloween-1 | halloween/halloween-3 |
| national-cat-day-2026 | #F1D4DF | #F6E7C8 | #4B2238 | #3A1C2C | #E98AA8 | #4B2238 | catday/catday-3 | catday/catday-2 |
| thanksgiving-2026 | #EBC9A0 | #DDE3C8 | #3D2B1F | #3D2B1F | #D98A2B | #6B3A22 | thanksgiving/thanksgiving-1 | thanksgiving/thanksgiving-4 |
| bfcm-2026 | #F4C7B1 | #F9E7C9 | #1F3A34 | #2A2420 | #F2AE3D | #1F3A34 | bfcm/bfcm-1 | bfcm/bfcm-3 |
| holidays-2026 | #F4D3CB | #D6E6DA | #1E4636 | #1E2E26 | #E9B44C | #1E4636 | holidays/holidays-1 | holidays/holidays-2 |
| winter-2026 | #D7E6F2 | #EEF0F4 | #1F3247 | #1F3247 | #8DB4D6 | #1F3247 | winter/winter-1 | winter/winter-2 |
| new-year-2027 | #F1E3C2 | #E3E6F2 | #1E2547 | #1E2547 | #D4A637 | #1E2547 | newyear/newyear-1 | newyear/newyear-2 |
| valentines-2027 | #F8C9D0 | #FBE6E4 | #6B1F33 | #4A1A27 | #F08FA0 | #6B1F33 | valentines/valentines-1 | valentines/valentines-2 |
| st-patricks-2027 | #F6F0D2 | #D3EBC8 | #1F4A2C | #1F3A24 | #E9B44C | #1F4A2C | stpatricks/stpatricks-1 | stpatricks/stpatricks-3 |
| tailvani-anniversary-2027 | #F9D4E2 | #FCEBC4 | #2B3524 | #2B3524 | #F2AE3D | #2B3524 | anniversary/anniversary-1 | anniversary/anniversary-3 |
| spring-2027 | #F9D3DC | #E2EED6 | #2F4A2E | #2F3A2A | #F6C744 | #2F4A2E | spring/spring-1 | spring/spring-2 |
| easter-2027 | #E3DDF4 | #FBF0C9 | #3E3A63 | #2F2B4A | #A9D8C8 | #3E3A63 | easter/easter-3 | easter/easter-1 |
| fourth-of-july-2027 | #DCE6F4 | #F6E3DE | #1C2B4D | #1C2B4D | #C8343B | #1C2B4D | july4/july4-1 | july4/july4-2 |
| summer-2027 | #FFE0A3 | #CFEAF0 | #0F4C5C | #183A42 | #F07B4A | #0F4C5C | summer/summer-1 | summer/summer-2 |
| national-dog-day-2027 | #FBD7A8 | #DDE5CF | #2B3524 | #2B3524 | #E07A3F | #2B3524 | dogday/dogday-1 | dogday/dogday-2 |

All palettes pass WCAG AA for text on every band (lowest is thanksgiving at 5.9:1).
