import numpy as np
import matplotlib.pyplot as plt

from src.price_simulation import simulate_price
from src.trading_simulation import simulate_trading
from src.trade_metrics import calculate_trade_metrics
from src.calculate_volume import calculate_daily_volume
from src.optimal_balance import calculate_optimal_balances
from src.balance_threshold import calculate_balance_threshold

DAYS = 100
HOURS_PER_DAY = 24
INITIAL_PRICE = 5
ASSETS_UNDER_MANAGEMENT = 10_000_000
SCANDAL_INTERVAL = 5

# Calculate the balance threshold
BALANCE_THRESHOLD = calculate_balance_threshold()
TRANSFER_THRESHOLD = BALANCE_THRESHOLD - 0.05  # Set transfer threshold 5% below max balance

# Main simulation
prices = simulate_price(DAYS, INITIAL_PRICE)
hourly_profits_without_loan, trade_count_without_loan, _ = simulate_trading(prices)
hourly_profits_with_loan, trade_count_with_loan, loan_cost = simulate_trading(prices, with_loan=True)

total_profit_without_loan = sum(hourly_profits_without_loan)
total_profit_with_loan = sum(hourly_profits_with_loan)

# Calculate metrics
metrics_without_loan = calculate_trade_metrics(hourly_profits_without_loan, trade_count_without_loan)
metrics_with_loan = calculate_trade_metrics(hourly_profits_with_loan, trade_count_with_loan)

# Calculate and print results
daily_volume_binance, daily_volume_coinbase = calculate_daily_volume()
optimal_balances = calculate_optimal_balances(ASSETS_UNDER_MANAGEMENT)

print(f"1. Expected daily trading volume: ${daily_volume_binance + daily_volume_coinbase:,.2f}")
print(f"2. Optimal balances:")
print(f"   DOUBLEDOGE_coinbase: ${optimal_balances[0]:,.2f}")
print(f"   DOUBLEDOGE_binance: ${optimal_balances[1]:,.2f}")
print(f"   USD: ${optimal_balances[2]:,.2f}")
print(f"   USDT: ${optimal_balances[3]:,.2f}")
print(f"3. Max balance for each asset/exchange: {BALANCE_THRESHOLD:.2%} of total assets")
print(f"4. Transfer between exchanges when balance exceeds {BALANCE_THRESHOLD:.2%} of total assets on one exchange")
print(f"5. Expected trades per day: {trade_count_without_loan // DAYS}")
print(f"6. Loan analysis:")
print(f"   Profit without loan: ${metrics_without_loan[0]:,.2f}")
print(f"   Profit with loan: ${metrics_with_loan[0]:,.2f}")
print(f"   Loan cost: ${loan_cost:,.2f}")
print(f"   Win rate without loan: {metrics_without_loan[3]:.2%}")
print(f"   Win rate with loan: {metrics_with_loan[3]:.2%}")
if metrics_with_loan[0] > metrics_without_loan[0]:
    print(f"   Recommendation: Take the loan. Additional profit: ${metrics_with_loan[0] - metrics_without_loan[0]:,.2f}")
else:
    print(f"   Recommendation: Do not take the loan. Potential loss: ${metrics_without_loan[0] - metrics_with_loan[0]:,.2f}")
print(f"7. Expected total profit per day (without loan): ${metrics_without_loan[0] / DAYS:,.2f}")
print("8. Risk measures: Implement position limits, stop-loss orders, and diversification")
print("9. Key metrics: Daily profit, trade count, asset distribution, price volatility, loan utilization")
print("10. Stop loss: 10% below entry, Take profit: 20% above entry")
print("11. Improvements: Implement machine learning for price prediction, optimize trade timing, dynamic loan utilization")

# Plot price simulation and P/L curves
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Price simulation plot
ax1.plot(prices)
ax1.set_title('DOUBLEDOGE Price Simulation')
ax1.set_xlabel('Hours')
ax1.set_ylabel('Price ($)')

# Highlight scandal days
for i in range(SCANDAL_INTERVAL, DAYS + 1, SCANDAL_INTERVAL):
    ax1.axvline(x=i * HOURS_PER_DAY, color='r', linestyle='--', alpha=0.5)

# P/L curve plot
hours = np.arange(DAYS * HOURS_PER_DAY)
cumulative_profit_without_loan = np.cumsum(hourly_profits_without_loan)
cumulative_profit_with_loan = np.cumsum(hourly_profits_with_loan)

ax2.plot(hours, cumulative_profit_without_loan, label='Without Loan')
ax2.plot(hours, cumulative_profit_with_loan, label='With Loan')
ax2.set_title('Cumulative Profit/Loss')
ax2.set_xlabel('Hours')
ax2.set_ylabel('Profit ($)')
ax2.legend()

# Highlight scandal days
for i in range(SCANDAL_INTERVAL, DAYS + 1, SCANDAL_INTERVAL):
    ax2.axvline(x=i * HOURS_PER_DAY, color='r', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()