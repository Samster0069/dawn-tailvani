# Tailvani storefront checkpoint CP22

The existing seasonal theme is the storefront foundation. This change integrates reviewed product information and populated collection browsing into default home, collection, search and product templates. It preserves seasonal artwork, cats-first ordering, Dawn product/variant/cart controls, native search/filter/sort and the existing reviews app block.

Empty/missing collection destinations are hidden in the hero and shop tiles. The seasonal feature band keeps its normal story destination when a seasonal collection is empty. Published sold-out items remain discoverable. The shop tile grid handles one remaining tile and keyboard focus visibly.

**Owner decision (2026-10-09, 16:30):** keep the detailed selling-point copy from the seasonal build: "Free US shipping on orders over $35", "14-day returns", processing/delivery times, reply time, and the detailed FAQ and product tabs. Do not replace them with generic links. Each claim keeps its link to the shipping or refund policy page, and the theme copy must match those policies. Hiding empty collections is kept. Before launch, a free-shipping rate for US orders of $35+ must exist in Shopify shipping settings (none existed at audit time). This updates theme copy only; legal policies and shipping/discount settings are not modified. WELCOME 10% remains. US-only shipping remains the owner requirement; hiding country selectors does not enforce checkout destinations.

Validation: all 184 tracked Liquid/JSON theme files pass Shopify Theme Check; 21 synthetic LiquidJS storefront fixtures pass, plus the 11 existing reviewed-product-information fixtures in the foundation checkpoint. Two missing editor translation keys found by the whole-theme audit are fixed. Run `npm ci --ignore-scripts` and `npm test` for repository fixture checks.

CI now runs Theme Check and fixtures on pushes/pull requests. Theme Check gets checks-write permission for reporting. Lighthouse is manual because it requires configured store credentials; skipping it on automatic runs is not a performance result. Remote CI status must be checked after pushing.

Browser validation remains blocked in this execution environment: a downloaded Chromium binary could not launch (permission error and crash). No mobile/browser, real Shopify preview, actual customer checkout, accessibility-conformance or Lighthouse pass is claimed. Synthetic fixture validation does not prove Shopify runtime behavior. A code branch is complete for review; production release still requires these checks.

Before release, use an unpublished theme, reconcile current theme-editor values, verify real menus and Search & Discovery configuration, create/populate approved product content data, inspect active/no-active/empty seasonal skins, verify mobile/cart/search/filter behavior, audit actual policies and test US-only shipping. The latest earlier shipping read had zero active methods; this code does not repair rates. Existing Shopify menu content and policies can still contain outdated text outside these repository files.

Rollback: retain the previous theme/settings and restore the prior Git revision. Product publication, prices, supplier routing, Shopify menus, filters and customer email flows are unchanged by this branch.
