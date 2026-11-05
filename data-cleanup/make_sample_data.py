from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "messy_sales.csv"

PRODUCTS = [
    "Wireless Mouse",
    "USB-C Hub",
    "Laptop Stand",
    "Mechanical Keyboard",
    "Noise Cancelling Headphones",
    "Webcam",
    "Monitor Light",
    "Desk Mat",
]
REGIONS = ["north", "South", " EAST ", "west", "North "]
STATUSES = ["paid", "PAID", "Pending", "pending", "refunded", "Refunded", "cancelled"]
CUSTOMERS = [
    ("Ada Okafor", "ada.okafor@example.com"),
    ("john mensah", "JOHN.MENSAH@EXAMPLE.COM"),
    ("Grace Bello", "grace.bello@example"),
    ("Ibrahim Musa", "ibrahim.musa@example.com"),
    ("Ngozi Eze", "ngozi.eze@example.com"),
    ("Samuel Adeyemi", "samuel.adeyemi@example.com"),
    ("Fatima Bello", "fatima.bello@example.com"),
    ("Chinedu Obi", "chinedu.obi@example.com"),
    ("", ""),
    ("Amina Yusuf", "amina.yusuf@example.com"),
]


def messy_date(value: date, index: int) -> str:
    if index % 17 == 0:
        return ""
    if index % 5 == 0:
        return value.strftime("%d/%m/%Y")
    if index % 7 == 0:
        return value.strftime("%b %d, %Y")
    return value.isoformat()


def messy_price(value: float, index: int) -> str:
    if index % 19 == 0:
        return ""
    if index % 4 == 0:
        return f"${value:,.2f}"
    if index % 6 == 0:
        return f"USD {value:.2f}"
    return f"{value:.2f}"


def messy_quantity(value: int, index: int) -> str:
    if index % 23 == 0:
        return ""
    if index % 8 == 0:
        return f" {value} "
    if index % 31 == 0:
        return "-1"
    return str(value)


def main() -> None:
    random.seed(46)
    start = date(2026, 1, 1)
    rows: list[dict[str, str]] = []
    for index in range(320):
        product = random.choice(PRODUCTS)
        region = random.choice(REGIONS)
        status = random.choice(STATUSES)
        customer, email = random.choice(CUSTOMERS)
        ordered = start + timedelta(days=random.randrange(0, 120))
        quantity = random.randint(1, 6)
        unit_price = round(random.uniform(12, 240), 2)
        if index % 11 == 0:
            product = f"  {product} "
        if index % 13 == 0:
            customer = customer.upper()
        if index % 29 == 0:
            email = email.replace("@", " at ") if email else ""
        rows.append({
            "order_id": f" ord-{1000 + index} ",
            "order_date": messy_date(ordered, index),
            "customer": customer,
            "email": email,
            "product": product,
            "region": region,
            "quantity": messy_quantity(quantity, index),
            "unit_price": messy_price(unit_price, index),
            "status": status,
            "notes": " priority " if index % 9 == 0 else "",
        })

    for row in random.sample(rows, 24):
        rows.append(dict(row))

    random.shuffle(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} messy rows to {OUTPUT}")


if __name__ == "__main__":
    main()
