# Portfolio Analysis — Short Write-Up

## Executive Summary

Written Premium remained broadly stable at portfolio level in 2024.

Total Written Premium decreased from approximately **MXN 5.94B in 2023 to MXN 5.94B in 2024**, representing a year-over-year decline of approximately **0.08%**, or **MXN 4.5M**.

Although the overall portfolio changed only slightly, this result masks meaningful differences across industries.

---

## Industry Performance

### Construction

Construction was the largest positive contributor to Premium Change in 2024.

Written Premium increased by approximately **MXN 142.8M**, representing growth of about **9%** versus 2023.

The increase was supported by both:

- approximately **5% growth in policy count**, and
- approximately **4% growth in Premium per policy**.

This suggests that the increase was associated with a combination of higher policy volume and higher average Premium per policy.

### Health

Health recorded one of the strongest relative increases in Written Premium, growing approximately **24%**, or **MXN 65.0M**.

This occurred despite an approximately **5% decline in policy count**.

Premium per policy increased approximately **30%**, indicating that the Premium increase was associated primarily with higher Premium per policy rather than additional policy volume.

### Manufacturing

Manufacturing experienced one of the largest absolute Premium declines.

Written Premium decreased approximately **10%**, representing a reduction of around **MXN 75.3M**.

Policy count declined only approximately **1%**, while Premium per policy decreased approximately **9%**.

The movement was therefore associated primarily with lower Premium per policy rather than a substantial reduction in policy volume.

### Agriculture

Agriculture provides another example of why Premium Growth should not be interpreted in isolation.

Policy count increased approximately **5%**, while Premium per policy decreased approximately **20%**.

As a result, total Written Premium declined approximately **16%**, or **MXN 32.6M**.

---

## Business Interpretation

The portfolio-level result suggests relative stability in total Written Premium during 2024, but the industry analysis shows that this stability was produced by offsetting movements across segments.

Construction and Health generated meaningful positive Premium changes, while industries such as Manufacturing and Agriculture moved in the opposite direction.

The underlying drivers also differed by industry. In some cases, Premium movement was associated with changes in policy volume, while in others it was more closely associated with changes in Premium per policy.

For this reason, **Premium Growth should be evaluated together with absolute Premium Change, policy volume, and Premium per policy** rather than as a standalone metric.

---

## Data Quality Consideration

Industry information was originally missing for approximately **34.95%** of policy records.

A deterministic client-history strategy recovered **91.65% of the originally missing classifications**, increasing final portfolio classification coverage to approximately **97.08%**.

The remaining **1,472 records** were retained explicitly as `Unknown`.

This category remains visible in the dashboard and should be considered when interpreting industry-level results.

---

## Methodological Note

Written Premium is grouped by **policy inception year**, based on `policy_start_date`.

Year-over-year Premium Growth is calculated as:

`(Current Year Premium / Previous Year Premium) - 1`

The analysis describes observed portfolio movements and their decomposition. It does not establish causal explanations for changes in Premium, policy volume, or Premium per policy.