from .Pricer import *


class AsianPricer(Pricer):
    r"""Class representing a pricer of an Asian option 

    $$
    C^\text{ASIAN}(T, K) := \mathbb{E}\left[e^{-\int_0^T r_u \mathrm{~d} u}\left(\frac{1}{T} \int_0^T S_u \mathrm{~d} u-K\right)_{+}\right]
    $$
    
    with maturity $T > 0$ and strike (exercise price) $K > 0$
    """
    pass