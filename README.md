# DOUBLEDOGE Arbitrage Trading System

## System Overview

This projects implement an arbitrage system for $DOUBLEDOGE between Binance and Coinbase. The system first simulates price movements then calculates optimal trade sizes and then executes trades.

## Symulation Results

## Task Questions

## Key Metrics to Monitor

- Daily profit
- trade count
- asset distribution
- price volatility
- loan utilization
- Sharpe ratio

Ways to improve the system:

- Implement machine learning for price prediction
- optimize trade timing
- dynamic loan utilization

## Code Structure

The project is organized into the following main components:

- `main.py`: Entry point of the application, orchestrates the simulation and analysis.
- `src/`:
  - `constants.py`: Contains all constant values used throughout the project.
  - `price_simulation.py`: Implements the price simulation logic.
  - `trading_simulation.py`: Contains the main trading logic and simulation.
  - `optimal_balance.py`: Calculates optimal asset balances.
  - `balance_threshold.py`: Determines balance thresholds for transfers.
  - `trade_metrics.py`: Calculates various trading performance metrics.
  - `calculate_volume.py`: Computes trading volumes for each exchange.
  - `volatility.py`: Calculates price volatility for risk management.
  