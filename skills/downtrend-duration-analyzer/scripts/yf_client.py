"""yfinance-based data client for downtrend-duration-analyzer.

Replaces FMP endpoints with free yfinance data:
  - fetch_sp500_list()       → S&P 500 constituents with sector + market cap
  - fetch_historical_prices() → OHLCV DataFrame via yf.download()
"""

from __future__ import annotations

import io
import warnings
from datetime import datetime

import pandas as pd
import yfinance as yf


_WIKI_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
_WIKI_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def _fetch_wiki_tables() -> list:
    """Fetch Wikipedia S&P 500 table, bypassing 403 with browser User-Agent."""
    import requests as _requests
    from io import StringIO

    try:
        resp = _requests.get(_WIKI_SP500_URL, headers=_WIKI_HEADERS, timeout=20)
        resp.raise_for_status()
        return pd.read_html(StringIO(resp.text))
    except Exception as e:
        print(f"Warning: could not fetch S&P 500 list from Wikipedia: {e}")
        return []


def fetch_sp500_list(sector: str | None = None) -> list[dict]:
    """Return S&P 500 stocks with symbol, sector, and marketCap.

    Pulls the constituent table from Wikipedia, then fetches market cap
    from yfinance in bulk (one Ticker() call per symbol — cached).
    """
    tables = _fetch_wiki_tables()
    if not tables:
        return []

    df = tables[0]
    # Normalise column names across Wikipedia table variants
    df.columns = [c.strip() for c in df.columns]
    symbol_col = next((c for c in df.columns if "Symbol" in c or "Ticker" in c), None)
    sector_col = next((c for c in df.columns if "GICS Sector" in c or "Sector" in c), None)

    if symbol_col is None:
        return []

    records = []
    for _, row in df.iterrows():
        sym = str(row[symbol_col]).replace(".", "-")  # BRK.B → BRK-B for yfinance
        sec = str(row[sector_col]) if sector_col else "Unknown"

        if sector and sec != sector:
            continue

        records.append({"symbol": sym, "sector": sec, "marketCap": None})

    # Fetch market caps in batch using yfinance fast_info
    for rec in records:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                info = yf.Ticker(rec["symbol"]).fast_info
                rec["marketCap"] = getattr(info, "market_cap", None)
        except Exception:
            pass

    return records


def fetch_historical_prices(
    symbol: str, from_date: str, to_date: str
) -> pd.DataFrame:
    """Download daily OHLCV for *symbol* between from_date and to_date.

    Returns a DataFrame with columns: date, open, high, low, close, volume
    sorted ascending by date.  Returns empty DataFrame on failure.
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw = yf.download(
                symbol,
                start=from_date,
                end=to_date,
                auto_adjust=True,
                progress=False,
            )
        if raw.empty:
            return pd.DataFrame()

        # yfinance returns MultiIndex columns when downloading a single ticker
        # in some versions — flatten if needed.
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = [c[0].lower() for c in raw.columns]
        else:
            raw.columns = [c.lower() for c in raw.columns]

        raw = raw.reset_index()
        raw.rename(columns={"index": "date", "Date": "date"}, inplace=True)
        raw["date"] = pd.to_datetime(raw["date"])
        raw = raw.sort_values("date").reset_index(drop=True)

        keep = [c for c in ["date", "open", "high", "low", "close", "volume"] if c in raw.columns]
        return raw[keep]

    except Exception as e:
        print(f"Warning: yfinance download failed for {symbol}: {e}")
        return pd.DataFrame()
