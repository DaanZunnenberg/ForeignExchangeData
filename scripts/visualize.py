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

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def plot(df, title: str) -> None:
    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1, sharex=True, figsize=(12, 6), gridspec_kw={"height_ratios": [3, 1]}
    )

    ax_price.plot(df.index, df["close"], linewidth=0.9, color="tab:blue", label="Close")
    if "high" in df.columns and "low" in df.columns:
        ax_price.fill_between(df.index, df["low"], df["high"], color="tab:blue", alpha=0.15, label="High/Low range")
        ax_price.legend(loc="upper left")
    ax_price.set_ylabel("Price")
    ax_price.set_title(title)
    ax_price.grid(True, alpha=0.3)

    colors = ["tab:green" if c >= o else "tab:red" for o, c in zip(df["open"], df["close"])] if "open" in df.columns else "tab:gray"
    ax_volume.bar(df.index, df["volume"], color=colors, width=1.0)
    ax_volume.set_yscale("log")
    ax_volume.set_ylabel("Volume (log)")
    ax_volume.set_xlabel("Datetime")
    ax_volume.grid(True, alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("months", nargs="*", help="Months to plot, e.g. 2025-01")
        parser.add_argument("--all", action="store_true", help="Plot all available months")
        parser.add_argument(
            "--resample", default="1h", help="Resample to a new interval, e.g. 5min, 1h, 1D (default: 1h)"
        )
        args = parser.parse_args()
        print(args)

        months = available_months() if args.all else args.months
        if not months:
            parser.error("Provide one or more months, or use --all")
    
    except SystemExit as e:
        args = Namespace(months=[], all=True, resample="1h")
        months = available_months() if args.all else args.months
    
    df = load_months(months)
    if args.resample:
        df = resample(df, args.resample)



    plot(df, f"EUR/USD {', '.join(months)}")


if __name__ == "__main__":
    main()

