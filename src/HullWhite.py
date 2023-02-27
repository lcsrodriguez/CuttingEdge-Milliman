from .RatesModel import *
from .Utils import *
from .Constants import *

class HullWhiteModel(RatesModel):
    """ Class representing the Hull & White model """
    
    MODEL_NAME = "HULL-WHITE"
    
    def __init__(self, r0: float, a: float, sigma: float) -> None:
        """
        Default constructor in order to verify the validity of the parameters, and store them
        
        Arguments:
        ---------
        r0: float
            Initial condition
        
        a: float
            Mean-reversion factor
        
        sigma: float
            Volatility factor
        """
        # Verification
        assert r0 > 0 and a > 0 and sigma > 0
        
        # Storing variables
        self.r0 = r0
        self.a = a
        self.sigma = sigma
    
    def __repr__(self) -> str:
        """
        Hard string representation
        """
        return f"Hull & White model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        """
        Gentle string representation
        """
        return f"Hull & White model {self.get_parameter_string(onLaTeX=False)}"
    
    def compute_theta(self) -> np.ndarray:
        """
        Function computing, storing and returning the theta 
        corresponding to the fitted interest rates term structure
        """
        # TODO
        pass
    
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        """
        Function returning a user-friendly string displaying the model parameters values
        """
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $a$ = {self.a}, $\sigma$ = {self.sigma})"
        return f"(r0 = {self.r0}, a = {self.a}, sigma = {self.sigma})"
    
    # TODO: Add Euler !
    
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS) -> dict:
        """
        Function implementing a path simulator following Hull & White model dynamics
        using the Milstein method
        Returns a dictionary (hashmap) with the time and generated rates columns
        """
        # Since b'(.) = 0, the Milstein scheme is equivalent to the Euler scheme
        return self.simulate_euler(T, N)
    
    