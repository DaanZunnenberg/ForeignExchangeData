#!/usr/bin/env python3
"""Plot EUR/USD OHLCV data from the data/ folder.

Usage:
    python scripts/visualize.py 2025-01 [2025-02 ...]
    python scripts/visualize.py --all
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_month(month: str) -> pd.DataFrame:
    path = DATA_DIR / f"EURUSDT_2T_{month}.csv"
    if not path.exists():
        sys.exit(f"No data file found for {month}: {path}")
    df = pd.read_csv(path, parse_dates=["datetime"])
    return df


def plot(df: pd.DataFrame, title: str) -> None:
    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1, sharex=True, figsize=(12, 6), gridspec_kw={"height_ratios": [3, 1]}
    )
    ax_price.plot(df["datetime"], df["close"], linewidth=0.8)
    ax_price.set_ylabel("Close price")
    ax_price.set_title(title)

    ax_volume.bar(df["datetime"], df["volume"], width=0.001)
    ax_volume.set_ylabel("Volume")
    ax_volume.set_xlabel("Datetime")

    fig.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("months", nargs="*", help="Months to plot, e.g. 2025-01")
    parser.add_argument("--all", action="store_true", help="Plot all available months")
    args = parser.parse_args()

    if args.all:
        months = sorted(p.stem.replace("EURUSDT_2T_", "") for p in DATA_DIR.glob("EURUSDT_2T_*.csv"))
    else:
        months = args.months

    if not months:
        parser.error("Provide one or more months, or use --all")

    frames = [load_month(m) for m in months]
    df = pd.concat(frames, ignore_index=True).sort_values("datetime")
    plot(df, f"EUR/USD {', '.join(months)}")


if __name__ == "__main__":
    main()
