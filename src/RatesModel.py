from .Model import Model
from .Constants import *

class RatesModel(Model):
    r""" Abstract class for Interest rates models """
    def simulate_euler(self,
                    T: float = 1.0,
                    N: int = Constants.MAX_STEPS) -> dict:
        pass