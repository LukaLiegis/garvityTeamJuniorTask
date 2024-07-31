from typing import Tuple, List

from src.calculate_volume import calculate_daily_volume
from src.volatility import calculate_volatility
import src.constants

def calculate_optimal_balances(total_assets: float, prices: List[float]) -> Tuple[float, float, float, float]:
    """
    Calculate optimal balances based on recent market volatility.
    """
    volatility = calculate_volatility(prices)
    
    # Define volatility thresholds
    low_volatility = 0.1
    high_volatility = 0.3

    if volatility <= low_volatility:
        # Low volatility: Higher allocation to DOUBLEDOGE
        doubledoge_allocation = 0.45
        stable_allocation = 0.05
    elif volatility >= high_volatility:
        # High volatility: Higher allocation to stable assets
        doubledoge_allocation = 0.35
        stable_allocation = 0.15
    else:
        # Medium volatility: Linear interpolation
        volatility_factor = (volatility - low_volatility) / (high_volatility - low_volatility)
        doubledoge_allocation = 0.45 - (0.1 * volatility_factor)
        stable_allocation = 0.05 + (0.1 * volatility_factor)

    # Split DOUBLEDOGE allocation between Coinbase and Binance based on their volume ratio
    coinbase_volume, binance_volume = src.constants.COINBASE_VOLUME, src.constants.BINANCE_VOLUME
    total_volume = coinbase_volume + binance_volume
    coinbase_ratio = coinbase_volume / total_volume
    binance_ratio = binance_volume / total_volume

    return (
        doubledoge_allocation * coinbase_ratio * total_assets,
        doubledoge_allocation * binance_ratio * total_assets,
        stable_allocation * total_assets,
        stable_allocation * total_assets
    )