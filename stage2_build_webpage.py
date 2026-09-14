"""
Stage 2 - Process 8: Publish web presentation

Builds a single static HTML page (index.html) for the sponsors: the
pricing formula, a sample input/output, the sales history, and the two
histogram charts produced by stage2_reports.py.

See Stage2_Design.md, section 3-4, process 8.
"""

from pathlib import Path

from price_calculator import process_4_priced_order, format_receipt
from stage2_reports import load_orders

OUTPUT_HTML = Path(__file__).parent / "index.html"

SAMPLE = dict(number_of_items=10, unit_price=600.00, country_code="DE", order_date="2026-02-03")

FORMULA = """order_value      = number_of_items * unit_price
discount_rate    = lookup(order_value)          # tiered bracket, 0-15%
discounted_value = order_value * (1 - discount_rate)
vat_rate         = lookup(country_code)          # DK 25%, BE 21%, DE 19%, NL 21%, FR 20%
vat_amount       = discounted_value * vat_rate
order_total      = discounted_value + vat_amount"""


def build_sample_block() -> str:
    priced = process_4_priced_order(**SAMPLE)
    receipt = format_receipt(priced)
    return f"""
    <h2>Sample input / output</h2>
    <p><strong>Input:</strong> number_of_items={SAMPLE['number_of_items']},
       unit_price={SAMPLE['unit_price']}, country_code={SAMPLE['country_code']},
       order_date={SAMPLE['order_date']}</p>
    <pre>{receipt}</pre>
    """


def build_history_table(limit: int = 25) -> str:
    df = load_orders()
    table_df = df.sort_values("order_date").head(limit).drop(columns=["month"])
    table_html = table_df.to_html(index=False, float_format=lambda v: f"{v:,.2f}")
    return f"""
    <h2>Sales history ({limit} of {len(df)} orders shown)</h2>
    {table_html}
    """


def build_page() -> str:
    sample_html = build_sample_block()
    history_html = build_history_table()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Order Price Calculator - Sponsor Presentation</title>
<style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 2rem auto; max-width: 900px; color: #222; }}
    h1 {{ border-bottom: 3px solid #4C72B0; padding-bottom: .3rem; }}
    h2 {{ color: #4C72B0; margin-top: 2rem; }}
    pre {{ background: #f4f4f4; padding: 1rem; border-radius: 6px; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; font-size: .85rem; }}
    th, td {{ border: 1px solid #ddd; padding: 4px 8px; text-align: right; }}
    th {{ background: #4C72B0; color: white; }}
    img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 6px; margin-top: .5rem; }}
    code {{ background: #eee; padding: 1px 5px; border-radius: 3px; }}
</style>
</head>
<body>
    <h1>Order Price Calculator &mdash; Stage 1 &amp; Stage 2 Prototype</h1>
    <p>This page presents the order price calculator (Stage 1) and the
       resulting sales history and reports (Stage 2), built using the
       traditional structured-analysis approach (context diagram, DFD,
       ERD) documented in <code>Stage1_Design.md</code> and
       <code>Stage2_Design.md</code>.</p>

    <h2>Formula</h2>
    <pre>{FORMULA}</pre>

    {sample_html}

    {history_html}

    <h2>Sales results by country (state)</h2>
    <img src="report_by_country.png" alt="Sales by country">

    <h2>Sales results by month</h2>
    <img src="report_by_month.png" alt="Sales by month">

</body>
</html>
"""


def main():
    html = build_page()
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
