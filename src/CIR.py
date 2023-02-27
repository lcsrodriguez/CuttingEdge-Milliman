from .RatesModel import *
from .Utils import *
from .Constants import *

class CIRModel(RatesModel):
    """ Class representing the Cox-Ingersoll-Ross (CIR) model """
    
    MODEL_NAME = "CIR"
    
    def __init__(self, r0: float, kappa: float, theta: float, sigma: float) -> None:
        """
        Default constructor in order to verify the validity of the parameters, and store them
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
        """
        Hard string representation
        """
        return f"CIR model {self.get_parameter_string(onLaTeX=False)})"
    
    def __str__(self) -> str:
        """
        Gentle string representation
        """
        return f"CIR model {self.get_parameter_string(onLaTeX=False)}"
  
    def get_parameter_string(self, onLaTeX: bool = True) -> str:
        """
        Function returning a user-friendly string displaying the model parameters values
        """
        if onLaTeX:
            return f"($r_0$ = {self.r0}, $\kappa$ = {self.kappa}, $\\theta$ = {self.theta}, $\sigma$ = {self.sigma})"
        return f"(r0 = {self.r0}, kappa = {self.kappa}, theta = {self.theta}, sigma = {self.sigma})"
    
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
                sim = self.simulate_milstein(**kwargs)
                if m == 1:
                    res.append(sim["t"])
                res.append(sim["r"])
        return res
    
    def simulate_euler(self,
                       T: float = 1.0,
                       N: int = Constants.MAX_STEPS) -> dict:
        """
        Function implementing a path simulator following CIR model dynamics
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
            #if r[t] <= 0:
            #    r[t] = np.abs(r[t])
            r[t + 1] = r[t] + self.kappa*(self.theta - r[t])*dT + self.sigma*np.sqrt(np.abs(r[t]))*dW[t]
        return {"t": H, "r":r}
        
    def simulate_milstein(self,
                          T: float = 1.0,
                          N: int = Constants.MAX_STEPS) -> dict:
        """
        Function implementing a path simulator following CIR model dynamics
        using the Milstein method
        Returns a dictionary (hashmap) with the time and generated rates columns
        """
        # Since b'(.) <> 0, the Milstein scheme is not equivalent to the Euler scheme
        # and a complete implementation is required !
        
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
            #print(r[t])
            r[t + 1] = r[t] \
                     + self.kappa*(self.theta - r[t])*dT  \
                     + self.sigma*np.sqrt(np.abs(r[t]))*dW[t] \
                     + (1/2)*(dW[t]**2 - dT)*(self.sigma*np.sqrt(np.abs(r[t])))*(self.sigma)/(2*np.sqrt(np.abs(r[t])))
        return {"t": H, "r":r}
        
    def plot_feller_line(self, **kwards) -> None:
        """
        Function printing the Feller line to highlight the positivity of simulated rates
        """
        if self.feller_condition:
            plt.axhline(y=0, color="m", ls="-.", alpha=0.7, **kwards, label="Feller line")
            _ = plt.legend()
    