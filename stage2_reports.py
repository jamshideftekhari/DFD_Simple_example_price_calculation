"""
Stage 2 - Processes 6 & 7: Sales histogram reports

Reads the D3 Order data store (sales_history.csv) and produces two
histogram reports:
    report_by_country.png  - total sales by country ("state")
    report_by_month.png    - total sales by month

See Stage2_Design.md, section 3-4, processes 6 and 7.
"""

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no GUI needed - just save PNG files
import matplotlib.pyplot as plt

CSV_PATH = Path(__file__).parent / "sales_history.csv"
COUNTRY_CHART = Path(__file__).parent / "report_by_country.png"
MONTH_CHART = Path(__file__).parent / "report_by_month.png"


def load_orders(path: Path = CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    return df


def sales_by_country(df: pd.DataFrame) -> pd.Series:
    """Process 6: total order_total grouped by country_code."""
    return df.groupby("country_code")["order_total"].sum().sort_values(ascending=False)


def sales_by_month(df: pd.DataFrame) -> pd.Series:
    """Process 7: total order_total grouped by calendar month."""
    return df.groupby("month")["order_total"].sum().sort_index()


def plot_histogram(series: pd.Series, title: str, xlabel: str, out_path: Path, color: str):
    fig, ax = plt.subplots(figsize=(8, 5))
    series.plot(kind="bar", ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Total sales (order total)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main():
    df = load_orders()

    by_country = sales_by_country(df)
    by_month = sales_by_month(df)

    plot_histogram(by_country, "Sales results by country (state)", "Country",
                    COUNTRY_CHART, "#4C72B0")
    plot_histogram(by_month, "Sales results by month", "Month",
                    MONTH_CHART, "#55A868")

    print("Sales by country:\n", by_country, "\n")
    print("Sales by month:\n", by_month, "\n")
    print(f"Saved {COUNTRY_CHART.name} and {MONTH_CHART.name}")

    return df, by_country, by_month


if __name__ == "__main__":
    main()
