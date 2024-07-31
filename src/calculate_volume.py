from typing import Tuple

import src.constants

def calculate_daily_volume() -> Tuple[float, float]:
    binance_volume = src.constants.BINANCE_VOLUME * src.constants.BINANCE_DOMINANCE
    coinbase_volume = src.constants.COINBASE_VOLUME * src.constants.COINBASE_DOMINANCE
    return binance_volume, coinbase_volume