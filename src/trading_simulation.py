from typing import Tuple, List
import numpy as np

from src.balance_threshold import calculate_balance_threshold
import src.constants

# Calculate the balance threshold
BALANCE_THRESHOLD = calculate_balance_threshold()
TRANSFER_THRESHOLD = BALANCE_THRESHOLD - 0.05  # Set transfer threshold 5% below max balance

def simulate_trading(prices: np.ndarray, with_loan: bool = False) -> Tuple[List[float], int, float]:
    hourly_profits = []
    trade_count = 0
    loan_cost = 0
    binance_balance = src.constants.ASSETS_UNDER_MANAGEMENT / 2
    coinbase_balance = src.constants.ASSETS_UNDER_MANAGEMENT / 2
    
    for day, daily_prices in enumerate(np.array_split(prices, src.constants.DAYS)):
        for hour, price in enumerate(daily_prices):
            hourly_profit = 0
            
            # Increased profit margin for 1 hour every day
            profit_margin = src.constants.INCREASED_PROFIT_MARGIN if hour == 0 else src.constants.NORMAL_PROFIT_MARGIN
            
            if np.random.random() < src.constants.COINBASE_TO_BINANCE_PROBABILITY:
                # Buy on Coinbase, sell on Binance
                if coinbase_balance >= src.constants.TRADE_SIZE:
                    buy_price = price * (1 - profit_margin/2)
                    sell_price = price * (1 + profit_margin/2)
                    trade_size = min(src.constants.TRADE_SIZE, coinbase_balance)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (src.constants.COINBASE_FEE + src.constants.BINANCE_FEE)
                    
                    hourly_profit += profit
                    trade_count += 1
                    coinbase_balance -= trade_size
                    binance_balance += trade_size + profit
            else:
                # Buy on Binance, sell on Coinbase
                if binance_balance >= src.constants.TRADE_SIZE:
                    buy_price = price * (1 - profit_margin/2)
                    sell_price = price * (1 + profit_margin/2)
                    trade_size = min(src.constants.TRADE_SIZE, binance_balance)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (src.constants.COINBASE_FEE + src.constants.BINANCE_FEE)
                    
                    hourly_profit += profit
                    trade_count += 1
                    binance_balance -= trade_size
                    coinbase_balance += trade_size + profit
            
            # Balance transfer logic (unchanged)
            total_balance = binance_balance + coinbase_balance
            if binance_balance > total_balance * BALANCE_THRESHOLD:
                transfer_amount = binance_balance - (total_balance * TRANSFER_THRESHOLD)
                transfer_fee = src.constants.BINANCE_TO_COINBASE_TRANSFER_FEE + src.constants.USD_USDT_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    binance_balance -= transfer_amount
                    coinbase_balance += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
            elif coinbase_balance > total_balance * BALANCE_THRESHOLD:
                transfer_amount = coinbase_balance - (total_balance * TRANSFER_THRESHOLD)
                transfer_fee = src.constants.COINBASE_TO_BINANCE_TRANSFER_FEE + src.constants.USD_USDT_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    coinbase_balance -= transfer_amount
                    binance_balance += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
            
            if with_loan:
                hourly_loan_cost = (src.constants.LOAN_AMOUNT * src.constants.LOAN_INTEREST_RATE) / src.constants.HOURS_PER_DAY
                loan_cost += hourly_loan_cost
                hourly_profit -= hourly_loan_cost
            
            hourly_profits.append(hourly_profit)
    
    return hourly_profits, trade_count, loan_cost