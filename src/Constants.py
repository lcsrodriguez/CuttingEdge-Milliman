from enum import Enum

class Constants:
    r"""
    Static class for constants and global variables
    """

    # Global variables & constants
    MAX_STEPS = int(1e5)

    # Monte-Carlo pricing iterations
    MC_DEFAULT_ITERS = int(5e2)

    # Defining the available numerical schemes
    Scheme = Enum("Scheme", ["EULER", "MILSTEIN"])

    # Defining the available numerical schemes
    Contract = Enum("Contract", ["CALL", "PUT"])

