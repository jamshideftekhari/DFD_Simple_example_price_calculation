"""
Stage 2 - Process 5: Generate order history

Simulates a year of orders spread across different months and different
countries, pricing each one with the Stage 1 processes (1-4), and writes
the result to sales_history.csv - the "spreadsheet" that stands in for the
D3 Order data store.

See Stage2_Design.md, section 3-4, process 5.
"""

import csv
import random
from pathlib import Path

from price_calculator import process_4_priced_order, COUNTRY_VAT

OUTPUT_CSV = Path(__file__).parent / "sales_history.csv"

MONTHS_2025 = [f"2025-{m:02d}" for m in range(1, 13)]
COUNTRY_CODES = list(COUNTRY_VAT.keys())

FIELDNAMES = [
    "order_id", "order_date", "country_code", "number_of_items", "unit_price",
    "order_value", "discount_rate", "discount_amount", "discounted_value",
    "vat_rate", "vat_amount", "order_total",
]


def random_order_date(month_prefix: str) -> str:
    day = random.randint(1, 28)
    return f"{month_prefix}-{day:02d}"


def generate_orders(orders_per_month: int = 10, seed: int = 42):
    """Return a list of order-record dicts (one per simulated order)."""
    random.seed(seed)
    orders = []
    order_id = 1
    for month_prefix in MONTHS_2025:
        for _ in range(orders_per_month):
            country = random.choice(COUNTRY_CODES)
            number_of_items = random.randint(1, 400)
            unit_price = round(random.uniform(10, 300), 2)
            order_date = random_order_date(month_prefix)

            priced = process_4_priced_order(number_of_items, unit_price, country, order_date)

            orders.append({
                "order_id": order_id,
                "order_date": priced.order_date,
                "country_code": priced.country_code,
                "number_of_items": priced.number_of_items,
                "unit_price": priced.unit_price,
                "order_value": priced.order_value,
                "discount_rate": priced.discount_rate,
                "discount_amount": priced.discount_amount,
                "discounted_value": priced.discounted_value,
                "vat_rate": priced.vat_rate,
                "vat_amount": priced.vat_amount,
                "order_total": priced.order_total,
            })
            order_id += 1
    return orders


def write_csv(orders, path: Path = OUTPUT_CSV) -> Path:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(orders)
    return path


if __name__ == "__main__":
    generated = generate_orders()
    csv_path = write_csv(generated)
    print(f"Wrote {len(generated)} orders to {csv_path}")
