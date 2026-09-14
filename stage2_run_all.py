"""
Stage 2 - Orchestrator

Runs the full Stage 2 pipeline in DFD order:
    5 Generate order history -> 6/7 histogram reports -> 8 web presentation
"""

from stage2_generate_orders import generate_orders, write_csv
from stage2_reports import main as build_reports
from stage2_build_webpage import main as build_webpage


def run():
    orders = generate_orders()
    csv_path = write_csv(orders)
    print(f"[5] Generated {len(orders)} orders -> {csv_path}")

    print("[6/7] Building histogram reports...")
    build_reports()

    print("[8] Building web presentation...")
    build_webpage()

    print("\nDone. Open index.html in a browser to view the presentation.")


if __name__ == "__main__":
    run()
