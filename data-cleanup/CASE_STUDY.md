# Case study: cleaning a messy sales export

**Client type:** small sales or operations team
**Tools:** Python, pandas, openpyxl, matplotlib
**Type:** portfolio sample using synthetic data

## Problem

The sample export had the problems that make spreadsheet reporting unreliable:

- duplicate order rows
- dates in several formats, plus blanks
- missing and malformed emails
- quantities with extra spaces, blanks and negative values
- prices stored as currency strings
- inconsistent region, product and status values

## Approach

1. Profile the file and count each quality issue.
2. Normalize text, dates, emails, quantities and prices.
3. Flag rows that still need a human decision instead of silently guessing.
4. Remove exact duplicates and calculate revenue only for valid rows.
5. Deliver a clean CSV, an Excel workbook and a short summary of what changed.

## Result

- 344 messy rows reduced to 320 clean rows.
- 24 duplicate rows removed.
- 19 date issues and 78 email issues flagged.
- 23 invalid quantities and 17 invalid prices flagged.
- Every row now carries a `data_quality_flag` so exceptions are easy to review.

## What this shows

A repeatable cleanup workflow that produces a usable file and an audit trail of the changes, instead of a one-off manual edit.

The same approach fits the USD 49 Data Cleanup package and the cleanup half of the USD 199 Bundle.

## Links

- Script: `clean_sales.py`
- Output: `output/clean_sales.xlsx`
- Quality chart: `../assets/cleanup_quality.png`
