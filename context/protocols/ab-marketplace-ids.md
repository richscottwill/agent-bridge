# AB Paid Acquisition — Marketplace IDs (canonical lookup)

**Purpose:** Prevent the category of error that produced the 2026-05-03 paid-search-hubble-query-library v1 bug where marketplace_ids were confused across markets, silently blending data in cross-team reporting.

**Verified:** 2026-05-03 via DataCentral Workbench (kiro-local) against `abbd_sandbox_mktg.m_amo_paid_search.tracking_url` domain patterns.

**Applies to:** Any agent or person generating SQL against `abbd_sandbox_mktg` on the ABDAI Redshift cluster (`abdw-dev-rs-01` / ABATLAS-DTL). **Do not reconstruct this mapping from memory or from other clusters — read from this file.** Marketplace_ids differ by cluster and have historically changed; the v1 doc shipped with an incorrect mapping because it was inferred rather than verified.

## The mapping

| Market | marketplace_id | Notes |
|---|---:|---|
| US | 1 | |
| UK | 3 | |
| DE | 4 | |
| FR | 5 | |
| JP | 6 | Uses Google + Bing + Yahoo; distinct `JP_AB_PSA_*` reftag taxonomy — v1 filter catches only ~13% of JP regs, needs rework |
| CA | 7 | |
| IT | 35691 | Previously believed to be MX. URLs resolve to `amazon.it`. |
| ES | 44551 | Previously believed to be IT-secondary. URLs resolve to `amazon.es`. |
| AU | 111172 | |
| MX | 771770 | Single ID. Previously believed to be a secondary MX alongside 35691. |
| IN | 44571 | Bing-only, separate `octosbng_*` reftag taxonomy — covered in the paid-search library's India appendix only |

**Markets explicitly not in the cluster:** marketplace_ids `8` and `9` do not exist in `abbd_sandbox_mktg`. Do not include them in any CTE or filter.

## The safety check — run before any new analysis

Any agent generating new SQL against this cluster should include this domain-probe query output alongside the analysis, or verify the mapping separately. If the output contradicts the table above, the cluster schema has drifted and this file needs an update.

```sql
SELECT marketplace_id,
  CASE
    WHEN tracking_url ILIKE '%amazon.com.mx%'  THEN 'MX'
    WHEN tracking_url ILIKE '%amazon.es%'      THEN 'ES'
    WHEN tracking_url ILIKE '%amazon.it%'      THEN 'IT'
    WHEN tracking_url ILIKE '%amazon.com.au%'  THEN 'AU'
    WHEN tracking_url ILIKE '%amazon.in%'      THEN 'IN'
    WHEN tracking_url ILIKE '%amazon.de%'      THEN 'DE'
    WHEN tracking_url ILIKE '%amazon.fr%'      THEN 'FR'
    WHEN tracking_url ILIKE '%amazon.co.uk%'   THEN 'UK'
    WHEN tracking_url ILIKE '%amazon.ca%'      THEN 'CA'
    WHEN tracking_url ILIKE '%amazon.co.jp%'   THEN 'JP'
    WHEN tracking_url ILIKE '%amazon.com%'     THEN 'US/com'
    ELSE 'other'
  END AS domain_market,
  COUNT(*) AS rows_7d
FROM abbd_sandbox_mktg.m_amo_paid_search
WHERE start_date >= CURRENT_DATE - 7
  AND tracking_url IS NOT NULL
GROUP BY marketplace_id, 2
ORDER BY marketplace_id, rows_7d DESC;
```

## How to use this in a market_map CTE

```sql
WITH market_map AS (
    SELECT 1      AS raw_id, 'US' AS market UNION ALL
    SELECT 3,      'UK' UNION ALL
    SELECT 4,      'DE' UNION ALL
    SELECT 5,      'FR' UNION ALL
    SELECT 6,      'JP' UNION ALL
    SELECT 7,      'CA' UNION ALL
    SELECT 35691,  'IT' UNION ALL
    SELECT 44551,  'ES' UNION ALL
    SELECT 111172, 'AU' UNION ALL
    SELECT 771770, 'MX'
    -- 44571 (IN) intentionally omitted; uses different taxonomy
)
```

Teammates querying Hubble should filter by `market = 'MX'`, not by `marketplace_id = 771770` — the CTE does the translation, and the shared abstraction means any future correction happens in one place.

## Known registration-side data lag

`abbd_sandbox_mktg.w_ab_mktg_reftags_reg` has a 2-3 day lag. Any reg-side query using `register_day >= CURRENT_DATE - N` silently under-reports the trailing days. Use `register_day BETWEEN CURRENT_DATE - N AND CURRENT_DATE - 3` for reg queries, and match the cost-side window the same way for consistency in joined queries.

## Change log

**2026-05-03 v1:** Created as a consequence of kiro-local's audit of `paid-search-hubble-query-library.docx` v1, which shipped with an inferred (and wrong) market_map. Purpose: next time an agent or person needs the mapping, read from here.
