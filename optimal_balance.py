from typing import Tuple
from calculate_volume import calculate_daily_volume

def calculate_optimal_balances(total_assets: float) -> Tuple[float, float, float, float]:
    binance_volume, coinbase_volume = calculate_daily_volume()
    total_volume = binance_volume + coinbase_volume
    
    doubledoge_coinbase = (coinbase_volume / total_volume) * total_assets * 0.4
    doubledoge_binance = (binance_volume / total_volume) * total_assets * 0.4
    usd = total_assets * 0.1
    usdt = total_assets * 0.1
    
    return doubledoge_coinbase, doubledoge_binance, usd, usdt