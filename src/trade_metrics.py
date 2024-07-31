from typing import List

def calculate_trade_metrics(hourly_profits: List[float], trade_count: int):
    total_profit = sum(hourly_profits)
    winning_trades = sum(1 for profit in hourly_profits if profit > 0)
    losing_trades = trade_count - winning_trades
    win_rate = winning_trades / trade_count if trade_count > 0 else 0
    
    return total_profit, winning_trades, losing_trades, win_rate