from decimal import Decimal, getcontext
import numpy as np
import random
from random import uniform

getcontext().prec = 8

class DoubleDogeSim:
    def __init__(self):
        self.initial_price = Decimal("5")
        self.current_price = self.initial_price
        self.days = 100
        self.hours_per_day = 24
        self.binance_volume = Decimal("100000000")
        self.coinbase_volume = Decimal("80000000")
        self.binance_dominance = Decimal("0.026")
        self.coinbase_dominance = Decimal("0.041")
        self.hourly_fluctuation = Decimal("0.05")
        self.max_daily_increase = Decimal("0.60")
        self.max_daily_decrease = Decimal("0.25")
        self.loan_interest = Decimal("0.03")
        self.binance_to_coinbase_fee_doubledoge = Decimal("45")
        self.coinbase_to_binance_fee_doubledoge = Decimal("62")
        self.binance_to_coinbase_fee_usd = Decimal("3")
        self.coinbase_to_binance_fee_usd = Decimal("4")
        self.usd_usdt_rate = Decimal("1.0012")
        self.profit_margin = Decimal("0.016")
        self.coinbase_fee = Decimal("0.00017")
        self.binance_fee = Decimal("0.00022")
        self.trade_size = Decimal("500")
        self.coinbase_buy_probability = Decimal("0.57")
        self.assets_under_management = Decimal("10000000")

        self.price_history = []
        self.daily_volume = Decimal("0")
        self.daily_trades = 0
        self.daily_profit = Decimal("0")

        self.balances = {
            "DOUBLEDOGE_coinbase": Decimal("0"),
            "DOUBLEDOGE_binance": Decimal("0"),
            "USD": self.assets_under_management / 2,
            "USDT": self.assets_under_management / 2
        }

    def simulate_price(self):
        for day in range(self.days):
            daily_change = Decimal(uniform(-0.25, 0.60))
            for hour in range(self.hours_per_day):
                hourly_change = Decimal(uniform(-0.05, 0.05))
                self.current_price *= (1 + hourly_change)
            self.current_price *= (1 + daily_change)
            self.current_price = max(min(
                self.current_price,
                self.initial_price * (1 + self.max_daily_increase)),
                self.initial_price * (1 - self.max_daily_decrease)
            )
            self.price_history.append(self.current_price)

    def simulate_trading(self):
        for day in range(self.days):
            self.daily_volume = Decimal("0")
            self.daily_trades = 0
            self.daily_profit = Decimal("0")

            for hour in range(self.hours_per_day):
                 if random.random() < self.coinbase_buy_probability:
                    self.trade("coinbase", "binance")
                 else:
                    self.trade("binance", "coinbase")

            # Rebalance if necessary
            self.rebalance()

    def trade(self, buy_exchange, sell_exchange):
        trade_amount = min(
            self.trade_size,
            self.balances["USD"],
            self.balances["USDT"]
        )
        if trade_amount > 0:
            coins_bought = trade_amount / self.current_price
            coins_sold = coins_bought * (1 - self.profit_margin)

            # Apply fees
            coins_bought *= (1 - getattr(self, f"{buy_exchange}_fee"))
            coins_sold *= (1 - getattr(self, f"{sell_exchange}_fee"))

            profit = (coins_sold * self.current_price) - trade_amount

            self.balances[f"DOUBLEDOGE_{buy_exchange}"] += coins_bought
            self.balances[f"DOUBLEDOGE_{sell_exchange}"] -= coins_sold

            if buy_exchange == "coinbase":
                self.balances["USD"] -= trade_amount
                self.balances["USDT"] += coins_sold * self.current_price
            else:
                self.balances["USDT"] -= trade_amount
                self.balances["USD"] += coins_sold * self.current_price

            self.daily_volume += trade_amount
            self.daily_trades += 1
            self.daily_profit += profit