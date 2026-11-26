# CodeTruck / DieselCodes — initial source audit (2026-11-26)

Scope: read-only inspection of both GitHub repositories, plus **draft** changes on `audit/safety-copy-2026-11-26`. This is not a production deployment, a crawl of every generated page, or a Search Console audit.

## Repositories

- CodeTruck: `alexmoto116-commits/truck-diag-pro-kody` (default: `master`), CNAME `codetruck.ru`.
- DieselCodes: `alexmoto116-commits/dieselcodes` (default: `main`), CNAME `dieselcodes.com`.

## Verified SEO facts

- Both repositories have `robots.txt`, `sitemap.xml` and canonical URLs on their home pages.
- CodeTruck's `sitemap.xml` is an index referencing category sitemaps for codes, makes, heaters, articles, J1587 and other content.
- DieselCodes `sitemap.xml` is a direct URL list.
- CodeTruck `robots.txt` explicitly disallows several AI and SEO crawlers, including `OAI-SearchBot`, `ChatGPT-User`, `AhrefsBot` and `SemrushBot`. Googlebot and Bingbot search access are separately allowed. Evaluate AI search visibility and privacy/business tradeoffs before changing this policy.
- CodeTruck's `problemy/ne-zavoditsya.html` currently contains `noindex, follow`; decide whether that is intentional before SEO rollout.
- DieselCodes `index.html` includes the warning: `Fault names and factory tables in the database are in Russian`. Confirm actual database-language coverage before removing or promising fully English results.
- Source code has structured data (TechArticle/FAQPage) on sampled diagnostic pages. Schema presence does not prove validity or search appearance.

## Confirmed diagnostic-content issues

1. Both `problemy/ne-zavoditsya.html` pages had templated advice about continuing to drive to a stop while discussing a non-starting engine. The context was contradictory.
2. DieselCodes `kody/spn-91.html` had a categorical `Safe to drive` label although the page itself described possibly unpredictable accelerator response.
3. CodeTruck's `scripts/build_pages.py` could regenerate the generic no-start risk text. A generator-level guard has now been added.

## Draft fixes, not merged

- CodeTruck PR: https://github.com/alexmoto116-commits/truck-diag-pro-kody/pull/1
- DieselCodes PR: https://github.com/alexmoto116-commits/dieselcodes/pull/1
- Each proposed branch includes a Python copy-regression script: `scripts/check_diagnostic_copy.py`.
- Review fixes against manufacturer procedures and visually inspect resulting pages before merging.
- **Important:** regression checks target specific copy regressions; they are not comprehensive vehicle-safety verification.

## Next engineering tasks

**P0 — before broad publication**
1. Review the generated site templates `scripts/build_pages.py`, `scripts/build_en_pages.py` and `scripts/build_en_marki_problemy.py` for repeated context-inappropriate advice; align data sources and templates for both languages.
2. Add broader generator-level tests and a build pipeline that regenerates to a temporary directory, validates HTML and links, then publishes only after approval.
3. Audit SPN/FMI safety messages with qualified mechanic input and manufacturer documentation. Avoid blanket permission-to-drive based on SPN alone.

**P1 — SEO**
1. Compare sitemap URL sets to generated files, canonicals, `noindex`, and internal links; resolve intentional vs accidental exclusions.
2. Validate English search-result content and real database translation coverage.
3. Use Search Console and Yandex Webmaster exports to prioritize pages by impressions and achievable click gains.
4. Add approved relevant video embeds and stable UTM links without slowing page load.

**P2 — product**
1. Measure CWV with representative mobile page samples.
2. Prioritize improvements to the existing code search and symptom navigation over net-new AI tools.

## Boundaries

No production site was deployed. No Google Search Console/analytics data was accessed. No repository-wide test run or live-browser render was performed during this review.
