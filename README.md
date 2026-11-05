# Custom Software Solution - Portfolio

Python automation and data cleanup samples by Kamil Muhammad.

These are synthetic portfolio samples built to show the workflow, not client work or client results. Each sample includes the source data, the script, the output and a short write-up.

## Samples

### 1. Data cleanup

Turn a messy sales export into a clean, validated Excel file with a quality summary.

- Source: `data-cleanup/messy_sales.csv`
- Script: `data-cleanup/clean_sales.py`
- Output: `data-cleanup/output/clean_sales.xlsx`
- Summary: `data-cleanup/output/cleanup_summary.md`
- Case study: `data-cleanup/CASE_STUDY.md`
- Result: 344 messy rows reduced to 320 clean rows; 24 duplicates removed and 78 email issues flagged.

### 2. Sales report automation

Consolidate monthly CSV exports into one formatted Excel report with monthly, region, product and channel summaries.

- Source: `report-automation/samples/`
- Script: `report-automation/build_report.py`
- Output: `report-automation/output/sales_report.xlsx`
- Summary: `report-automation/output/report_summary.md`
- Case study: `report-automation/CASE_STUDY.md`
- Result: 3 files and 282 rows consolidated into one report with 246 clean rows used.

## Packages

| Package | Price | Scope |
|---|---|---|
| Data Cleanup | USD 49 | Up to 1,000 rows, dedupe, normalize, validate, summary |
| Python Automation | USD 99 | One workflow, script, README, one revision, handover |
| Cleanup + Automation | USD 199 | Both plus a short before/after report |

Hourly floor: USD 20/hr. Turnaround is about 2-4 days for small projects.

## Run the samples

```powershell
cd portfolio/data-cleanup
python make_sample_data.py
python clean_sales.py

cd ../report-automation
python make_sample_data.py
python build_report.py
```

Requirements: Python 3.11+, pandas, openpyxl, matplotlib.

## Contact

- Business: Custom Software Solution
- Email: muhammadkamilukamil@gmail.com
- Phone: +2349129250475
- GitHub: https://github.com/kamilmuhammad-dev/software-solution
- Live page: https://kamilmuhammad-dev.github.io/software-solution/
