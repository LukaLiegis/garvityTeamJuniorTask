import numpy as np
from typing import Tuple, List
from src.balance_threshold import calculate_balance_threshold
from src.optimal_balance import calculate_optimal_balances
import src.constants

# Calculate the balance threshold
BALANCE_THRESHOLD = calculate_balance_threshold()
TRANSFER_THRESHOLD = BALANCE_THRESHOLD - 0.05  # Set transfer threshold 5% below max balance

def simulate_trading(prices: np.ndarray, with_loan: bool = False) -> Tuple[List[float], int, float, List[float], List[float]]:
    hourly_profits = []
    trade_count = 0
    loan_cost = 0
    total_balance = src.constants.ASSETS_UNDER_MANAGEMENT
    binance_volumes = []
    coinbase_volumes = []
    
    # Time constraints
    transfer_cooldown_binance_to_coinbase = 0
    transfer_cooldown_coinbase_to_binance = 0
    
    # Initial balance allocation
    doubledoge_coinbase, doubledoge_binance, usd, usdt = calculate_optimal_balances(total_balance, prices[:24])  # Use first day's prices for initial allocation
    
    for day in range(src.constants.DAYS):
        # Recalculate optimal balances daily
        if day > 0:
            doubledoge_coinbase, doubledoge_binance, usd, usdt = calculate_optimal_balances(total_balance, prices[max(0, day*24-720):day*24])  # Use last 30 days or all available data

        for hour in range(src.constants.HOURS_PER_DAY):
            current_price = prices[day * src.constants.HOURS_PER_DAY + hour]
            hourly_profit = 0
            binance_volume = 0
            coinbase_volume = 0
            
            # Increased profit margin for 1 hour every day
            profit_margin = src.constants.INCREASED_PROFIT_MARGIN if hour == 0 else src.constants.NORMAL_PROFIT_MARGIN
            
            # Use fixed probability for trade direction
            if np.random.random() < src.constants.COINBASE_TO_BINANCE_PROBABILITY:
                # Buy on Coinbase, sell on Binance
                if doubledoge_coinbase >= src.constants.TRADE_SIZE:
                    buy_price = current_price * (1 - profit_margin/2)
                    sell_price = current_price * (1 + profit_margin/2)
                    trade_size = min(src.constants.TRADE_SIZE, doubledoge_coinbase)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (src.constants.COINBASE_FEE + src.constants.BINANCE_FEE)
                    
                    hourly_profit += profit
                    trade_count += 1
                    doubledoge_coinbase -= trade_size
                    doubledoge_binance += trade_size + profit
                    coinbase_volume += trade_size
                    binance_volume += trade_size
            else:
                # Buy on Binance, sell on Coinbase
                if doubledoge_binance >= src.constants.TRADE_SIZE:
                    buy_price = current_price * (1 - profit_margin/2)
                    sell_price = current_price * (1 + profit_margin/2)
                    trade_size = min(src.constants.TRADE_SIZE, doubledoge_binance)
                    profit = (sell_price - buy_price) * trade_size
                    profit -= trade_size * (src.constants.COINBASE_FEE + src.constants.BINANCE_FEE)
                    
                    hourly_profit += profit
                    trade_count += 1
                    doubledoge_binance -= trade_size
                    doubledoge_coinbase += trade_size + profit
                    binance_volume += trade_size
                    coinbase_volume += trade_size
            
            # Balance transfer logic with time constraints
            total_doubledoge = doubledoge_coinbase + doubledoge_binance
            if doubledoge_binance > total_doubledoge * BALANCE_THRESHOLD and transfer_cooldown_binance_to_coinbase == 0:
                transfer_amount = doubledoge_binance - (total_doubledoge * TRANSFER_THRESHOLD)
                transfer_fee = src.constants.BINANCE_TO_COINBASE_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    doubledoge_binance -= transfer_amount
                    doubledoge_coinbase += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
                    transfer_cooldown_binance_to_coinbase = 1  # 15 minutes cooldown (1/4 of an hour)
            elif doubledoge_coinbase > total_doubledoge * BALANCE_THRESHOLD and transfer_cooldown_coinbase_to_binance == 0:
                transfer_amount = doubledoge_coinbase - (total_doubledoge * TRANSFER_THRESHOLD)
                transfer_fee = src.constants.COINBASE_TO_BINANCE_TRANSFER_FEE
                if transfer_amount > transfer_fee:
                    doubledoge_coinbase -= transfer_amount
                    doubledoge_binance += transfer_amount - transfer_fee
                    hourly_profit -= transfer_fee
                    transfer_cooldown_coinbase_to_binance = 1  # 15 minutes cooldown (1/4 of an hour)
            
            # Update transfer cooldowns
            transfer_cooldown_binance_to_coinbase = max(0, transfer_cooldown_binance_to_coinbase - 1)
            transfer_cooldown_coinbase_to_binance = max(0, transfer_cooldown_coinbase_to_binance - 1)
            
            # Apply loan cost hourly, but based on the 3% daily rate
            if with_loan:
                hourly_loan_cost = (src.constants.LOAN_AMOUNT * src.constants.LOAN_INTEREST_RATE) / src.constants.HOURS_PER_DAY
                loan_cost += hourly_loan_cost
                hourly_profit -= hourly_loan_cost
            
            hourly_profits.append(hourly_profit)
            binance_volumes.append(binance_volume)
            coinbase_volumes.append(coinbase_volume)
            
            # Update total balance
            total_balance += hourly_profit
    
    return hourly_profits, trade_count, loan_cost, binance_volumes, coinbase_volumes