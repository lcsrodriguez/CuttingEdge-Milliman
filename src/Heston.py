from .EquityModel import *
from .RatesModel import *
from .Utils import *
from .Constants import *

class Heston(EquityModel):
    r"""Class representing the Heston model *(stochastic volatility)*
    
    $$\frac{\mathrm{d}S_t}{S_t} := r_t\mathrm{d}t + \sqrt{V_t}\mathrm{d}W_t$$

    and

    $$\mathrm{d}V_t := \kappa(\theta - V_t)\mathrm{d}t + \eta\sqrt{V_t}\mathrm{d}\widetilde{W_t}$$

    """
    
    # Name of the model
    MODEL_NAME = "HESTON"