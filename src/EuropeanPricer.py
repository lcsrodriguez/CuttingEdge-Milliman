from .Pricer import *
from .Constants import *
from .EquityModel import *
from .Utils import *
import pandas

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
        self.preCompute : bool = preCompute
        self.isSimulated : bool  = False

        # Pricer parameter
        self.model: EquityModel = udl_model
        self.N_MC : int = N_MC
        
        # Pre-computing the equity trajectories
        if preCompute:
            print("Pre-computing the equity trajectories")
            self.simulate_samples(N_MC=N_MC)
    

    def simulate_samples(self, N_MC: int = Constants.MC_DEFAULT_ITERS) -> pandas.DataFrame: # trajectories to be stored (for caching)
        r"""Function which simulates prices trajectories

        Args:
            N_MC (int, optional): Number of Monte-Carlo trajectories to be simulated. Defaults to Constants.MC_DEFAULT_ITERS.

        Returns:
            pd.DataFrame: Trajectories
        """
        
        # Updating N_MC if different
        self.N_MC = N_MC

        print("Simulating trajectories") # check if we add a tqdm handler
        # Simulating the trajectories necessary to Monte-Carlo
        trajectories = [self.model.simulate_euler(getRates=True) for _ in range(self.N_MC)]

        # Casting it into a pandas DataFrame for a better handling (using slicing)
        trajectories = Utils.cast_df(trajectories)

        # Storing the results
        self.trajectories = trajectories
        self.isSimulated = True

        # Returning the trajectories
        return self.trajectories


    def compute_option_price(self, K: float, contract: Constants.Contract.CALL) -> float:
        r"""Function computing and returning the option price thanks to a Monte-Carlo simulation, depending on its contract type

        Args:
            K (float): Strike price (Exercise price)
            contract (Constants.Contract.CALL): Contract option type (PUT or CALL)

        Raises:
            Exception: Exception regarding the contract type

        Returns:
            float: Option price
        """        

        # If not simulated yet, we simulate the trajectories
        if not self.isSimulated:
            self.simulate_samples()

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
            phi = np.exp(-integral)*Pricer.CALL_PAYOFF(S_T_[i])

            # Appending the $\phi_i$
            PHIS.append(phi)
        
        # Computing the option price by aggregating the previously-computed results
        OPTION_PRICE = (1/self.N_MC)*sum(PHIS)
        return OPTION_PRICE

    def compute_option_price_call(self, K: float) -> float:
        r"""Function computing and returning the call option price thanks to a Monte-Carlo simulation

        Args:
            K (float): Strike price (Exercise price)

        Returns:
            float: Call option price
        """        
        return self.compute_option_price(K=K, contract=Constants.Contract.CALL)

    def compute_option_price_put(self, K: float) -> float:
        r"""Function computing and returning the put option price thanks to a Monte-Carlo simulation

        Args:
            K (float): Strike price (Exercise price)

        Returns:
            float: Put option price
        """       
        return self.compute_option_price(K=K, contract=Constants.Contract.PUT)
