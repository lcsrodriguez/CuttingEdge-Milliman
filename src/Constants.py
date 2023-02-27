from enum import Enum

class Constants:
    """
    Static class for constants and global variables
    """

    # Global variables & constants
    MAX_STEPS = int(1e5)

    # Defining the available numerical schemes
    Scheme = Enum('Scheme', ["EULER", "MILSTEIN"])

