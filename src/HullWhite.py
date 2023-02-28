from .RatesModel import *
from .Utils import *
from .Constants import *

class HullWhite(RatesModel):
    r""" Class representing the Hull & White model
    
    $$
        \left\{
        \begin{aligned}
            \mathrm{d}r_t &= \kappa(\theta(t) - ar_t)\mathrm{d}t + \sigma\sqrt{r_t} \mathrm{d}B_t \\
            r(0) &= r_0
        \end{aligned}
        \right.
    $$
    """
        
    # Name of the model
    MODEL_NAME = "HULL-WHITE"
    
    def __init__(self, r0: float, a: float, sigma: float) -> None:
        r"""Default constructor in order to verify the validity of the parameters, and store them

        Args:
            r0 (float): Initial value $r_0$ of the process $(r_t)_t$ at time $t = 0$
            a (float): Mean-reversion center parameter $a$
            sigma (float): Volatility (constant) parameter $\sigma$
        """   
        # Verification
        assert r0 > 0 and a > 0 and sigma > 0
        
        # Storing variables
        self.r0 = r0
        self.a = a
        self.sigma = sigma
    
    def __repr__(self) -> str:
        r"""Hard string representation

        Returns:
            str: Output string
        """
        return f"Hull & White model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation

        Returns:
            str: Output string
        """
        return f"Hull & White model {self.get_parameter_string(onLaTeX=False)}"
    
    def compute_theta(self) -> np.ndarray:
        r"""
        Function computing, storing and returning the theta 
        corresponding to the fitted interest rates term structure

        !!! danger
            **TODO**
        """
        # TODO
        pass
    
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r""" Function returning a user-friendly string displaying the model parameters values

        Args:
            onLaTeX (bool, optional): Boolean value indicating if $\LaTeX$ formatting is enabled. Defaults to True.

        Returns:
            str: Output string of each parameter's value
        """
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $a$ = {self.a}, $\sigma$ = {self.sigma})"
        return f"(r0 = {self.r0}, a = {self.a}, sigma = {self.sigma})"    