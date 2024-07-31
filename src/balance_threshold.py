HOURLY_FLUCTUATION = 0.05
COINBASE_FEE = 0.00017
BINANCE_FEE = 0.00022

def calculate_balance_threshold():
    binance_volume = 100_000_000 * 0.026  # 2.6% dominance
    coinbase_volume = 80_000_000 * 0.041  # 4.1% dominance
    total_volume = binance_volume + coinbase_volume
    
    # Calculate the ratio of volumes
    volume_ratio = max(binance_volume, coinbase_volume) / total_volume
    
    # Add a buffer for price fluctuations and fees
    buffer = HOURLY_FLUCTUATION + max(COINBASE_FEE, BINANCE_FEE)
    
    # Calculate the threshold
    threshold = volume_ratio + buffer
    
    # Round to nearest 5% for practicality
    rounded_threshold = round(threshold * 20) / 20
    
    return rounded_threshold