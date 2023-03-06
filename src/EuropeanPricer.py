from .Pricer import *
from .Constants import *
from .EquityModel import *
from .Utils import *

class EuropeanPricer(Pricer):
    r"""Class representing a pricer of an European option 

    $$
    C^\text{EUR}(T, K) := \mathbb{E}\left[e^{-\int_0^T r_u \mathrm{~d} u}\left(S_T-K\right)_{+}\right]
    $$

    with maturity $T > 0$ and strike (exercise price) $K > 0$
    """
    
    def __init__(self, udl_model: EquityModel, preCompute: bool = False, N_MC: int = Constants.MC_DEFAULT_ITERS) -> None:
        r"""Construtor function retrieving and storing the underlying price model

        Args:
            udl_model (EquityModel): Underlying asset price model
            preCompute (bool, optional): Boolean value corresponding to the pre-computation of equity trajectories. Defaults to False.
            N_MC (int, optional): Number of Monte-Carlo trajectories to be considered. Defaults to Constants.MC_DEFAULT_ITERS.
        """
        self.preCompute = preCompute

        # Pricer parameter
        self.model: EquityModel = udl_model
        self.N_MC = N_MC
        
        # Pre-computing the equity trajectories
        if preCompute:
            print("Pre-computing the equity trajectories")
            self.simulate_samples(N_MC=N_MC)
    

    def simulate_samples(self, N_MC: int = Constants.MC_DEFAULT_ITERS) -> pd.DataFrame: # trajectories to be stored (for caching)
        r"""Function which simulates prices trajectories

        Args:
            N_MC (int, optional): Number of Monte-Carlo trajectories to be simulated. Defaults to Constants.MC_DEFAULT_ITERS.

        Returns:
            pd.DataFrame: Trajectories
        """
        
        print("Simulating trajectories") # check if we add a tqdm handler
        # Simulating the trajectories necessary to Monte-Carlo
        trajectories = [self.model.simulate_euler(getRates=True) for _ in range(self.N_MC)]

        # Casting it into a pandas DataFrame for a better handling (using slicing)
        trajectories = Utils.cast_df(trajectories)

        # Storing the results
        self.trajectories = trajectories

        # Returning the trajectories
        return self.trajectories


    def compute_option_price(self, contract: Constants.Contract.CALL):


        # Retrieving the time interval values
        t = trajectories[0]["t"]

        # Retrieving the list of underlying asset $(S^i_t)_t$
        S_T_ = [trajectories[k]["S"].iloc[-1] for k in range(len(trajectories))]


        pass

    def compute_option_price_call(self, K: float):
        pass

    def compute_option_price_put(self, K: float):
        pass
