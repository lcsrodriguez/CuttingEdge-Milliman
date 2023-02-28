from .EquityModel import *
from .RatesModel import *
from .Utils import *
from .Constants import *

class BlackScholes(EquityModel):
    r""" Class representing the Black & Scholes model 
    
    $$\frac{\mathrm{d}S_t}{S_t} := r_t\mathrm{d}t + \sigma\mathrm{d}W_t$$
    """
    
    # Name of the model
    MODEL_NAME = "BLACK-SCHOLES"
    
    def __init__(self, S0: float, r: RatesModel, sigma: float) -> None:
        r"""Default constructor in order to verify the validity of the parameters, and store them

        Args:
            S0 (float): Initial value $S_0$ of the process $(S_t)_t$ at time $t = 0$
            r (RatesModel): Rate model to be used (corresponding to the $(r_t)_t$ process)
            sigma (float): Volatility (constant) parameter $\sigma \in \mathbb{R}^+$

        Raises:
            Exception: Exception raided if wrong rate model
        """
        # Verification of parameters
        assert S0 > 0 and sigma > 0
        #assert rho <= 1 and rho >= -1 # Boundaries for Brownian motions
        
        # Check if the rate model is a registered and valid model 
        if not issubclass(type(r), RatesModel): # type(r).__bases__[0] == RatesModel
            raise Exception("r must be a registered interest rates model\n(Available models: Vasicek, CIR, HW)")
                
        # Storing variables
        self.S0 = S0
        self.r = r
        self.sigma = sigma
        #self.rho = rho
        
    def __repr__(self) -> str:
        r"""Hard string representation

        Returns:
            str: Output string
        """
        return f"Black-Scholes model {self.get_parameter_string(onLaTeX=False)}"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation

        Returns:
            str: Output string
        """
        return f"Black-Scholes model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r""" Function returning a user-friendly string displaying the model parameters values

        Args:
            onLaTeX (bool, optional): Boolean value indicating if $\LaTeX$ formatting is enabled. Defaults to True.

        Returns:
            str: Output string of each parameter's value
        """
        if onLaTeX:
            return f"($S_0$ = {self.S0}, $\sigma$ = {self.sigma})"
        return f"(S0 = {self.S0}, sigma = {self.sigma})"
    
    def simulate_path(self, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
        r"""Function wrapping the 2 available simulators to simulate 1 path

        Args:
            scheme (Constants.Scheme, optional): Numerical scheme to be used. Defaults to Constants.Scheme.EULER.

        Returns:
            dict: Hashmap of results with keys `t` for time interval and `r` for rates simulation results
        """
        if scheme == Constants.Scheme.EULER:
            return self.simulate_euler(**kwargs)
        return self.simulate_milstein(**kwargs)
    
    def simulate_paths(self, M: int = 3, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
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
                sim = self.simulate_euler(**kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["r"])
            elif scheme == Constants.Scheme.MILSTEIN:
                sim = self.simulate_milstein(**kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["r"])
        return res
    
    def simulate_euler(self,
                       T: float = 1.0,
                       N: int = Constants.MAX_STEPS) -> dict:
        r"""Function implementing a path simulator following Black-Scholes model dynamics using the Euler-Maruyama method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns
        """ 
        pass
        
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS) -> dict:
        r"""Function implementing a path simulator following Black-Scholes model dynamics using the Milstein method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns

        !!! danger "Warning"
            Since $b'(.) \neq 0$, the Milstein scheme is not equivalent to the Euler scheme and a complete implementation is required !
        """ 
        pass