from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT / "samples"
PRODUCTS = ["Analytics Setup", "Automation Sprint", "Data Cleanup", "Monthly Report", "Dashboard Build"]
REGIONS = ["Lagos", "Abuja", "Remote", "Accra", "Nairobi"]
CHANNELS = ["referral", "marketplace", "direct", "social"]
CUSTOMER_TYPES = ["small business", "agency", "freelancer", "e-commerce"]


def main() -> None:
    random.seed(46)
    SAMPLES.mkdir(parents=True, exist_ok=True)
    start = date(2026, 1, 1)
    for month in range(3):
        rows = []
        month_start = start.replace(month=month + 1)
        for index in range(90):
            order_date = month_start + timedelta(days=random.randrange(0, 28))
            product = random.choice(PRODUCTS)
            region = random.choice(REGIONS)
            channel = random.choice(CHANNELS)
            customer_type = random.choice(CUSTOMER_TYPES)
            units = random.randint(1, 4)
            unit_price = round(random.uniform(25, 220), 2)
            units_text = "" if index % 21 == 0 else str(units)
            price_text = "" if index % 27 == 0 else f"{unit_price:.2f}"
            rows.append({
                "date": order_date.isoformat(),
                "product": product,
                "region": region,
                "channel": channel,
                "customer_type": customer_type,
                "units": units_text,
                "unit_price": price_text,
            })
        for row in random.sample(rows, 4):
            rows.append(dict(row))
        output = SAMPLES / f"sales_{month_start:%Y-%m}.csv"
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
