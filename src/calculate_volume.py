from typing import Tuple

def calculate_daily_volume() -> Tuple[float, float]:
    binance_volume = 100_000_000 * 0.026  # 2.6% dominance
    coinbase_volume = 80_000_000 * 0.041  # 4.1% dominance
    return binance_volume, coinbase_volume