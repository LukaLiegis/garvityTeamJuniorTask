from decimal import Decimal, getcontext
import numpy as np
import random
from random import uniform
import matplotlib.pyplot as plt

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
        self.profit_history = []
        self.volume_history = []
        self.trades_history = []

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
            self.price_history.append(float(self.current_price))

    def simulate_trading(self):
        for day in range(self.days):
            daily_volume = Decimal('0')
            daily_trades = 0
            daily_profit = Decimal('0')
            
            for hour in range(self.hours_per_day):
                if random.random() < self.coinbase_buy_probability:
                    trade_result = self.trade('coinbase', 'binance')
                else:
                    trade_result = self.trade('binance', 'coinbase')
                
                daily_volume += trade_result['volume']
                daily_trades += trade_result['trades']
                daily_profit += trade_result['profit']
            
            rebalance_cost = self.rebalance()
            daily_profit -= rebalance_cost
            
            self.profit_history.append(float(daily_profit))
            self.volume_history.append(float(daily_volume))
            self.trades_history.append(daily_trades)

    def trade(self, buy_exchange, sell_exchange):
        trade_amount = min(self.trade_size, self.balances['USD'], self.balances['USDT'])
        if trade_amount > 0:
            coins_bought = trade_amount / self.current_price
            coins_sold = coins_bought * (1 - self.profit_margin)
            
            coins_bought *= (1 - getattr(self, f'{buy_exchange}_fee'))
            coins_sold *= (1 - getattr(self, f'{sell_exchange}_fee'))
            
            profit = (coins_sold * self.current_price) - trade_amount
            
            self.balances[f'DOUBLEDOGE_{buy_exchange}'] += coins_bought
            self.balances[f'DOUBLEDOGE_{sell_exchange}'] -= coins_sold
            
            if buy_exchange == 'coinbase':
                self.balances['USD'] -= trade_amount
                self.balances['USDT'] += coins_sold * self.current_price
            else:
                self.balances['USDT'] -= trade_amount
                self.balances['USD'] += coins_sold * self.current_price
            
            return {'volume': trade_amount, 'trades': 1, 'profit': profit}
        return {'volume': Decimal('0'), 'trades': 0, 'profit': Decimal('0')}
    
    def rebalance(self):
        total_fiat = self.balances['USD'] + self.balances['USDT']
        total_doubledoge = (self.balances['DOUBLEDOGE_coinbase'] + self.balances['DOUBLEDOGE_binance']) * self.current_price
        total_value = total_fiat + total_doubledoge

        rebalance_cost = Decimal('0')

        # Rebalance USD and USDT
        usd_difference = self.balances['USD'] - total_fiat / 2
        if abs(usd_difference) > total_value * Decimal('0.05'):  # 5% threshold
            transfer_amount = abs(usd_difference)
            transfer_fee = self.binance_to_coinbase_fee_usd if usd_difference > 0 else self.coinbase_to_binance_fee_usd
            
            if transfer_amount > transfer_fee:
                actual_transfer = transfer_amount - transfer_fee
                if usd_difference > 0:
                    self.balances['USD'] -= transfer_amount
                    self.balances['USDT'] += actual_transfer
                else:
                    self.balances['USD'] += actual_transfer
                    self.balances['USDT'] -= transfer_amount
                rebalance_cost += transfer_fee

        # Rebalance DOUBLEDOGE between exchanges
        total_doubledoge_coins = self.balances['DOUBLEDOGE_coinbase'] + self.balances['DOUBLEDOGE_binance']
        target_doubledoge_coinbase = total_doubledoge_coins * Decimal(self.coinbase_dominance) / (Decimal(self.coinbase_dominance) + Decimal(self.binance_dominance))
        doubledoge_difference = self.balances['DOUBLEDOGE_coinbase'] - target_doubledoge_coinbase

        if abs(doubledoge_difference) > total_doubledoge_coins * Decimal('0.1'):  # 10% threshold
            transfer_amount = abs(doubledoge_difference)
            transfer_fee = self.coinbase_to_binance_fee_doubledoge if doubledoge_difference > 0 else self.binance_to_coinbase_fee_doubledoge
            transfer_fee_in_coins = transfer_fee / self.current_price
            
            if transfer_amount > transfer_fee_in_coins:
                actual_transfer = transfer_amount - transfer_fee_in_coins
                if doubledoge_difference > 0:
                    self.balances['DOUBLEDOGE_coinbase'] -= transfer_amount
                    self.balances['DOUBLEDOGE_binance'] += actual_transfer
                else:
                    self.balances['DOUBLEDOGE_coinbase'] += actual_transfer
                    self.balances['DOUBLEDOGE_binance'] -= transfer_amount
                rebalance_cost += transfer_fee

        return rebalance_cost

    def run_simulation(self):
        self.simulate_price()
        self.simulate_trading()

# Run the simulation
sim = DoubleDogeSim()
sim.run_simulation()

# Print results
print(f"Average daily volume: {sim.daily_volume / sim.days}")
print(f"Average daily trades: {sim.daily_trades / sim.days}")
print(f"Average daily profit: {sum(sim.profit_history) / sim.days}")
print(f"Final balances: {sim.balances}")

# Plot price history and profit curve
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# Plot price history
ax1.plot(sim.price_history)
ax1.set_title('DOUBLEDOGE Price History')
ax1.set_ylabel('Price (USD)')

# Plot cumulative profit curve
cumulative_profit = np.cumsum(sim.profit_history)
ax2.plot(cumulative_profit)
ax2.set_title('Cumulative Profit')
ax2.set_xlabel('Days')
ax2.set_ylabel('Profit (USD)')

plt.tight_layout()
plt.show()