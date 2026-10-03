# Mexico P&C Portfolio — Data Scientist Technical Challenge

This project analyzes a Mexico Property & Casualty (P&C) insurance portfolio with a focus on two main objectives:

1. Recover missing industry classifications using a transparent and conservative data-quality strategy.
2. Analyze Written Premium and Premium Growth across industries and geographic segments through an interactive dashboard.

The solution prioritizes reproducibility, traceability, and explicit treatment of uncertainty.

---

## Project Structure

```text
chubb-data-scientist-challenge/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_industry_fill.ipynb
│   └── 03_premium_analysis.ipynb
├── reports/
│   ├── fill_quality_report.md
│   └── short_writeup.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 1. Data Quality Assessment

The portfolio contains **50,441 policy records**.

Initial exploratory analysis identified **17,631 records with missing industry information**, representing approximately **34.95% of the portfolio**.

Before applying any predictive method, client history was evaluated as a deterministic source of information.

Among clients with known industry information, no `ClientId` was associated with more than one known industry. This made client history a high-confidence source for recovering missing values.

---

## 2. Industry Fill Strategy

A conservative hierarchical strategy was used:

### Step 1 — Preserve original values

Existing industry classifications were never overwritten.

### Step 2 — Same-client history

When a policy had a missing industry but the same `ClientId` appeared in another policy with a known industry, that known classification was propagated to the missing record.

This recovered:

- **16,159 records**
- **91.65% of originally missing industry values**

After this step, only **1,472 records** remained unresolved.

### Step 3 — Evaluate predictive alternatives

Several approaches were evaluated for the remaining records:

- Supervised classification using policy characteristics
- Client-name TF-IDF classification
- High-precision semantic keyword rules
- External enrichment feasibility

These alternatives did not demonstrate sufficient predictive quality or reliability for automatic assignment.

Rather than forcing low-confidence predictions, unresolved records were explicitly classified as:

`Unknown`

This preserves uncertainty instead of introducing unsupported classifications.

### Final coverage

After deterministic recovery:

- **48,969 records classified**
- **1,472 records Unknown**
- **97.08% portfolio classification coverage**

The processed dataset also retains the original industry field and the method used for each record to preserve traceability.

---

## 3. Premium Analysis

Written Premium is analyzed using the policy inception year derived from `policy_start_date`.

Premium Growth is calculated as year-over-year growth:

```text
Premium Growth YoY =
(Current Year Premium / Previous Year Premium) - 1
```

The analysis also considers:

- Absolute Premium Change
- Policy count
- Client count
- Premium per policy
- Policy growth
- Premium-per-policy growth

This avoids interpreting percentage growth without considering portfolio size and underlying volume.

---

## 4. Key Portfolio Findings

At portfolio level, Written Premium remained broadly stable in 2024, declining approximately **0.08%** versus 2023.

However, the aggregate result masks meaningful industry-level movements.

**Construction** was the largest positive contributor to Premium Change, supported by growth in both policy volume and Premium per policy.

**Health** also showed strong Premium growth despite a lower policy count, primarily associated with a substantial increase in Premium per policy.

Conversely, **Manufacturing** experienced one of the largest absolute declines, mainly associated with lower Premium per policy rather than a significant reduction in policy volume.

These results demonstrate why Premium Growth should be interpreted together with absolute Premium Change, policy volume, and Premium per policy.

---

## 5. Interactive Dashboard

The Streamlit dashboard provides an interactive view of portfolio performance.

It includes:

- Written Premium
- Premium Growth YoY
- Premium Change
- Policy and client counts
- Premium trends over time
- Industry analysis
- Geographic analysis
- Dynamic filters by year, industry, state, and municipality
- Dynamic portfolio and industry insights

The dashboard preserves `Unknown` as a visible industry category so that unresolved classifications remain transparent throughout the analysis.

---

## 6. Running the Project

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd chubb-data-scientist-challenge
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

The processed dataset must be available at:

```text
data/processed/portfolio_mexico_filled.csv
```

---

## 7. Reproducibility

The project separates:

- Exploratory analysis
- Industry recovery
- Premium analysis
- Visualization

The notebooks can be executed sequentially:

```text
01_eda.ipynb
      ↓
02_industry_fill.ipynb
      ↓
03_premium_analysis.ipynb
      ↓
dashboard/app.py
```

No original industry classifications are overwritten during the fill process.

---

## 8. Limitations

The remaining `Unknown` records correspond primarily to clients without reliable historical industry information.

Predictive and text-based approaches were evaluated but intentionally not used for automatic classification because their validation performance was insufficient.

External enrichment was also not applied because client names did not provide sufficiently reliable evidence for deterministic matching.

With additional validated external company information, the remaining unresolved records could be revisited.

---

## 9. Technology Stack

- Python
- pandas
- NumPy
- scikit-learn
- Plotly
- Streamlit
- Jupyter / Google Colab
- Git / GitHub