# Sales report automation sample

This sample consolidates monthly CSV exports into one formatted Excel report. It is the kind of workflow that can be rerun each week or month with one command.

## What the script does

- Finds all `sales_*.csv` files in the samples folder.
- Combines the files and removes duplicate rows.
- Parses dates and numbers, and excludes rows with missing required values.
- Calculates revenue per row.
- Builds monthly, region, product and channel summaries.
- Writes a formatted Excel workbook with charts.
- Writes a short Markdown summary and two PNG charts.

## Results from the sample

| Metric | Value |
|---|---|
| Files read | 3 |
| Rows read | 282 |
| Duplicate rows removed | 12 |
| Rows excluded for missing values | 24 |
| Clean rows used | 246 |
| Total revenue | USD 75,304.57 |
| Best month | 2026-01 (USD 27,778.07) |
| Top region | Abuja (USD 16,414.82) |
| Top product | Automation Sprint (USD 21,162.66) |
| Top channel | referral (USD 20,894.37) |

## Run it

```powershell
python make_sample_data.py
python build_report.py
```

## Files

- `samples/` - generated monthly source files
- `build_report.py` - consolidation and report script
- `output/sales_report.xlsx` - formatted report
- `output/report_summary.md` - short summary
- `../assets/report_revenue_by_month.png`
- `../assets/report_revenue_by_region.png`

This is a synthetic sample, not a client result.
