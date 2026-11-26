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

## Follow-up audit (2026-11-26)

- `scripts/index_keep.json` contains **288** SPN URLs: **31** RU (`kody/spn-*.html`) and **257** EN (`en/kody/spn-*.html`). These are explicit allowlists for indexing, NOT total numbers of pages in the code database. A mass noindex removal should **not** be performed without GSC evidence and manual content-quality review.
- Checked `sitemap-ru-kody.xml`: it contains **31** URLs, matching the 31 RU entries on the allowlist. Checked `sitemap-ru-marki.xml`: **62** brand URLs. Checked `sitemap-ru-main.xml`: **5** URLs.
- DieselCodes `sitemap.xml` currently contains **86** URL locations (46 with `/kody/`, 15 with `/marki/`, 7 with `/problemy/`, plus other sections). These are source-repository counts, not confirmed Google indexing.
- The English symptom generator `scripts/build_en_marki_problemy.py` had the same no-start generic risk logic as the Russian generator. Its no-start special case has been corrected on the draft branch, so future generation does not reintroduce the specific contradiction.
- Added a standalone read-only audit tool to both repositories at `scripts/audit_static_seo.py`. It checks static HTML titles, H1 counts, canonical targets, duplicate titles, broken local links, XML sitemap references, and sitemap/noindex mismatches. It runs locally on the complete checkout; output requires inspection before remediation. The tool has **not yet been executed against a full checkout**, so no result counts are claimed.
- The two PRs remain **draft**; branch updates do not deploy production changes.

### Recommended order

1. Run `python scripts/audit_static_seo.py --json seo-audit-results.json` on each complete repo checkout and triage false positives (fragment anchors, redirects, externally hosted pages).
2. Test the Python generators and render a sample RU/EN no-start page into a temporary build directory. Check for regressions before merging.
3. Obtain GSC export for URLs with impressions; review which noindex SPN pages are content-rich enough to re-open, without lifting the allowlist globally.
4. Review the risk-message mapping and output (HTML + FAQ structured data) for priority vehicle-control, braking, oil-pressure and overheating codes.

## Static source cross-check, follow-up

- CodeTruck sitemap section counts: RU codes 31, makes 62, heaters 138, analyses 14, J1587 28, VAG heaters 17, main pages 5. All sampled entries were unique. No claim is made about Google index coverage.
- DieselCodes sitemap includes 86 URLs. Sampled 10 English pages (home, directories, selected SPNs, symptoms and maker pages) each had one title, one H1, one canonical and no explicit `noindex`. Eight sampled pages had no missing local links when validated against the repository's 107-path tree. This was a **sample**, not a full-site crawl.
- CodeTruck sampled SPN pages 91, 100, 102, 110 were indexable and SPN 1 carried `noindex`, consistent with the RU allowlist.
- Added `scripts/audit_index_policy.py` to validate all RU SPN pages against the allowlist and `sitemap-ru-kody.xml` upon a local checkout. It **has not been executed** in the GitHub-connected environment.
- Direct network checkout is blocked in the inspection environment; code and spot checks were obtained through the GitHub connector. Therefore full local execution, visual browser rendering, and CI validation remain pending.

### Pre-merge commands

```bash
python scripts/check_diagnostic_copy.py
python scripts/audit_static_seo.py --json seo-audit-results.json
python scripts/audit_index_policy.py
```

For DieselCodes, run the first two commands only. Run page-generation commands in a disposable copy or worktree after reviewing side effects; never regenerate into a production checkout blindly.

## Repository-tree sitemap integrity check

Performed a complete **repository file-tree ↔ sitemap location** cross-check using GitHub API (not a browser crawl):

| Metric | CodeTruck | DieselCodes |
| --- | ---: | ---: |
| HTML files | 2,501 | 87 |
| Unique HTML pages in XML sitemaps | 295 | 86 |
| Sitemap targets missing from repository | 0 | 0 |
| HTML files not named by sitemaps | 2,206 | 1 |

The DieselCodes file outside sitemap is `404.html` (expected). CodeTruck's 2,206 unlisted files break down as 2,172 in `kody/`, 28 in `problemy/`, 3 in `otopiteli/`, plus `404.html` and two search-engine verification files. The `otopiteli/index.html` path is actually indexed via the main sitemap as directory `/otopiteli/`; the three unlisted standalone heater code pages have `noindex` in inspected source.

Sampled missing-from-sitemap symptom pages (`ne-zavoditsya`, `glohnet-na-hodu`, `gorit-check-engine`, `upala-moshchnost`, `peregrev-dvigatelya`) all have `noindex`. These exclusions appear deliberate rather than evidence of broken site generation. Validate all 28 during the full offline script run before claiming exhaustive consistency.

**CI status:** Draft-branch GitHub Actions workflows were added in both repositories. At the time of this check, no workflow runs had been reported for the draft branches. Tests have not been executed by GitHub Actions, and a direct git clone was blocked by the execution environment's DNS/network restrictions. The PRs remain draft.

## Language-architecture clarification (user-confirmed, 2026-11-26)

**CodeTruck.ru is Russian-only. DieselCodes.com is the separate English site.** The previous /en/ content on CodeTruck was removed, with visitor-facing redirection messaging pointing to DieselCodes. No plan to republish CodeTruck /en/ pages.

Verified in CodeTruck's `master` GitHub tree: there are **zero paths under `en/`**. `scripts/build_pages.py` explicitly documents removal of English content on **2026-11-14** and says that the English content belongs to `dieselcodes.com`. CodeTruck's `robots.txt` still mentions old `/en/` redirect stubs; the repository tree does not contain such files. The actual live-server redirection/message behavior has NOT yet been verified.

**Interpretation correction:** The **257** English SPN paths in `scripts/index_keep.json` are historic/orphaned allowlist entries, **not** 257 live or indexed CodeTruck English pages. Do not equate this list with current published English URL inventory.

Action:
- Audit whether the obsolete English entries can be cleaned from the allowlist without impacting current scripts or deployment.
- Keep canonical, sitemap and content language Russian-only on CodeTruck.
- Handle English SEO only on DieselCodes, avoid duplicating English pages at CodeTruck.
- Check any real server redirects separately; if implementing permanent URL migration, map old URLs to relevant English equivalents on DieselCodes, rather than blindly redirecting every path to the homepage.

## Dealer-code KV root cause — 2026-11-26

Private, read-only local reports of Cloudflare `PCODE_KV` found 28,350 dealer records and all 64 search-index shards. Initial count of **65 `dealer_record_missing_from_direct_index`** was a **false positive due to comparing raw, non-normalized KV key suffixes to normalized index terms**.

A follow-up private diagnosis confirmed that normalized keys for all 65 records are present in the search index, with no wrong-shard or cross-brand findings. Distribution: `cumminsisb` 6, `cumminsislisc` 45, `cumminsisx` 14. Of these, 61 raw identifiers differ in case only, and four Cummins ISX identifiers have a complex hyphenated form. Worker `cleanInput()` uppercases user input *before* `shapeOk()`, so raw lowercase in KV keys is not by itself evidence that real users will receive a 400 response.

**Do not rebuild the KV index** for this issue. A Worker-input regression test was added as `scripts/test_pcode_worker_input.cjs` and wired into draft-branch CI. This checks representative input formats using the actual Worker parser, but has not been run on GitHub Actions yet.

Next: validate the four complex Cummins ISX identifier forms privately, against the actual parser and the respective KV key behavior. Any output shared outside the local machine should be only aggregate counts, without dealer-code identifiers, descriptions, account IDs or credentials. If these cases are genuinely rejected, prepare a narrow worker parser fix and test it before deployment. No KV writes or deployments have been made.
