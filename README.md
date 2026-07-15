# ForeignExchangeData

EUR/USD OHLCV data, 2-minute bars, for 2025 (January–December).

## Structure

- `data/EURUSDT_2T_2025-MM.csv` — one file per month, 2-minute interval bars.
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

## Visualization

```bash
pip install -r requirements.txt
python scripts/visualize.py 2025-01
python scripts/visualize.py --all
```
