from typing import List
import numpy as np

import src.constants

def calculate_trade_metrics(hourly_profits: List[float], trade_count: int):
    total_profit = sum(hourly_profits)
    winning_trades = sum(1 for profit in hourly_profits if profit > 0)
    losing_trades = trade_count - winning_trades
    win_rate = winning_trades / trade_count if trade_count > 0 else 0
    
    # Calculate daily returns for Sharpe ratio
    daily_profits = [sum(hourly_profits[i:i+24]) for i in range(0, len(hourly_profits), 24)]
    daily_returns = [profit / src.constants.ASSETS_UNDER_MANAGEMENT for profit in daily_profits]
    
    # Calculate Sharpe ratio
    risk_free_rate = 0.02 / 365  # Assuming 2% annual risk-free rate
    excess_returns = [return_ - risk_free_rate for return_ in daily_returns]
    sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns)) * np.sqrt(365)
    
    return total_profit, winning_trades, losing_trades, win_rate, sharpe_ratio