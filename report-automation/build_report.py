from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT / "samples"
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT.parent / "assets"


def load_sales() -> tuple[pd.DataFrame, dict[str, int]]:
    files = sorted(SAMPLES.glob("sales_*.csv"))
    if not files:
        raise SystemExit("No sample files found. Run make_sample_data.py first.")
    frames = []
    for path in files:
        frame = pd.read_csv(path, dtype=str).fillna("")
        frame["source_file"] = path.name
        frames.append(frame)
    raw = pd.concat(frames, ignore_index=True)
    rows_read = len(raw)

    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.drop_duplicates(subset=["date", "product", "region", "channel", "customer_type", "units", "unit_price"]).copy()
    duplicates_removed = rows_read - len(df)
    missing = df["date"].isna() | df["units"].isna() | df["unit_price"].isna()
    excluded = int(missing.sum())
    clean = df.loc[~missing].copy()
    clean["revenue"] = (clean["units"] * clean["unit_price"]).round(2)
    clean["period"] = clean["date"].dt.to_period("M").astype(str)
    stats = {
        "files": len(files),
        "rows_read": rows_read,
        "duplicates_removed": duplicates_removed,
        "excluded_missing": excluded,
        "clean_rows": len(clean),
    }
    return clean, stats


def build_tables(clean: pd.DataFrame) -> dict[str, pd.DataFrame]:
    monthly = (
        clean.groupby("period", as_index=False)
        .agg(orders=("revenue", "size"), units=("units", "sum"), revenue=("revenue", "sum"))
        .sort_values("period")
    )
    monthly["avg_order_value"] = (monthly["revenue"] / monthly["orders"]).round(2)
    monthly = monthly.rename(columns={
        "period": "Period",
        "orders": "Orders",
        "units": "Units",
        "revenue": "Revenue",
        "avg_order_value": "Avg Order Value",
    })

    regions = (
        clean.groupby("region", as_index=False)
        .agg(orders=("revenue", "size"), units=("units", "sum"), revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .rename(columns={"region": "Region", "orders": "Orders", "units": "Units", "revenue": "Revenue"})
    )
    products = (
        clean.groupby("product", as_index=False)
        .agg(orders=("revenue", "size"), units=("units", "sum"), revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .rename(columns={"product": "Product", "orders": "Orders", "units": "Units", "revenue": "Revenue"})
    )
    channels = (
        clean.groupby("channel", as_index=False)
        .agg(orders=("revenue", "size"), units=("units", "sum"), revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
        .rename(columns={"channel": "Channel", "orders": "Orders", "units": "Units", "revenue": "Revenue"})
    )
    quality = pd.DataFrame([
        ("Revenue", round(float(clean["revenue"].sum()), 2)),
        ("Orders", len(clean)),
        ("Units", int(clean["units"].sum())),
        ("Average order value", round(float(clean["revenue"].mean()), 2)),
    ], columns=["Metric", "Value"])
    return {
        "Monthly": monthly,
        "Regions": regions,
        "Products": products,
        "Channels": channels,
        "Summary": quality,
    }


def style_sheet(writer, sheet_name: str, frame: pd.DataFrame) -> None:
    sheet = writer.sheets[sheet_name]
    sheet.freeze_panes = "A2"
    header_fill = PatternFill("solid", fgColor="0F766E")
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
    for index, column in enumerate(frame.columns, start=1):
        width = max(12, min(32, int(frame[column].astype(str).str.len().max() if len(frame) else 12) + 2))
        sheet.column_dimensions[get_column_letter(index)].width = width
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            if isinstance(cell.value, (int, float)) and cell.column_letter in {"D", "E"}:
                cell.number_format = '#,##0.00'


def add_monthly_chart(writer, monthly: pd.DataFrame) -> None:
    sheet = writer.sheets["Monthly"]
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Revenue by month"
    chart.y_axis.title = "Revenue"
    chart.x_axis.title = "Month"
    data = Reference(sheet, min_col=4, min_row=1, max_row=len(monthly) + 1)
    categories = Reference(sheet, min_col=1, min_row=2, max_row=len(monthly) + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    chart.height = 7
    chart.width = 14
    sheet.add_chart(chart, "G2")


def make_charts(monthly: pd.DataFrame, regions: pd.DataFrame) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(monthly["Period"], monthly["Revenue"], color="#0f766e")
    ax.set_title("Revenue by month")
    ax.set_ylabel("USD")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    fig.savefig(ASSETS_DIR / "report_revenue_by_month.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ordered = regions.sort_values("Revenue")
    ax.barh(ordered["Region"], ordered["Revenue"], color="#f97316")
    ax.set_title("Revenue by region")
    ax.set_xlabel("USD")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    fig.savefig(ASSETS_DIR / "report_revenue_by_region.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    clean, stats = load_sales()
    tables = build_tables(clean)
    output = OUTPUT_DIR / "sales_report.xlsx"
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, frame in tables.items():
            frame.to_excel(writer, sheet_name=sheet_name, index=False)
            style_sheet(writer, sheet_name, frame)
        clean[["date", "product", "region", "channel", "customer_type", "units", "unit_price", "revenue"]].to_excel(
            writer, sheet_name="Clean Data", index=False
        )
        style_sheet(writer, "Clean Data", clean)
        pd.DataFrame([
            ("Files read", stats["files"]),
            ("Rows read", stats["rows_read"]),
            ("Duplicate rows removed", stats["duplicates_removed"]),
            ("Rows excluded for missing values", stats["excluded_missing"]),
            ("Clean rows", stats["clean_rows"]),
        ], columns=["Metric", "Value"]).to_excel(writer, sheet_name="Data Quality", index=False)
        style_sheet(writer, "Data Quality", pd.DataFrame([("Metric", "")]))
        add_monthly_chart(writer, tables["Monthly"])

    make_charts(tables["Monthly"], tables["Regions"])
    best_month = tables["Monthly"].sort_values("Revenue", ascending=False).iloc[0]
    top_region = tables["Regions"].iloc[0]
    top_product = tables["Products"].iloc[0]
    top_channel = tables["Channels"].iloc[0]
    lines = [
        "# Sales report automation summary",
        "",
        "## Input",
        "",
        f"- Files read: {stats['files']}",
        f"- Rows read: {stats['rows_read']}",
        f"- Duplicate rows removed: {stats['duplicates_removed']}",
        f"- Rows excluded for missing values: {stats['excluded_missing']}",
        f"- Clean rows used: {stats['clean_rows']}",
        "",
        "## Headlines",
        "",
        f"- Total revenue: USD {clean['revenue'].sum():,.2f}",
        f"- Best month: {best_month['Period']} (USD {best_month['Revenue']:,.2f})",
        f"- Top region: {top_region['Region']} (USD {top_region['Revenue']:,.2f})",
        f"- Top product: {top_product['Product']} (USD {top_product['Revenue']:,.2f})",
        f"- Top channel: {top_channel['Channel']} (USD {top_channel['Revenue']:,.2f})",
        "",
        "## Files",
        "",
        "- `output/sales_report.xlsx`",
        "- `output/report_summary.md`",
        "- `../assets/report_revenue_by_month.png`",
        "- `../assets/report_revenue_by_region.png`",
        "",
        "This is a synthetic portfolio sample, not a client result.",
    ]
    (OUTPUT_DIR / "report_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
