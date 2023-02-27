# Importing all the libraries
import numpy as np
import numpy.random as npr
import time
import warnings
import scipy
import random
import pandas as pd
import matplotlib.pyplot as plt
from enum import Enum
import missingno as msn
import QuantLib as ql
from .Constants import *

# Silencing all warnings for a better UX
warnings.filterwarnings("ignore")

# Setting up a fixed random seed for experiment purposes
npr.seed(1)


class Utils:
    r"""
    Static class for utils functions
    """
    
    @staticmethod
    def cast_df(x: dict | list | np.ndarray | pd.Series) -> pd.DataFrame:
        r"""Function to explicitly cast a dictionary or Numpy array into a **pandas** `DataFrame`

        Args:
            x (dict | list | np.ndarray | pd.Series): Input data variable

        Returns:
            pd.DataFrame: Output Pandas `DataFrame`
        """
        return pd.DataFrame(x)

    @staticmethod
    def generate_correlated_gaussians(rho: float = 0.5,
                                  T: float = 1.0,
                                  N: int = Constants.MAX_STEPS) -> np.ndarray:
        r"""Function which generates a series of two Gaussian series correlated by the given
        factor $\rho \in \left]-1, 1\right[$

        Args:
            rho (float, optional): Correlation ratio given by the user. Defaults to 0.5.
            T (float, optional): Time horizon (upper bound of the time interval). Defaults to 1.0.
            N (int, optional): Number of step in the time mesh. Defaults to Constants.MAX_STEPS.

        Returns:
            np.ndarray: 2 numpy arrays which corresponds to *Brownian increments* ($(dB_t)_t$ and $(dW_t)_t$)
        """            
        # Checking the value of rho
        assert rho < 1.0 and rho > -1.0
        
        # Creating the correlation matrix
        C = np.array([[1, rho], [rho, 1]])
        
        # Performing the Cholesky decomposition
        L = np.linalg.cholesky(C) # L is the lower triangular matrix, L.T is the upper triangular matrix
        
        # Setting up the time step
        dT = T/N
        
        # Creation of 2 Brownian motions with N steps
        X = np.random.normal(0, (dT**(1/2)), (2, N))
        
        # Compute the correlated paths
        CX = np.dot(L, X)
        
        # Checking the correlation ratio of the simulated BM
        corr_coeff = np.corrcoef(CX.cumsum(axis=1))[1][0]
        print("-------------- Generation of Brownian Motions --------------")
        print(f"Simulated rho: {corr_coeff} \tGiven rho: {rho}\nAbsolute error: {np.abs(corr_coeff - rho)}")
        
        # Return the correlated paths
        return CX
    
    @staticmethod
    def generate_correlated_brownians(*args, **kwargs) -> np.ndarray:
        r"""Function which generates a series of two Brownian motions correlated by the given
        factor $\rho \in \left]-1, 1\right[$

        Returns:
            np.ndarray: 2 numpy arrays which corresponds to *Brownian increments* ($(dB_t)_t$ and $(dW_t)_t$)
        """
        # Computing the Gaussian increments
        CX = Utils.generate_correlated_gaussians(*args, **kwargs)
        return [path.cumsum() for path in CX]