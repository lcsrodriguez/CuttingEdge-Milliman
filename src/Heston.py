from .EquityModel import *
from .RatesModel import *
from .Utils import *
from .Constants import *

class Heston(EquityModel):
    r"""Class representing the Heston model *(stochastic volatility)*
    
    $$\frac{\mathrm{d}S_t}{S_t} := r_t\mathrm{d}t + \sqrt{V_t}\mathrm{d}W_t$$

    and

    $$\mathrm{d}V_t := \kappa(\theta - V_t)\mathrm{d}t + \eta\sqrt{V_t}\mathrm{d}\widetilde{W_t}$$

    As for the correlation matrix $\Sigma$, it is expected to be of the following form

    $$ \Sigma := \begin{bmatrix}
    \rho_{11} & \rho_{12} & \rho_{13} \\
    \rho_{21} & \rho_{22} & \rho_{23} \\
    \rho_{31} & \rho_{32} & \rho_{33} 
    \end{bmatrix} = \begin{bmatrix}
    1 & \rho_{21} & \rho_{31} \\
    \rho_{21} & 1 & \rho_{32} \\
    \rho_{31} & \rho_{32} & 1
    \end{bmatrix}  \in \mathcal{S}^{++}_3  $$

    where $\forall (i, j) \in \lbrace 1, 2, 3\rbrace^2, \ \rho_{ij} := \text{Cov}(W^i, W^j)$

    """
    
    # Name of the model
    MODEL_NAME = "HESTON"
    
    def __init__(self, 
                 S0: float, 
                 V0: float,
                 r: RatesModel, 
                 kappa: float, 
                 theta: float, 
                 eta: float,  
                 Sigma: Union[np.ndarray, list]) -> None:
        super().__init__()

        # Verification of parameter values
        assert S0 > 0
        assert V0 > 0
        
        # Check if the rate model is a registered and valid model 
        if not issubclass(type(r), RatesModel): # type(r).__bases__[0] == RatesModel
            raise Exception("r must be a registered interest rates model\n(Available models: Vasicek, CIR, HW)")
                
        # Storing variables
        self.S0 = S0
        self.V0 = V0
        self.r: RatesModel = r
        self.kappa = kappa
        self.theta = theta
        self.eta = eta

        # Checking the correlation matrix
        if isinstance(Sigma, list):
            # Check whether this is a square matrix for safety purpose
            assert len(Sigma) == len(Sigma)[0]
            Sigma = np.array(Sigma)
        self.Sigma = Sigma

        self.LAST_SIMULATION = {}

    def __repr__(self) -> str:
        r"""Hard string representation

        Returns:
            str: Output string
        """
        return f"Heston model {self.get_parameter_string(onLaTeX=False)}"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation

        Returns:
            str: Output string
        """
        return f"Heston model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r""" Function returning a user-friendly string displaying the model parameters values

        Args:
            onLaTeX (bool, optional): Boolean value indicating if $\LaTeX$ formatting is enabled. Defaults to True.

        Returns:
            str: Output string of each parameter's value
        """
        if onLaTeX:
            return f"($S_0$ = {self.S0}, $\kappa$ = {self.kappa}, $\\theta$ = {self.theta}, $\eta$ = {self.eta})"
        return f"(S0 = {self.S0}, kappa = {self.kappa}, theta = {self.theta}, eta = {self.eta})"
    
    def simulate_path(self, scheme: Constants.Scheme = Constants.Scheme.EULER, *args, **kwargs) -> dict:
        r"""Function wrapping the 2 available simulators to simulate 1 path

        Args:
            scheme (Constants.Scheme, optional): Numerical scheme to be used. Defaults to Constants.Scheme.EULER.

        Returns:
            dict: Hashmap of results with keys `t` for time interval and `r` for rates simulation results
        """
        if scheme == Constants.Scheme.EULER:
            return self.simulate_euler(*args, **kwargs)
        return self.simulate_milstein(*args, **kwargs)
    
    def simulate_paths(self, M: int = 3, scheme: Constants.Scheme = Constants.Scheme.EULER, *args, **kwargs) -> dict:
        r"""Function wrapping the 2 available simulators to simulate **several** paths

        Args:
            M (int, optional): Number of trajectories to be applied. Defaults to 3.
            scheme (Constants.Scheme, optional): Numerical scheme to be applied. Defaults to Constants.Scheme.EULER.

        Returns:
            dict: Hashmap of results with keys `t` for time interval and `r`$\star$ for rates simulation results where $\star$ stand for the id of the simulations
        """
        assert M >= 1 and type(M) == int
        
        res = []
        for m in range(1, M + 1):
            if scheme == Constants.Scheme.EULER:
                sim = self.simulate_euler(*args, **kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["S"])
            elif scheme == Constants.Scheme.MILSTEIN:
                sim = self.simulate_milstein(*args, **kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["S"])
        return res

    def simulate_euler(self,
                       T: float = 1.0,
                       N: int = Constants.MAX_STEPS,
                       getVariance: bool = False,
                       getRates: bool = False) -> dict:
        
        # Time step
        dT = T/float(N)

        # Generating the time horizon array
        H = np.arange(0, T, dT)

        # Getting the correlation matrix
        Sigma = self.Sigma

        # Generating the dW array
        dB, dW1, dW2 = Utils.generate_correlated_gaussians(Sigma=Sigma)

        # Initializing the array for the underlying price and spot variance processes
        S = np.zeros(N) # Underlying price process
        V = np.zeros(N) # Spot variance process

        # Setting up the initial conditions
        S[0] = self.S0 
        V[0] = self.V0
        
        # Simulating the interest rates according to the given model
        simulated_rates = self.r.simulate_euler(T=T, N=N, dB=dB)
        simulated_rates = simulated_rates["r"]

        # Computing simultaneously the underlying price and 
        for t in range(N - 1):
            S[t + 1] = S[t] + (simulated_rates[t]*S[t])*dT + np.sqrt(V[t])*S[t]*dW1[t] #+ (1/2)*(self.sigma**2)*S[t]*(dW1[t]**2 - dT)
            V[t + 1] = V[t] + self.kappa*(self.theta - V[t])*dT + self.eta*np.sqrt(V[t])*dW2[t]

        # Check for right output
        if getRates and getVariance:
            return {"t": H, "S": S, "V": V, "r": simulated_rates}
        elif getVariance and not getRates:
            return {"t": H, "S": S, "V": V}
        elif not getVariance and getRates:
            return {"t": H, "S": S, "r": simulated_rates}
        else:
            return {"t": H, "S": S}


    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS,
                          getVariance: bool = False,
                          getRates: bool = False) -> dict:
        
        # Time step
        dT = T/float(N)

        # Generating the time horizon array
        H = np.arange(0, T, dT)

        # Getting the correlation matrix
        Sigma = self.Sigma

        # Generating the correlated Brownian motions
        # Convention:
        #   - (B_t)_t ==> Brownian motion for the underlying interest rates (Vasicek/CIR/HW)
        #   - (W^1_t)_t ==> Brownian motion for the underlying price process
        #   - (W^2_t)_t ==> Brownian motion for the spot variance process
        dB, dW1, dW2 = Utils.generate_correlated_gaussians(Sigma=Sigma)

        # Initializing the array for the underlying price and spot variance processes
        S = np.zeros(N) # Underlying price process
        V = np.zeros(N) # Spot variance process

        # Setting up the initial conditions
        S[0] = self.S0 
        V[0] = self.V0
        
        # Simulating the interest rates according to the given model
        simulated_rates = self.r.simulate_euler(T=T, N=N, dB=dB)
        simulated_rates = simulated_rates["r"]

        # Computing simultaneously the underlying price and 
        for t in range(N - 1):
            S[t + 1] = S[t] + (simulated_rates[t]*S[t])*dT + np.sqrt(V[t])*S[t]*dW1[t] + (1/2)*(dW1[t]**2 - dT)*V[t]*S[t]
            V[t + 1] = V[t] + self.kappa*(self.theta - V[t])*dT + self.eta*np.sqrt(V[t])*dW2[t]
                    
        # Check for right output
        if getRates and getVariance:
            return {"t": H, "S": S, "V": V, "r": simulated_rates}
        elif getVariance and not getRates:
            return {"t": H, "S": S, "V": V}
        elif not getVariance and getRates:
            return {"t": H, "S": S, "r": simulated_rates}
        else:
            return {"t": H, "S": S}