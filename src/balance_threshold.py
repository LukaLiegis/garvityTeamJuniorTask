import src.constants
from src.calculate_volume import calculate_daily_volume

def calculate_balance_threshold() -> float:
    """
    Calculation to determine the optimal balance threshold.
    """
    binance_volume, coinbase_volume = calculate_daily_volume()
    total_volume = binance_volume + coinbase_volume
    
    # Calculate the ratio of volumes
    volume_ratio = max(binance_volume, coinbase_volume) / total_volume
    
    # Add a buffer for price fluctuations and fees
    buffer = src.constants.HOURLY_FLUCTUATION + max(src.constants.COINBASE_FEE, src.constants.BINANCE_FEE)
    
    # Calculate the threshold
    threshold = volume_ratio + buffer
    
    # Round to nearest 5% for practicality
    rounded_threshold = round(threshold * 20) / 20
    
    return rounded_threshold