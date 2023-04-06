from .Utils import *
from .Constants import *


class ZeroCouponHandler:
    r"""Function allowing the user to easily handle external market data (Zero-Coupon market prices)
    to interpolate and return an approximated shape of the function $t \longmapsto \theta(t)$ *mean-reversion* factor in the Hull & White model
    """

    def __init__(self) -> None:
        pass
    
    def get_data() -> None:
        r"""
        Reading the data from the Excel file in the `assets/data` sub-folder
        """
        return NotImplemented

    def compute_theta_values() -> None:
        r"""
        From the registered ZC price data, computing the values of $t \longmapsto \theta(t)$
        """
        return NotImplemented

    def get_theta_values() -> None:
        r"""
        Simple getter for the array of $\Big(t \longmapsto \theta(t)\Big)$
        """
        return NotImplemented

    def plot_theta_values() -> None:
        r"""
        Plot the shape of theta over the given time horizon $H = \left[0, T\right]$
        """
        return NotImplemented