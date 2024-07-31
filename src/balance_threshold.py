import src.constants

def calculate_balance_threshold():
    """
    Calculation to determine the optimal balance threshold.
    """
    binance_volume = src.constants.BINANCE_VOLUME / src.constants.BINANCE_DOMINANCE
    coinbase_volume = src.constants.COINBASE_VOLUME / src.constants.COINBASE_DOMINANCE
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