import numpy as np

HOURS_PER_DAY = 24
MAX_DAILY_INCREASE = 0.60
MAX_DAILY_DECREASE = 0.25
HOURLY_FLUCTUATION = 0.05

def simulate_price(days: int, initial_price: float) -> np.ndarray:
    prices = np.zeros(days * HOURS_PER_DAY)
    prices[0] = initial_price
    
    for day in range(days):
        daily_change = np.random.uniform(-MAX_DAILY_DECREASE, MAX_DAILY_INCREASE)
        for hour in range(HOURS_PER_DAY):
            idx = day * HOURS_PER_DAY + hour
            if idx > 0:
                hourly_change = np.random.uniform(-HOURLY_FLUCTUATION, HOURLY_FLUCTUATION)
                prices[idx] = prices[idx-1] * (1 + hourly_change)
        
        # Apply daily change
        prices[day*HOURS_PER_DAY:(day+1)*HOURS_PER_DAY] *= (1 + daily_change)
    
    return prices