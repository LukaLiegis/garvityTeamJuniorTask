from typing import Tuple, List
import numpy as np

DAYS = 100
HOURS_PER_DAY = 24
NORMAL_PROFIT_MARGIN = 0.016
INCREASED_PROFIT_MARGIN = 0.10
COINBASE_FEE = 0.00017
BINANCE_FEE = 0.00022
LOAN_INTEREST_RATE = 0.03
LOAN_AMOUNT = 1_000_000
TRADE_SIZE = 500
COINBASE_TO_BINANCE_PROBABILITY = 0.57
BINANCE_TO_COINBASE_TRANSFER_FEE = 45
COINBASE_TO_BINANCE_TRANSFER_FEE = 62
USD_USDT_TRANSFER_FEE = 3.5  # Average of $3 and $4
ASSETS_UNDER_MANAGEMENT = 10_000_000

def simulate_trading(prices: np.ndarray, with_loan: bool = False) -> Tuple[List[float], int, float]:
    hourly_profits = []
    trade_count = 0
    loan_cost = 0
    binance_balance = ASSETS_UNDER_MANAGEMENT / 2
    coinbase_balance = ASSETS_UNDER_MANAGEMENT / 2
    
    for day, daily_prices in enumerate(np.array_split(prices, DAYS)):
        for hour, price in enumerate(daily_prices):
            hourly_profit = 0
            
            # Increased profit margin for 1 hour every day
            profit_margin = INCREASED_PROFIT_MARGIN if hour == 0 else NORMAL_PROFIT_MARGIN
            
            if np.random.random() < COINBASE_TO_BINANCE_PROBABILITY:
                # Buy on Coinbase, sell on Binance
                if coinbase_balance >= TRADE_SIZE:
                    buy_price = price * (1 - profit_margin/2)
                    sell_price = price * (1 + profit_margin/2)
                    trade_size = min(TRADE_SIZE, coinbase_balance)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (COINBASE_FEE + BINANCE_FEE)
                    
                    if profit > 0:
                        hourly_profit += profit
                        trade_count += 1
                        coinbase_balance -= trade_size
                        binance_balance += trade_size + profit
            else:
                # Buy on Binance, sell on Coinbase
                if binance_balance >= TRADE_SIZE:
                    buy_price = price * (1 - profit_margin/2)
                    sell_price = price * (1 + profit_margin/2)
                    trade_size = min(TRADE_SIZE, binance_balance)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (COINBASE_FEE + BINANCE_FEE)
                    
                    if profit > 0:
                        hourly_profit += profit
                        trade_count += 1
                        binance_balance -= trade_size
                        coinbase_balance += trade_size + profit
            
            # Balance transfer logic
            total_balance = binance_balance + coinbase_balance
            if binance_balance > total_balance * 0.55:
                transfer_amount = binance_balance - (total_balance * 0.5)
                transfer_fee = BINANCE_TO_COINBASE_TRANSFER_FEE + USD_USDT_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    binance_balance -= transfer_amount
                    coinbase_balance += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
            elif coinbase_balance > total_balance * 0.55:
                transfer_amount = coinbase_balance - (total_balance * 0.5)
                transfer_fee = COINBASE_TO_BINANCE_TRANSFER_FEE + USD_USDT_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    coinbase_balance -= transfer_amount
                    binance_balance += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
            
            if with_loan:
                hourly_loan_cost = (LOAN_AMOUNT * LOAN_INTEREST_RATE) / HOURS_PER_DAY
                loan_cost += hourly_loan_cost
                hourly_profit -= hourly_loan_cost
            
            hourly_profits.append(hourly_profit)
    
    return hourly_profits, trade_count, loan_cost