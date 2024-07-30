from typing import Tuple
import numpy as np

DAYS = 100
NORMAL_PROFIT_MARGIN = 0.016
INCREASED_PROFIT_MARGIN = 0.10
COINBASE_FEE = 0.00017
BINANCE_FEE = 0.00022
LOAN_INTEREST_RATE = 0.03
LOAN_AMOUNT = 1_000_000
TRADE_SIZE = 500
COINBASE_TO_BINANCE_PROBABILITY = 0.57

def simulate_trading(prices: np.ndarray, with_loan: bool = False) -> Tuple[float, int, float]:
    total_profit = 0
    trade_count = 0
    loan_cost = 0
    
    for day, daily_prices in enumerate(np.array_split(prices, DAYS)):
        daily_profit = 0
        daily_trades = 0
        
        for hour, price in enumerate(daily_prices):
            # Increased profit margin for 1 hour every day
            if hour == 0:
                profit_margin = INCREASED_PROFIT_MARGIN
            else:
                profit_margin = NORMAL_PROFIT_MARGIN
            
            if np.random.random() < COINBASE_TO_BINANCE_PROBABILITY:
                # Buy on Coinbase, sell on Binance
                buy_price = price * (1 - profit_margin/2)
                sell_price = price * (1 + profit_margin/2)
            else:
                # Buy on Binance, sell on Coinbase
                buy_price = price * (1 - profit_margin/2)
                sell_price = price * (1 + profit_margin/2)
            
            trade_size = TRADE_SIZE * (2 if with_loan else 1)  # Double trade size if loan is taken
            profit = (sell_price - buy_price) * trade_size
            profit -= trade_size * COINBASE_FEE  # Coinbase fee
            profit -= trade_size * BINANCE_FEE   # Binance fee
            
            if profit > 0:
                daily_profit += profit
                daily_trades += 1
        
        if with_loan:
            daily_loan_cost = LOAN_AMOUNT * LOAN_INTEREST_RATE
            loan_cost += daily_loan_cost
            daily_profit -= daily_loan_cost
        
        total_profit += daily_profit
        trade_count += daily_trades
    
    return total_profit, trade_count, loan_cost