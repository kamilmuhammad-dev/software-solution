# Case study: automating a monthly sales report

**Client type:** small business or agency
**Tools:** Python, pandas, openpyxl, matplotlib
**Type:** portfolio sample using synthetic data

## Problem

Monthly exports arrived in separate CSV files. Preparing the report meant repeating the same manual steps: copying files, removing duplicates, fixing numbers, building pivot summaries and formatting the workbook.

## Approach

1. Standardize the input file naming pattern.
2. Combine every monthly file and remove duplicate rows.
3. Parse dates and numbers, and exclude rows with missing required values.
4. Calculate revenue and build monthly, region, product and channel summaries.
5. Write a formatted Excel workbook with a chart.
6. Save a short summary so the numbers can be reviewed quickly.

## Result

- 3 files and 282 rows consolidated into one report.
- 12 duplicate rows removed.
- 24 incomplete rows excluded.
- 246 clean rows used.
- Total revenue: USD 75,304.57.
- One command rebuilds the report when new files arrive.

## What this shows

A repeatable reporting workflow that replaces copy-paste steps and keeps the cleaning rules consistent from month to month.

The same approach fits the USD 99 Python Automation package and the automation half of the USD 199 Bundle.

## Links

- Script: `build_report.py`
- Report: `output/sales_report.xlsx`
- Chart: `../assets/report_revenue_by_month.png`
