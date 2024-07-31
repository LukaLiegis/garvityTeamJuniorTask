import numpy as np
from typing import List

import src.constants

def calculate_volatility(prices: List[float], window: int = 20) -> float:
    """
    Calculate the volatility of the price series using a rolling window.
    """
    returns = np.log(prices[1:] / prices[:-1])
    volatility = np.std(returns[-window:]) * np.sqrt(src.constants.HOURS_PER_DAY)
    return volatility