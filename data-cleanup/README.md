# Data cleanup sample

This sample starts with a deliberately messy sales export and produces a clean workbook plus a one-page quality summary.

## What the script does

- Removes exact duplicate rows.
- Normalizes whitespace, casing and order IDs.
- Parses multiple date formats and flags invalid dates.
- Lowercases emails and checks their format.
- Converts quantities and prices to numbers and flags invalid values.
- Maps status values to a consistent set.
- Calculates revenue only for valid, non-refunded, non-cancelled rows.
- Writes a clean CSV, a formatted Excel workbook and a Markdown summary.
- Creates a before/after quality chart.

## Results from the sample

| Metric | Value |
|---|---|
| Rows before cleanup | 344 |
| Rows after cleanup | 320 |
| Duplicate rows removed | 24 |
| Missing or invalid dates | 19 |
| Missing or invalid emails | 78 |
| Invalid quantities | 23 |
| Invalid prices | 17 |
| Rows with no quality issues | 196 |
| Cleaned revenue | USD 61,974.21 |

## Run it

```powershell
python make_sample_data.py
python clean_sales.py
```

## Files

- `messy_sales.csv` - generated messy source data
- `clean_sales.py` - cleanup script
- `output/clean_sales.csv` - clean data
- `output/clean_sales.xlsx` - workbook with Clean Data and Summary sheets
- `output/cleanup_summary.md` - short report
- `../assets/cleanup_quality.png` - quality chart

This is a synthetic sample, not a client result.
