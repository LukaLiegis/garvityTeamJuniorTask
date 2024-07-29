from decimal import Decimal, getcontext
import numpy as np
import random

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