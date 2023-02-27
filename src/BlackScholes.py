from .EquityModel import *
from .RatesModel import *
from .Utils import *
from .Constants import *

class BlackScholes(EquityModel):
    r""" Class representing the Black & Scholes model """
    
    # Name of the model
    MODEL_NAME = "BLACK-SCHOLES"
    
    def __init__(self, S0: float, r: RatesModel, sigma: float, rho: float) -> None:
        r"""
        Default constructor in order to verify the validity of the parameters, and store them
        """
        # Verification of parameters
        assert S0 > 0 and sigma > 0
        assert rho <= 1 and rho >= -1 # Boundaries for Brownian motions
        
        # Check if the rate model is a registered and valid model 
        if not issubclass(type(r), RatesModel): # type(r).__bases__[0] == RatesModel
            raise Exception("r must be a registered interest rates model\n(Available models: Vasicek, CIR, HW)")
                
        # Storing variables
        self.S0 = S0
        self.r = r
        self.sigma = sigma
        self.rho = rho
        
    def __repr__(self) -> str:
        r"""
        Hard string representation
        """
        return f"Black-Scholes model {self.get_parameter_string(onLaTeX=False)}"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation
        """
        return f"Black-Scholes model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r"""
        Function returning a user-friendly string displaying the model parameters values
        """
        if onLaTeX:
            return f"($S_0$ = {self.S0}, $\sigma$ = {self.sigma})"
        return f"(S0 = {self.S0}, sigma = {self.sigma})"
    
    def simulate_path(self, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
        r"""
        Function wrapping the 2 available simulators to simulate 1 path
        """
        if scheme == Constants.Scheme.EULER:
            return self.simulate_euler(**kwargs)
        return self.simulate_milstein(**kwargs)
    
    def simulate_paths(self, M: int = 3, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
        r"""
        Function wrapping the 2 available simulators to simulate several paths
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
        r"""
        Function implementing a path simulator following Black-Scholes model dynamics
        using the Euler-Maruyama method
        Returns a dictionary (hashmap) with the time and generated asset price columns
        """
        pass
        
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS) -> dict:
        r"""
        Function implementing a path simulator following Black-Scholes model dynamics
        using the Milstein method
        Returns a dictionary (hashmap) with the time and generated asset price columns
        """
        pass