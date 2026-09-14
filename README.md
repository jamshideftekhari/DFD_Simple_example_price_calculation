# Order Price Calculator — Traditional Analysis & Design

A small order-pricing system, analyzed with the **traditional (structured)
approach** — context diagram, DFD, ERD — and implemented as a Python
prototype in two stages.

- **Stage 1** — calculate the total price of one order: value-based
  discount, then country VAT/moms on the discounted value.
- **Stage 2** — generate a year of orders across countries and months, and
  produce histogram reports plus a sponsor-facing web page.

See `Assignment.txt` for the original brief and
`Traditional Approach Requirements.pdf` for the modeling method being
followed.

## Requirements

```
python 3.x
pandas
matplotlib
```

## Quick start

```
python price_calculator.py                # Stage 1: sample calculations
python price_calculator.py --interactive  # Stage 1: enter your own order
python stage2_run_all.py                   # Stage 2: full pipeline
```

After `stage2_run_all.py` runs, open `index.html` in a browser to see the
sponsor presentation (formula, sample order, sales history, and both
histograms).

## Formula (Stage 1)

```
order_value      = number_of_items * unit_price
discount_rate     = lookup(order_value)         # tiered bracket, 0-15%
discounted_value  = order_value * (1 - discount_rate)
vat_rate          = lookup(country_code)         # DK 25%, BE 21%, DE 19%, NL 21%, FR 20%
vat_amount        = discounted_value * vat_rate
order_total       = discounted_value + vat_amount
```

Discount is based on **order value**, not item count:

| Order value (≥) | Discount |
|---|---|
| 0 | 0% |
| 1,000 | 3% |
| 5,000 | 5% |
| 7,000 | 7% |
| 10,000 | 10% |
| 50,000 | 15% |

## Design documents

| File | Contents |
|---|---|
| `Stage1_Design.md` | Context diagram, DFD level 1, ERD, data dictionary, process descriptions for the single-order calculator |
| `Stage2_Design.md` | Extends Stage 1 with DFD processes 5–8 (generate history, two histogram reports, web presentation) and the Sponsor/Management external agent |

Read these alongside the code — each Python function is named after the
DFD process it implements.

## Files

**Stage 1**
- `price_calculator.py` — pricing logic (processes 1–4) and a text receipt formatter. Run directly for a demo or `--interactive` mode.

**Stage 2** — run in this order (or all at once via `stage2_run_all.py`)
- `stage2_generate_orders.py` — process 5: simulates 120 orders (10/month × 12 months) across the 5 countries, prices each via `price_calculator.py`, writes `sales_history.csv`
- `stage2_reports.py` — processes 6–7: reads the CSV, groups sales by country and by month, saves `report_by_country.png` and `report_by_month.png`
- `stage2_build_webpage.py` — process 8: assembles `index.html` (formula, sample input/output, sales history table, both charts)
- `stage2_run_all.py` — orchestrates the three scripts above in DFD order

**Generated output** (recreated each run of `stage2_run_all.py`)
- `sales_history.csv` — the D3 Order data store, standing in for a spreadsheet
- `report_by_country.png`, `report_by_month.png` — the two histogram reports
- `index.html` — the sponsor presentation

## Notes / assumptions

- The discount table is read as **tiered brackets** (spend more, save
  more), with 0% below $1,000 — the assignment doesn't state a rate below
  the first threshold.
- The assignment's "different states" is read as **different countries**,
  since `country_code` is the only geographic field in the domain model.
- Stage 2 uses a plain CSV as the "spreadsheet" data store rather than a
  literal `.xlsx` file, to avoid an extra dependency (`openpyxl`) — ask if
  you'd rather have a real Excel workbook with visible formulas.
