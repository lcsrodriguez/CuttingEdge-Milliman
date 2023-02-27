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
    """
    Static class for utils functions
    """
    
    # Function to explicitly cast a dictionary or Numpy array into a pandas DataFrame
    cast_df = lambda x: pd.DataFrame(x)