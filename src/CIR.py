from .RatesModel import *
from .Utils import *
from .Constants import *
import numpy as np

class CIR(RatesModel):
    r""" Class representing the Cox-Ingersoll-Ross (CIR) model
    
    $$
    \left\{
    \begin{aligned}
        \mathrm{d}r_t &= \kappa(\theta - r_t)\mathrm{d}t + \sigma\sqrt{r_t} \mathrm{d}B_t \\
        r(0) &= r_0
    \end{aligned}
    \right.
    $$
    """

    # Name of the model
    MODEL_NAME = "CIR"
    
    def __init__(self, r0: float, kappa: float, theta: float, sigma: float) -> None:
        r"""Default constructor in order to verify the validity of the parameters, and store them

        Args:
            r0 (float): Initial value $r_0$ of the process $(r_t)_t$ at time $t = 0$
            kappa (float): Mean-reversion speed parameter $\kappa$s
            theta (float): Mean-reversion center parameter $\theta$
            sigma (float): Volatility (constant) parameter $\sigma$
        """        
        # Verification
        assert r0 > 0 and kappa > 0 and theta > 0 and sigma > 0
        
        # Verifying the Feller condition
        self.feller_condition = 2*kappa*theta >= sigma**2
        if self.feller_condition:
            print("(r_t)_t strictly positive")
        
        # Storing variables
        self.r0 = r0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        
    def __repr__(self) -> str:
        r"""Hard string representation

        Returns:
            str: Output string
        """
        return f"CIR model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        r"""
        Gentle string representation

        Returns:
            str: Output string
        """
        return f"CIR model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        r""" Function returning a user-friendly string displaying the model parameters values

        Args:
            onLaTeX (bool, optional): Boolean value indicating if $\LaTeX$ formatting is enabled. Defaults to True.

        Returns:
            str: Output string of each parameter's value
        """
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $\kappa$ = {self.kappa}, $\\theta$ = {self.theta}, $\sigma$ = {self.sigma})"
        return f"(r0 = {self.r0}, kappa = {self.kappa}, theta = {self.theta}, sigma = {self.sigma})"
    
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
                       N: int = Constants.MAX_STEPS,
                       dB: np.ndarray = None) -> dict:
        r"""Function implementing a path simulator following CIR model dynamics using the Euler-Maruyama method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.
            dB (np.ndarray, optional): Series of the Brownian increments. Defaults to None.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns
        """ 
        # Time step
        dT = T/float(N)

        # Generating the time horizon array
        H = np.arange(0, T, dT)

        # Generating the dB array
        if dB is None:
            dB = np.random.normal(0, 1, N)

        # Initializing the rates array
        r = np.zeros(N)
        r[0] = self.r0

        # Computing the rates
        for t in range(N - 1):
            #if r[t] <= 0:
            #    r[t] = np.abs(r[t])
            r[t + 1] = r[t] + self.kappa*(self.theta - r[t])*dT + self.sigma*np.sqrt(np.abs(r[t]))*dB[t]
        return {"t": H, "r": r}
        
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS,
                          dB: np.ndarray = None) -> dict:
        r"""Function implementing a path simulator following CIR model dynamics using the Euler-Maruyama method

        Args:
            T (float, optional): Time horizon. Defaults to 1.0.
            N (int, optional): Number of time step in the mesh. Defaults to Constants.MAX_STEPS.
            dB (np.ndarray, optional): Series of the Brownian increments. Defaults to None.

        Returns:
            dict: Dictionary (hashmap) with the time and generated rates columns

        !!! danger "Warning"
            Since $b'(.) \neq 0$, the Milstein scheme is not equivalent to the Euler scheme and a complete implementation is required !
        
        """ 
        
        # Time step
        dT = T/float(N)

        # Generating the time horizon array
        H = np.arange(0, T, dT)

        # Generating the dB array
        if dB is None:
            dB = np.random.normal(0, 1, N)

        # Initializing the rates array
        r = np.zeros(N)
        r[0] = self.r0

        # Computing the rates
        for t in range(N - 1):
            #print(r[t])
            r[t + 1] = r[t] \
                     + self.kappa*(self.theta - r[t])*dT  \
                     + self.sigma*np.sqrt(np.abs(r[t]))*dB[t] \
                     + (1/2)*(dB[t]**2 - dT)*(self.sigma*np.sqrt(np.abs(r[t])))*(self.sigma)/(2*np.sqrt(np.abs(r[t])))
        return {"t": H, "r": r}
        
    def plot_feller_line(self, **kwards) -> None:    
        r"""
        Function printing the Feller line to highlight the positivity of simulated rates

        Returns:
            None
        """
        if self.feller_condition:
            plt.axhline(y=0, color="m", ls="-.", alpha=0.7, **kwards, label="Feller line")
            _ = plt.legend()
    