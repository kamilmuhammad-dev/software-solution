from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "messy_sales.csv"
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT.parent / "assets"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
STATUS_MAP = {
    "paid": "paid",
    "pending": "pending",
    "refunded": "refunded",
    "cancelled": "cancelled",
    "canceled": "cancelled",
}


def parse_date(value: object) -> pd.Timestamp | pd.NaT:
    text = str(value or "").strip()
    if not text:
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%b %d, %Y", "%B %d, %Y"):
        try:
            return pd.Timestamp(datetime.strptime(text, fmt).date())
        except ValueError:
            continue
    return pd.NaT


def parse_money(value: object) -> float:
    text = str(value or "").strip()
    if not text:
        return float("nan")
    text = text.replace("USD", "").replace("$", "").replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return float("nan")


def clean_text(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(SOURCE, dtype=str).fillna("")
    rows_before = len(raw)

    df = raw.copy()
    df["order_id"] = df["order_id"].map(lambda value: clean_text(value).upper())
    df["order_date"] = df["order_date"].map(parse_date)
    df["customer"] = df["customer"].map(lambda value: clean_text(value).title())
    df["email"] = df["email"].map(lambda value: clean_text(value).lower())
    df["product"] = df["product"].map(lambda value: clean_text(value).title())
    df["region"] = df["region"].map(lambda value: clean_text(value).title())
    df["status"] = df["status"].map(lambda value: clean_text(value).lower())
    df["notes"] = df["notes"].map(clean_text)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = df["unit_price"].map(parse_money)

    df["email_valid"] = df["email"].map(lambda value: bool(EMAIL_RE.match(value)))
    df["status_clean"] = df["status"].map(lambda value: STATUS_MAP.get(value, "unknown"))
    df["quantity_valid"] = df["quantity"].notna() & (df["quantity"] > 0)
    df["price_valid"] = df["unit_price"].notna() & (df["unit_price"] >= 0)
    df["date_valid"] = df["order_date"].notna()

    df = df.drop_duplicates(subset=[column for column in raw.columns], keep="first").copy()
    duplicates_removed = rows_before - len(df)

    df["data_quality_flag"] = df.apply(
        lambda row: "; ".join([
            flag for flag in [
                "" if row["date_valid"] else "missing or invalid date",
                "" if row["email_valid"] else "missing or invalid email",
                "" if row["quantity_valid"] else "invalid quantity",
                "" if row["price_valid"] else "invalid price",
                "" if row["status_clean"] != "unknown" else "unknown status",
                "" if row["customer"] else "missing customer",
            ] if flag
        ]) or "ok",
        axis=1,
    )
    df["revenue"] = (df["quantity"].fillna(0) * df["unit_price"].fillna(0)).round(2)
    df.loc[~df["quantity_valid"], "revenue"] = 0
    df.loc[~df["price_valid"], "revenue"] = 0
    df.loc[df["status_clean"].isin(["refunded", "cancelled"]), "revenue"] = 0
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d").fillna("")

    output_columns = [
        "order_id", "order_date", "customer", "email", "product", "region",
        "quantity", "unit_price", "status_clean", "revenue", "data_quality_flag", "notes",
    ]
    clean = df[output_columns].rename(columns={"status_clean": "status"})
    clean = clean.sort_values(["order_date", "order_id"])

    summary = pd.DataFrame([
        ("Rows before cleanup", rows_before),
        ("Rows after cleanup", len(clean)),
        ("Duplicate rows removed", duplicates_removed),
        ("Missing or invalid dates", int((~df["date_valid"]).sum())),
        ("Missing or invalid emails", int((~df["email_valid"]).sum())),
        ("Invalid quantities", int((~df["quantity_valid"]).sum())),
        ("Invalid prices", int((~df["price_valid"]).sum())),
        ("Unknown statuses", int((df["status_clean"] == "unknown").sum())),
        ("Rows with no quality issues", int((df["data_quality_flag"] == "ok").sum())),
        ("Cleaned revenue", round(float(df["revenue"].sum()), 2)),
    ], columns=["Metric", "Value"])

    clean.to_csv(OUTPUT_DIR / "clean_sales.csv", index=False)
    with pd.ExcelWriter(OUTPUT_DIR / "clean_sales.xlsx", engine="openpyxl") as writer:
        clean.to_excel(writer, sheet_name="Clean Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    issue_counts = {
        "Duplicates": duplicates_removed,
        "Bad dates": int((~df["date_valid"]).sum()),
        "Bad emails": int((~df["email_valid"]).sum()),
        "Bad quantities": int((~df["quantity_valid"]).sum()),
        "Bad prices": int((~df["price_valid"]).sum()),
        "Unknown status": int((df["status_clean"] == "unknown").sum()),
    }
    fig, ax = plt.subplots(figsize=(9, 4.8))
    labels = list(issue_counts)
    values = list(issue_counts.values())
    bars = ax.bar(labels, values, color=["#0f766e", "#f97316", "#dc2626", "#7c3aed", "#2563eb", "#0891b2"])
    ax.set_title("Issues found and fixed in the sample dataset")
    ax.set_ylabel("Rows affected")
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, padding=2)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    fig.savefig(ASSETS_DIR / "cleanup_quality.png", dpi=160)
    plt.close(fig)

    def display_value(metric: str, value: object) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if metric == "Cleaned revenue":
            return f"{float(value):,.2f}"
        return str(value)

    summary_lines = [
        "# Data cleanup summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    summary_lines += [
        f"| {metric} | {display_value(metric, value)} |"
        for metric, value in summary.itertuples(index=False)
    ]
    summary_lines += [
        "",
        "## What changed",
        "",
        "- Duplicate rows were removed.",
        "- Dates were normalized to YYYY-MM-DD and invalid dates were flagged.",
        "- Emails were lowercased and checked for valid formatting.",
        "- Quantities and prices were converted to numbers; invalid values were flagged.",
        "- Status values were mapped to a consistent set.",
        "- Revenue was calculated only for valid, non-refunded, non-cancelled rows.",
        "",
        "## Files",
        "",
        "- `output/clean_sales.csv`",
        "- `output/clean_sales.xlsx`",
        "- `output/cleanup_summary.md`",
        "- `../assets/cleanup_quality.png`",
    ]
    (OUTPUT_DIR / "cleanup_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
