from .RatesModel import *
from .Utils import *
from .Constants import *

class Vasicek(RatesModel):
    r"""Class representing the Vasicek model 
    
    $$
        \left\{
        \begin{aligned}
            \mathrm{d}r_t &= \kappa(\theta - r_t)\mathrm{d}t + \eta \mathrm{d}B_t \\
            r(0) &= r_0
        \end{aligned}
        \right.
    $$
    """
    
    # Name of the model
    MODEL_NAME = "VASICEK"
    
    def __init__(self, r0: float, kappa: float, theta: float, eta: float) -> None:
        r"""Default constructor in order to verify the validity of the parameters, and store them

        Args:
            r0 (float): Initial value $r_0$ of the process $(r_t)_t$ at time $t = 0$
            kappa (float): Mean-reversion speed parameter $\kappa$s
            theta (float): Mean-reversion center parameter $\theta$
            eta (float): Volatility (constant) parameter $\eta$
        """
        # Verification
        assert r0 > 0 and kappa > 0 and theta > 0 and eta > 0
        
        # Storing variable
        self.r0 = r0
        self.kappa = kappa
        self.theta = theta
        self.eta = eta
        
    def __repr__(self) -> str:
        r"""Hard string representation

        Returns:
            str: Output string
        """
        return f"Vasicek model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation

        Returns:
            str: Output string
        """
        return f"Vasicek model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r""" Function returning a user-friendly string displaying the model parameters values

        Args:
            onLaTeX (bool, optional): Boolean value indicating if $\LaTeX$ formatting is enabled. Defaults to True.

        Returns:
            str: Output string of each parameter's value
        """ 
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $\kappa$ = {self.kappa}, $\\theta$ = {self.theta}, $\eta$ = {self.eta})"
        return f"(r0 = {self.r0}, kappa = {self.kappa}, theta = {self.theta}, eta = {self.eta})"

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
                sim = self.simulate_euler(**kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["r"])
        return res
            
    def simulate_euler(self,
                       T: float = 1.0,
                       N: int = Constants.MAX_STEPS) -> dict:
        r"""Function implementing a path simulator following Vasicek model dynamics using the Euler-Maruyama method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns
        """        
        # Time step
        dT = T/float(N)

        # Generating the time horizon array
        H = np.arange(0, T, dT)

        # Generating the dW array
        dW = np.random.normal(0, 1, N)

        # Initializing the rates array
        r = np.zeros(N)
        r[0] = self.r0

        # Computing the rates
        for t in range(N - 1):
            r[t + 1] = r[t] + self.kappa*(self.theta - r[t])*dT + self.eta*dW[t]
        return {"t": H, "r":r}
        
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS) -> dict:
        r"""Function implementing a path simulator following Vasicek model dynamics using the Milstein method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns


        !!! note
            Since $b'(.) = 0$, the Milstein scheme is equivalent to the Euler scheme
        """   
        # Since b'(.) = 0, the Milstein scheme is equivalent to the Euler scheme
        return self.simulate_euler(T, N)