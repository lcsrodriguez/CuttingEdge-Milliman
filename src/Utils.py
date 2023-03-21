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
from tqdm.notebook import trange, tqdm
from typing import List, Union, Any

# Silencing all warnings for a better UX
warnings.filterwarnings("ignore")

# Setting up a fixed random seed for experiment purposes
npr.seed(1)


class Utils:
    r"""
    Static class for utils functions
    """
    
    @staticmethod
    def get_dict_values(x: dict) -> Any:
        r"""Function taking a random dictionary and unpacking it by returning its values

        Args:
            x (dict): Dictionary (Hashmap)

        Returns:
            Any: Values
        """
        return x.values()
    
    @staticmethod
    def plot_confidence_intervals(pricer_res: dict) -> None:
        r"""Function plotting the confidence intervals and the price from a given pricer

        Args:
            pricer_res (dict): Resulting hashtable of a pricer

        Returns:
            None: No return (only plot on stdout)
        """
        # Getting pricer & confidence interval
        price, ci = Utils.get_dict_values(x=pricer_res)

        plt.figure(figsize=(10, 5))

        # Declaring color for 
        colors = ["green", "blue", "purple", "orange", "magenta"]

        # Plotting the price line
        plt.axvline(x=price, color="red", label="MC price")

        # Removing the y-ticks
        plt.yticks([], [])

        # For each confidence interval level computed during the pricing step
        for i, ci_level in enumerate(ci.items()):
            # Getting the CI level and the upper/lower boundaries
            ci_level_ = ci_level[0]
            boundaries = ci_level[1]
            
            # Plotting for each CI, the upper and lower boundaries
            plt.axvline(x = boundaries["lower"], color=colors[i], label=f"CI {ci_level_}%", ls="-.")
            plt.axvline(x = boundaries["upper"], color=colors[i], ls="-.")
            
            # Defining the limits of the x-axis
            plt.xlim([boundaries["lower"] - 0.5, boundaries["upper"] + 0.5])
            #print(ci_level)

        # Setting the plotting options
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Markers")  
        plt.title("Confidence intervals distribution for Monte-Carlo pricing")
        plt.grid()

        return None

    @staticmethod
    def get_level_values(x: List[Constants.Level]) -> Union[List[int], List[float], List[Union[int, float]]]:
        r"""Function returning the list of the CI level values

        Args:
            x (List[Constants.Level]): List of CI levels

        Returns:
            Union[List[int], List[float], List[Union[int, float]]]: List of level values
        """
        return [level.value for level in x]

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
                                      N: int = Constants.MAX_STEPS,
                                      verbose: bool = False) -> np.ndarray:
        r"""Function which generates a series of two Gaussian series correlated by the given
        factor $\rho \in \left]-1, 1\right[$

        Args:
            rho (float, optional): Correlation ratio given by the user. Defaults to 0.5.
            T (float, optional): Time horizon (upper bound of the time interval). Defaults to 1.0.
            N (int, optional): Number of step in the time mesh. Defaults to Constants.MAX_STEPS.
            verbose (bool, optional): Boolean to verbose. Defaults to False.

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
        if verbose:
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
    
    @staticmethod
    def generate_ndim_correlated_gaussians(mu: np.ndarray,
                                           sigma: np.ndarray, 
                                           T: float = 1.0, 
                                           N: int = Constants.MAX_STEPS, 
                                           verbose: bool = False) -> np.ndarray:
        r"""Function which generates a series of two Gaussian series correlated by the given
        vector of means : $\mu \in \mathbb{R}^n$ and correlation matrix $\Sigma \in \mathcal{S}_n$

        The underlying algorithm generates samples of increments from a correlated Brownian motion with a given mean $\mu$ and Variance-Covariance matrix $\Sigma$.
        
        The algorithm uses the fact that if you have $n$ independent brownian motions, the samples given by $\mu + C\times Z$ are distributed as $\mathcal{N}(\mu,\Sigma)$, where:
        
        - $Z \sim \mathcal{N}(0, 1)$ *(Gaussian variate)*
        - $\mu$ is the vector of means
        - $C$ is the square root of the Variance-Covariance matrix.

        $$C = \Sigma^{\frac{1}{2}}$$

        To compute the square root of the variance-covariance matrix $C$, the **Cholesky decomposition** is implemented.


        Args:
            mu (np.ndarray): Vector of means given by the user
            sigma (np.ndarray): Correlation matrix given by the user
            T (float, optional): Time horizon (upper bound of the time interval). Defaults to 1.0.
            N (int, optional): Number of step in the time mesh. Defaults to Constants.MAX_STEPS.
            verbose (bool, optional): Boolean to verbose. Defaults to False.

        Returns:
            np.ndarray: $n \in \mathbb{N}^+$ numpy arrays which corresponds to *Brownian increments* ($(dW^1_t)_t, \ldots, (dW^n_t)_t$)
        """
        pass