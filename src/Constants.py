from enum import Enum

class Constants:
    r"""
    Static class for constants and global variables
    """

    # Global variables & constants
    MAX_STEPS = int(2e4)

    # Monte-Carlo pricing iterations
    MC_DEFAULT_ITERS = int(5e2)

    # Defining the available numerical schemes
    Scheme = Enum("Scheme", ["EULER", "MILSTEIN"])

    # Defining the available numerical schemes
    Contract = Enum("Contract", ["CALL", "PUT"])

    # Z-score for Monte-Carlo confidence intervals
    Z_SCORES = {
        80: 1.282,
        85: 1.440,
        90: 1.645,
        95: 1.960,
        99: 2.576,
        99.5: 2.807,
        99.9: 3.291
    }
    # Reference: https://www.alchemer.com/resources/blog/how-to-calculate-confidence-intervals/
    
    # Available Confidence interval levels
    AVAILABLE_CI_LEVELS = list(Z_SCORES.keys())

    # Enumeration of available levels
    Level = Enum("Level", dict((f"LEVEL_{str(k).replace('.', '_')}", k) for k in list(Z_SCORES.keys())))

    # Pool of available functions to avoid negative interest-rates generation through CIR model
    CIR_HELPER_FUNCTIONS = {
        "ABSOLUTE": lambda x: abs(x),
        "MAX_0": lambda x: max(0, x)
    }

    # Strategy to compute the values of $t \longmapsto \theta(t)$
    THETA_STRATEGIES = Enum("THETA", ["MARKET_ZC_PRICE", "SCENARIO"])