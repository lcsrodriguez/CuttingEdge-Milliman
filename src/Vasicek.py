from .RatesModel import *
from .Utils import *
from .Constants import *

class Vasicek(RatesModel):
    """ Class representing the Vasicek model """
    
    MODEL_NAME = "VASICEK"
    
    def __init__(self, r0: float, kappa: float, theta: float, eta: float) -> None:
        """
        Default constructor in order to verify the validity of the parameters, and store them
        """
        # Verification
        assert r0 > 0 and kappa > 0 and theta > 0 and eta > 0
        
        # Storing variable
        self.r0 = r0
        self.kappa = kappa
        self.theta = theta
        self.eta = eta
        
    def __repr__(self) -> str:
        """
        Hard string representation
        """
        return f"Vasicek model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        """
        Gentle string representation
        """
        return f"Vasicek model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        """
        Function returning a user-friendly string displaying the model parameters values
        """
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $\kappa$ = {self.kappa}, $\\theta$ = {self.theta}, $\eta$ = {self.eta})"
        return f"(r0 = {self.r0}, kappa = {self.kappa}, theta = {self.theta}, eta = {self.eta})"

    def simulate_path(self, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
        """
        Function wrapping the 2 available simulators to simulate 1 path
        """
        if scheme == Constants.Scheme.EULER:
            return self.simulate_euler(**kwargs)
        return self.simulate_milstein(**kwargs)
    
    def simulate_paths(self, M: int = 3, scheme: Constants.Scheme = Constants.Scheme.EULER, **kwargs) -> dict:
        """
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
                sim = self.simulate_euler(**kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["r"])
        return res
            
    def simulate_euler(self,
                       T: float = 1.0,
                       N: int = Constants.MAX_STEPS) -> dict:
        """
        Function implementing a path simulator following Vasicek model dynamics
        using the Euler-Maruyama method
        Returns a dictionary (hashmap) with the time and generated rates columns
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
        """
        Function implementing a path simulator following Vasicek model dynamics
        using the Milstein method
        Returns a dictionary (hashmap) with the time and generated rates columns
        """
        # Since b'(.) = 0, the Milstein scheme is equivalent to the Euler scheme
        return self.simulate_euler(T, N)