Overview
SQLAlchemy FollowTrend is a Python application I built to analyze and follow financial market trends using SQLAlchemy as the ORM for database interactions. It queries historical price data (e.g., stocks or crypto) from PostgreSQL/MySQL, applies trend-following indicators (like moving averages or MACD), and generates buy/sell signals for automated trading strategies. This project demonstrates my expertise in database design, ORM querying, data pipelines, and algorithmic analysis—ideal for fintech apps or backtesting systems.
Disclaimer: For educational purposes only. Trading involves risks; backtest thoroughly and not for financial advice.
Features

Database Integration: SQLAlchemy models for storing OHLCV (Open, High, Low, Close, Volume) data and trend signals.
Trend Analysis: Computes indicators (e.g., SMA, EMA, RSI) and detects uptrends/downtrends with SQL queries or Pandas integration.
Signal Generation: Rule-based alerts (e.g., golden cross) with configurable thresholds.
Backtesting Engine: Simulate strategies on historical data to evaluate performance (e.g., Sharpe ratio).
CLI Dashboard: Interactive queries for trend visualization and export to CSV.
Async Support: Non-blocking DB operations for real-time data feeds.

Tech Stack

Language: Python 3.10+
Key Libraries:

sqlalchemy for ORM and query building.
alembic for migrations.
pandas and numpy for data analysis.
yfinance or ccxt for fetching market data.
click for CLI tools.


Supports PostgreSQL/MySQL; SQLite for local testing.

Getting Started
Prerequisites

Python 3.10 or higher.
A database (e.g., PostgreSQL) and connection details.
Git for cloning.

Installation

Clone the repository:
bashgit clone https://github.com/abd0o0/sqlalchemy-followtrend.git
cd sqlalchemy-followtrend

Create a virtual environment and install dependencies:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Set up environment variables (create .env in the root):
textDATABASE_URL=postgresql://user:pass@localhost:5432/trend_db
YFINANCE_SYMBOL=AAPL  # Default stock for testing


Usage

Initialize Database (Run migrations):
bashalembic upgrade head

Fetch and Store Data via CLI:
bashpython trend_cli.py fetch --symbol AAPL --period 1y
This pulls 1 year of data and inserts it into the DB.
Analyze Trends (Generate Signals):
bashpython trend_cli.py analyze --symbol AAPL --indicator sma --window 50
Outputs trend signals (e.g., "Buy: Golden Cross at 2025-09-01").
Programmatic Use (in a Python script):
pythonfrom sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import PriceData, TrendSignal
from analyzer import TrendAnalyzer

# Setup DB
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

# Analyze
analyzer = TrendAnalyzer(session)
signals = analyzer.compute_signals('AAPL', window=20)

# Query signals
recent = session.query(TrendSignal).filter_by(symbol='AAPL').order_by(TrendSignal.date.desc()).limit(5).all()
for signal in recent:
    print(f"{signal.date}: {signal.action} at {signal.price}")

session.close()

Backtest Strategy:
bashpython trend_cli.py backtest --symbol TSLA --start 2024-01-01 --end 2025-09-26 --strategy sma_crossover
Outputs metrics like ROI and win rate.

Run python trend_cli.py --help for all commands. Examples in /examples folder; migration scripts in /alembic.
