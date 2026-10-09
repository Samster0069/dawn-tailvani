# Shopify store setup: record of what was done in the admin (not stored in theme files)

Theme code lives on branch `revamp-seasonal`. Everything below lives in Shopify itself and is recorded here so it can be rebuilt.

## Metaobjects
- Definitions:
  - `tailvani_supplier`: gid MetaobjectDefinition/26681082135, admin-only
  - `tailvani_season_skin`: gid MetaobjectDefinition/26681114903, storefront read
- The skin definition gained these fields during the rebuild: `color_band`, `color_dark`, `feature_image`, `feature_heading`, `feature_text`.
- 16 skins:
  - created by `01-skins-create.graphql`
  - colours, images and copy updated by `02-skins-update-rebuild.graphql`
- Later edits:
  - `hero_collection` linked per skin (see table)
  - winter `feature_text` = "Cozy sweaters and coats for cats and small dogs who feel the chill."
  - The images behind 8 hero and 10 feature file IDs were replaced in place (same filenames/IDs) to target cats and small dogs (media commit 6ede578).

| Skin | Collection |
|---|---|
| fall, thanksgiving | fall |
| halloween | halloween |
| cat day | cats |
| bfcm, holidays | holiday-gifts |
| winter, spring, summer | matching season |
| new year, anniversary | new-arrivals |
| valentines | valentines |
| st-patricks | st-patricks |
| easter | easter |
| july4 | fourth-of-july |
| dog day | dogs |

## Collections (smart, published to Online Store)
- Created by `03-collections-create.graphql`.
- Plus `other-pets` (TAG = pet:other).
- Old manual collections renamed `apparel-old-catalog` / `accessories-old-catalog`.
- Tag taxonomy:
  - `pet:cat`, `pet:dog`, `pet:other`
  - `type:apparel`, `type:accessories`, `type:toys`, `type:beds`, `type:grooming`
  - `season:fall`, `season:winter`, `season:spring`, `season:summer`
  - `occasion:halloween`, `occasion:holidays`, `occasion:valentines`, `occasion:st-patricks`, `occasion:easter`, `occasion:july4`
  - `disc:all`, `disc:max10` (promo eligibility); `SRC-<CODE>` (supplier)
- Promo collections: `promo-up-to-20` (disc:all) and `promo-up-to-10` (disc:all OR disc:max10).

## Menus
- `main-menu`: New arrivals, Cats, Dogs, Clothing, Accessories (All accessories, Toys, Beds and blankets, Grooming, Other pets), Help
- `footer-shop`: New arrivals, Cats, Dogs, Other pets, Clothing, Accessories, About Tailvani
- `footer`: Help and FAQ, Contact, Shipping policy, Refund policy, Privacy policy, Terms of service, Your privacy choices, Search

## Pages
- `/pages/about` (template suffix `about`)
- `/pages/faq` (template suffix `faq`; the answers live in templates/page.faq.json)

## Files
- 43 images uploaded from `upload/` (IDs in `shopify-file-ids.json`), plus `tailvani-mark.png` (favicon).

## Store state at time of record (Oct 9, 2026)
- Password page on.
- 14 old products in Draft.
- WELCOME = 10% off, once per customer.
- Free shipping rate on orders of $35+.
- Live theme `dawn-tailvani/main` is unchanged; `dawn-tailvani/revamp-seasonal` is the unpublished preview.
