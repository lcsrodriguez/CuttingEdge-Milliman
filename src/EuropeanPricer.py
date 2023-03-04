from .Pricer import *
from .Constants import *
from .EquityModel import *

class EuropeanPricer(Pricer):
    r"""Class representing a pricer of an European option 

    $$
    C^\text{EUR}(T, K) := \mathbb{E}\left[e^{-\int_0^T r_u \mathrm{~d} u}\left(S_T-K\right)_{+}\right]
    $$

    with maturity $T > 0$ and strike (exercise price) $K > 0$
    """
    
    def __init__(self, udl_model: EquityModel, preCompute: bool = False, N_MC: int = Constants.MC_DEFAULT_ITERS) -> None:
        """Construtor function retrieving and storing the underlying price model

        Args:
            udl_model (EquityModel): Underlying asset price model
            preCompute (bool, optional): Boolean value corresponding to the pre-computation of equity trajectories. Defaults to False.
            N_MC (int, optional): Number of Monte-Carlo trajectories to be considered. Defaults to Constants.MC_DEFAULT_ITERS.
        """
        self.preCompute = preCompute
        
        # Pre-computing the equity trajectories
        if preCompute:
            print("Pre-computing the equity trajectories")
            self.simulate_samples(N_MC=N_MC)
    

    def simulate_samples(self, N_MC: int = Constants.MC_DEFAULT_ITERS) -> bool: # trajectories to be stored (for caching)
        pass


    def compute_option_price(self, contract: Constants.Contract.CALL):
        pass

    def compute_option_price_call(self, K: float):
        pass

    def compute_option_price_put(self, K: float):
        pass
