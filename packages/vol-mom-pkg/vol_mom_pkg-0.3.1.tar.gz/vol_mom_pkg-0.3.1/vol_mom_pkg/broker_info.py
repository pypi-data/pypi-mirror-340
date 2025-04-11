import requests
import pandas as pd
from dotenv import load_dotenv
import datetime
import pytz
from .data import get_ohlc_alpaca
# import os

# load_dotenv()
# ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
# ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
# ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

ALPACA_API_KEY = "PKSWP8A9QH87I5DX69Y4"
ALPACA_API_SECRET = "we0Fo1a7UmijE45Z3rWYkZjXqnsfFg3B8pwrnbdC"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET
}

def get_orders(status="all"):
    """Fetch all orders (open, closed, or canceled)."""
    url = f"{ALPACA_BASE_URL}/v2/orders"
    response = requests.get(url, headers=HEADERS, params={"status": status})
    return response.json() if response.status_code == 200 else None

def get_positions():
    """Fetch current portfolio positions."""
    url = f"{ALPACA_BASE_URL}/v2/positions"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def get_account():
    """Fetch account details (including cash balance, buying power, etc.)."""
    url = f"{ALPACA_BASE_URL}/v2/account"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def get_daily_pnl():
    """Fetch PnL details from Alpaca API."""
    account_info = get_account()
    if account_info:
        return {
            "equity": account_info.get("equity"),
            "last_equity": account_info.get("last_equity"),
            "pnl_today": float(account_info.get("equity", 0)) - float(account_info.get("last_equity", 0))
        }
    return None

def get_historical_pnl(start_date=None, end_date=None, timeframe="1D"):
    """Fetch PnL over a custom period from Alpaca API."""
    
    if start_date is None:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    url = f"{ALPACA_BASE_URL}/v2/account/portfolio/history"
    params = {
        "timeframe": timeframe,
        "date_start": start_date, 
        "date_end": end_date 
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching portfolio history: {response.text}")
        return None

    data = response.json()
    if "equity" not in data or not data["equity"]:
        print("No portfolio history found.")
        return None

    # Convert response data into a pandas DataFrame
    history = pd.DataFrame({
        "timestamp": data["timestamp"],
        "equity": data["equity"]
    })

    # Convert timestamps to datetime
    history["date"] = pd.to_datetime(history["timestamp"], unit="s")
    history.set_index("date", inplace=True)

    # Filter data within the date range
    history = history.loc[start_date:end_date]

    if history.empty:
        print("No data available for the given date range.")
        return None

    # Get equity at start and end of the period
    start_equity = history["equity"].iloc[0]
    end_equity = history["equity"].iloc[-1]

    # Calculate PnL
    pnl = end_equity - start_equity
    return {
        "start_equity": start_equity,
        "end_equity": end_equity,
        "pnl": pnl
    }

def get_incremental_pnl(start_date=None, end_date=None, timeframe="1D"):
    """Fetch PnL over a custom period from Alpaca API and return a DataFrame with daily account values and SPY close prices."""
    utc = pytz.utc
    est = pytz.timezone("America/New_York")

    if start_date is None:
        start_date = datetime.datetime.now(est) - datetime.timedelta(days=30)
    else:
        start_date = est.localize(datetime.datetime.strptime(start_date, "%Y-%m-%d"))
    
    if end_date is None:
        end_date = datetime.datetime.now(est)
    else:
        end_date = est.localize(datetime.datetime.strptime(end_date, "%Y-%m-%d"))

    start_date = start_date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    # Convert to ISO 8601 format
    start_date_iso = start_date.strftime("%Y-%m-%dT20:00:00Z")  # 4PM EST (market close in DST)
    end_date_iso = end_date.strftime("%Y-%m-%dT20:00:00Z")

    # Fetch account portfolio history
    url = f"{ALPACA_BASE_URL}/v2/account/portfolio/history"
    params = {
        "start": start_date_iso,
        "end": end_date_iso,
        "timeframe": timeframe
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching portfolio history: {response.text}")
        return None

    data = response.json()
    if "equity" not in data or not data["equity"]:
        print("No portfolio history found.")
        return None

    # Convert response data into a pandas DataFrame
    history = pd.DataFrame({
        "timestamp": data["timestamp"],
        "Account Value": data["equity"]
    })

    # Convert timestamps to datetime
    history["date"] = pd.to_datetime(history["timestamp"], unit="s")
    history.set_index("date", inplace=True)

    # Ensure the index covers all dates within the range
    history = history[['Account Value']]
    history['Daily Chg'] = history['Account Value'] - history['Account Value'].shift(1)

    return history

def get_transactions():
    """Fetch account activities (transactions such as fills, dividends, etc.)."""
    url = f"{ALPACA_BASE_URL}/v2/account/activities"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None