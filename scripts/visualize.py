#!/usr/bin/env python3
"""Plot EUR/USD OHLCV data from the data/ folder.

Usage:
    python scripts/visualize.py 2025-01 [2025-02 ...]
    python scripts/visualize.py --all
    python scripts/visualize.py --all --resample 1h
"""

import argparse

import matplotlib.pyplot as plt

from data_tools import available_months, load_months, resample


def plot(df, title: str) -> None:
    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1, sharex=True, figsize=(12, 6), gridspec_kw={"height_ratios": [3, 1]}
    )
    ax_price.plot(df.index, df["close"], linewidth=0.8)
    ax_price.set_ylabel("Close price")
    ax_price.set_title(title)

    ax_volume.bar(df.index, df["volume"], width=0.001)
    ax_volume.set_ylabel("Volume")
    ax_volume.set_xlabel("Datetime")

    fig.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("months", nargs="*", help="Months to plot, e.g. 2025-01")
    parser.add_argument("--all", action="store_true", help="Plot all available months")
    parser.add_argument("--resample", help="Resample to a new interval, e.g. 5min, 1h, 1D")
    args = parser.parse_args()

    months = available_months() if args.all else args.months
    if not months:
        parser.error("Provide one or more months, or use --all")

    df = load_months(months)
    if args.resample:
        df = resample(df, args.resample)

    plot(df, f"EUR/USD {', '.join(months)}")


if __name__ == "__main__":
    main()
