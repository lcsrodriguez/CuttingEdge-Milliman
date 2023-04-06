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
    
    def __init__(self, 
                 udl_model: EquityModel, 
                 preCompute: bool = False, 
                 N_MC: int = Constants.MC_DEFAULT_ITERS) -> None:
        r"""Construtor function retrieving and storing the underlying price model

        Args:
            udl_model (EquityModel): Underlying asset price model
            preCompute (bool, optional): Boolean value corresponding to the pre-computation of equity trajectories. Defaults to False.
            N_MC (int, optional): Number of Monte-Carlo trajectories to be considered. Defaults to Constants.MC_DEFAULT_ITERS.
        """
        self.preCompute : bool = preCompute
        self.isSimulated : bool  = False

        # Pricer parameter
        self.model: EquityModel = udl_model
        self.N_MC : int = N_MC
        
        # Pre-computing the equity trajectories
        if preCompute:
            print("Pre-computing the equity trajectories")
            self.simulate_samples(N_MC=N_MC)
    
    def compute_option_price(self, 
                             K: float, 
                             contract: Constants.Contract = Constants.Contract.CALL,
                             ci_levels: Union[List[Constants.Level], Constants.Level] = Constants.Level.LEVEL_95,
                             N_MC: int = Constants.MC_DEFAULT_ITERS) -> float:
        r"""Function computing and returning the option price thanks to a Monte-Carlo simulation, depending on its contract type

        $$
        \phi^i := \exp\Big(-\int_{0}^T r^i_u \mathrm{d}u\Big)\Pi(S^i_T, K)
        $$

        Args:
            K (float): Strike price (Exercise price)
            contract (Constants.Contract.CALL): Contract option type (PUT or CALL)
            N_MC (int, optional): Number of Monte-Carlo trajectories to be simulated. Defaults to Constants.MC_DEFAULT_ITERS.

        Raises:
            Exception: Exception regarding the contract type

        Returns:
            float: Option price
        """        

        # If not simulated yet, we simulate the trajectories
        if not self.isSimulated:
            self.simulate_samples(N_MC=N_MC)

        # Defining the payoff function according to the contract type
        if contract == Constants.Contract.CALL:
            PAYOFF_FUNCTION = Pricer.CALL_PAYOFF 
        elif contract == Constants.Contract.PUT:
            PAYOFF_FUNCTION = Pricer.PUT_PAYOFF 
        else:
            raise Exception("The contract type is not valid.")

        # Retrieving the time interval values
        t = self.trajectories[0]["t"]

        # Retrieving the list of last-time underlying asset price $S^i_T$
        S_T_ = [self.trajectories[k]["S"].iloc[-1] for k in range(len(self.trajectories))]

        # Retrieving the list of rates $(r^i_t)_t$
        R_ = [self.trajectories[k]["r"].to_numpy() for k in range(len(self.trajectories))]

        # Computing the $\phi_i$
        PHIS = []
        for i in range(self.N_MC):
            # Computing the integral of interest rates using Simpson numerical method
            integral = scipy.integrate.simpson(R_[i], t)

            # Computing the coefficient $\phi_i$
            phi = np.exp(-integral)*PAYOFF_FUNCTION(x=S_T_[i], K=K)

            # Appending the $\phi_i$
            PHIS.append(phi)
        
        # Computing the option price by aggregating the previously-computed results
        OPTION_PRICE = (1/self.N_MC)*sum(PHIS)

        # Casting into a Numpy array to access statistic methods
        PHIS = np.array(PHIS)

        # Computing Monte-Carlo confidence intervals
        CI_LEVELS = []

        # Filtering with respect to the input type
        if type(ci_levels) == Constants.Level or (type(ci_levels) == list and len(ci_levels) == 1):
            if type(ci_levels) == list and len(ci_levels) == 1:
                CI_LEVELS.append(ci_levels[0])
            else:
                CI_LEVELS.append(ci_levels)
        elif type(ci_levels) == list:
            CI_LEVELS += ci_levels
        
        print(f"Required CI levels: ", Utils.get_level_values(CI_LEVELS))
        
        CI_DICT = {level.value: None for level in CI_LEVELS}
        # For each required CI level
        for level in CI_LEVELS:
            # Getting the respective Z-score
            a = Constants.Z_SCORES[level.value]
            
            # Computing the CI factor
            ci_factor = a*(PHIS.std())/np.sqrt(self.N_MC)

            # Computing the lower/upper bounds of the CI interval
            ci = {
                "lower": OPTION_PRICE - ci_factor, 
                "upper": OPTION_PRICE + ci_factor,
                "radius": ci_factor
            }
            CI_DICT[level.value] = ci

        # Returning the option price and the Confidence interval
        return {"price": OPTION_PRICE, "ci": CI_DICT}