"""Load, combine, and resample EUR/USD OHLCV data from the data/ folder."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

OHLC_AGG = {
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum",
    "trade_count": "sum",
}


def available_months() -> list[str]:
    """Return the sorted list of months (e.g. '2025-01') present in data/."""
    return sorted(p.stem.replace("eurusd_2m_", "") for p in DATA_DIR.glob("eurusd_2m_*.csv"))


def load_month(month: str) -> pd.DataFrame:
    """Load a single month's CSV as a DataFrame indexed by datetime."""
    path = DATA_DIR / f"eurusd_2m_{month}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No data file found for {month}: {path}")
    df = pd.read_csv(path, parse_dates=["datetime"])
    return df.set_index("datetime").sort_index()


def load_months(months: list[str]) -> pd.DataFrame:
    """Load and combine multiple months into a single sorted DataFrame."""
    if not months:
        raise ValueError("load_months requires at least one month")
    frames = [load_month(m) for m in months]
    df = pd.concat(frames).sort_index()
    return df[~df.index.duplicated(keep="first")]


def load_all() -> pd.DataFrame:
    """Load and combine every month found in data/."""
    return load_months(available_months())


def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample OHLCV data to a new bar interval, e.g. '5min', '1h', '1D'."""
    agg = {col: how for col, how in OHLC_AGG.items() if col in df.columns}
    return df.resample(rule).agg(agg).dropna(how="all")
