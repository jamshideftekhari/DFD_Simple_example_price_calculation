"""
Stage 1 - Order Price Calculator  (traditional-approach prototype)

Each function corresponds to one process on the Level-1 DFD:
    process_1_order_value   -> Process 1: Compute order value
    process_2_discount      -> Process 2: Apply discount
    process_3_vat           -> Process 3: Apply VAT / moms
    process_4_priced_order  -> Process 4: Produce priced order

The two reference tables (DISCOUNT_BRACKETS, COUNTRY_VAT) are the DFD
data stores D1 Discount_Bracket and D2 Country.
"""

from dataclasses import dataclass, asdict


# --------------------------------------------------------------------------- #
#  Data stores (reference tables)                                             #
# --------------------------------------------------------------------------- #

# D1 - Discount_Bracket : (minimum order value inclusive, discount rate)
#      Highest bracket whose minimum is <= order_value wins.
DISCOUNT_BRACKETS = [
    (0,      0.00),
    (1_000,  0.03),
    (5_000,  0.05),
    (7_000,  0.07),
    (10_000, 0.10),
    (50_000, 0.15),
]

# D2 - Country : country_code -> (country_name, vat_rate)
COUNTRY_VAT = {
    "DK": ("Denmark",     0.25),
    "BE": ("Belgium",     0.21),
    "DE": ("Germany",     0.19),
    "NL": ("Netherlands", 0.21),
    "FR": ("France",      0.20),
}


# --------------------------------------------------------------------------- #
#  Result structure (the "priced_order" data flow / D3 Order record)          #
# --------------------------------------------------------------------------- #

@dataclass
class PricedOrder:
    number_of_items:  int
    unit_price:       float
    country_code:     str
    order_date:       str        # Stage 2 only
    order_value:      float
    discount_rate:    float
    discount_amount:  float
    discounted_value: float
    vat_rate:         float
    vat_amount:       float
    order_total:      float


# --------------------------------------------------------------------------- #
#  Processes                                                                   #
# --------------------------------------------------------------------------- #

def process_1_order_value(number_of_items: int, unit_price: float) -> float:
    """Process 1: order_value = number_of_items * unit_price."""
    if number_of_items < 1:
        raise ValueError("number_of_items must be >= 1")
    if unit_price < 0:
        raise ValueError("unit_price must be >= 0")
    return number_of_items * unit_price


def lookup_discount_rate(order_value: float) -> float:
    """Read D1: highest bracket whose minimum is <= order_value."""
    rate = 0.0
    for minimum, bracket_rate in DISCOUNT_BRACKETS:
        if order_value >= minimum:
            rate = bracket_rate
        else:
            break
    return rate


def process_2_discount(order_value: float):
    """Process 2: apply the value-based discount."""
    discount_rate = lookup_discount_rate(order_value)
    discount_amount = order_value * discount_rate
    discounted_value = order_value - discount_amount
    return discount_rate, discount_amount, discounted_value


def process_3_vat(discounted_value: float, country_code: str):
    """Process 3: add country VAT/moms on the discounted value."""
    code = country_code.upper()
    if code not in COUNTRY_VAT:
        raise ValueError(
            f"Unknown country code {country_code!r}. "
            f"Known: {', '.join(sorted(COUNTRY_VAT))}"
        )
    _name, vat_rate = COUNTRY_VAT[code]
    vat_amount = discounted_value * vat_rate
    return vat_rate, vat_amount


def process_4_priced_order(number_of_items, unit_price, country_code,
                           order_date="") -> PricedOrder:
    """Process 4: orchestrate 1->2->3 and produce the priced order."""
    order_value = process_1_order_value(number_of_items, unit_price)
    discount_rate, discount_amount, discounted_value = process_2_discount(order_value)
    vat_rate, vat_amount = process_3_vat(discounted_value, country_code)
    order_total = discounted_value + vat_amount

    return PricedOrder(
        number_of_items=number_of_items,
        unit_price=round(unit_price, 2),
        country_code=country_code.upper(),
        order_date=order_date,
        order_value=round(order_value, 2),
        discount_rate=discount_rate,
        discount_amount=round(discount_amount, 2),
        discounted_value=round(discounted_value, 2),
        vat_rate=vat_rate,
        vat_amount=round(vat_amount, 2),
        order_total=round(order_total, 2),
    )


# The "one-line calculator" the assignment asks for:
def calculate_order_total(number_of_items, unit_price, country_code):
    """One-line total, for quick use / spreadsheet cells."""
    return process_4_priced_order(number_of_items, unit_price, country_code).order_total


# --------------------------------------------------------------------------- #
#  Presentation (a receipt) + interactive entry                               #
# --------------------------------------------------------------------------- #

def format_receipt(o: PricedOrder) -> str:
    name = COUNTRY_VAT[o.country_code][0]
    lines = [
        "-------------------------------------------",
        "            ORDER PRICE RECEIPT            ",
        "-------------------------------------------",
        f" Items x Unit price : {o.number_of_items} x {o.unit_price:,.2f}",
        f" Country            : {o.country_code} ({name})",
    ]
    if o.order_date:
        lines.append(f" Date               : {o.order_date}")
    lines += [
        "-------------------------------------------",
        f" Order value        : {o.order_value:>12,.2f}",
        f" Discount ({o.discount_rate*100:>4.1f}%)   : {-o.discount_amount:>12,.2f}",
        f" Discounted value   : {o.discounted_value:>12,.2f}",
        f" VAT/moms ({o.vat_rate*100:>4.1f}%)   : {o.vat_amount:>12,.2f}",
        "-------------------------------------------",
        f" ORDER TOTAL        : {o.order_total:>12,.2f}",
        "-------------------------------------------",
    ]
    return "\n".join(lines)


def run_demo():
    print("### Sample calculations ###\n")
    samples = [
        (5,   150.00, "DK", "2026-01-15"),   # 750  -> no discount, 25% VAT
        (10,  600.00, "DE", "2026-02-03"),   # 6000 -> 5% discount, 19% VAT
        (100, 120.00, "FR", "2026-03-20"),   # 12000-> 10% discount, 20% VAT
        (200, 300.00, "NL", "2026-04-11"),   # 60000-> 15% discount, 21% VAT
    ]
    for n, p, c, d in samples:
        print(format_receipt(process_4_priced_order(n, p, c, d)))
        print()


def run_interactive():
    print("### Enter an order ###")
    n = int(input("Number of items      : "))
    p = float(input("Unit price           : "))
    c = input("Country code (DK/BE/DE/NL/FR): ").strip()
    d = input("Date (YYYY-MM-DD, optional)  : ").strip()
    print()
    print(format_receipt(process_4_priced_order(n, p, c, d)))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive()
    else:
        run_demo()
