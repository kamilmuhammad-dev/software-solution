# Data cleanup summary

| Metric | Value |
|---|---|
| Rows before cleanup | 344 |
| Rows after cleanup | 320 |
| Duplicate rows removed | 24 |
| Missing or invalid dates | 19 |
| Missing or invalid emails | 78 |
| Invalid quantities | 23 |
| Invalid prices | 17 |
| Unknown statuses | 0 |
| Rows with no quality issues | 196 |
| Cleaned revenue | 61,974.21 |

## What changed

- Duplicate rows were removed.
- Dates were normalized to YYYY-MM-DD and invalid dates were flagged.
- Emails were lowercased and checked for valid formatting.
- Quantities and prices were converted to numbers; invalid values were flagged.
- Status values were mapped to a consistent set.
- Revenue was calculated only for valid, non-refunded, non-cancelled rows.

## Files

- `output/clean_sales.csv`
- `output/clean_sales.xlsx`
- `output/cleanup_summary.md`
- `../assets/cleanup_quality.png`
