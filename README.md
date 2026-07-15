# ForeignExchangeData

EUR/USD Open, High, Low, Close, Volume (OHLCV) data, 2-minute bars, for 2025 (January–December).

> **This is a test/sandbox repository.** It exists purely for people to play around with sample FX data and try out trading strategies, backtests, and analysis techniques. The data is provided as-is with no guarantees of accuracy or completeness — do not use it for real trading decisions. No rights reserved: use, copy, modify, and share this data and code freely for any purpose.

## Structure

- `data/eurusd_2m_2025-MM.csv` — one file per month, 2-minute interval bars.
- `scripts/data_tools.py` — load, combine, and resample the data files.
- `scripts/visualize.py` — plot price and volume for one or more months.

## Columns

| Column | Description |
|---|---|
| `datetime` | Bar timestamp (UTC) |
| `open` | Opening price |
| `high` | High price |
| `low` | Low price |
| `close` | Closing price |
| `volume` | Traded volume |
| `trade_count` | Number of trades |

## Data tools

```python
from scripts.data_tools import load_months, load_all, resample

df = load_months(["2025-01", "2025-02"])  # combine specific months
df = load_all()                           # combine all available months
hourly = resample(df, "1h")                # resample to any pandas offset alias
```

## Visualization

```bash
pip install -r requirements.txt
python scripts/visualize.py 2025-01
python scripts/visualize.py --all
python scripts/visualize.py --all --resample 1h
```
