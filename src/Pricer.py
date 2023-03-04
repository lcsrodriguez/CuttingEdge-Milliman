class Pricer:
    r"""Abstract class for pricers """
    pass

    @staticmethod
    def CALL_PAYOFF(x: float, K: float) -> float:
        r"""Payoff function for a call option

        $$\Pi^{\text{CALL}} := (X - K)_+$$

        Args:
            x (float): underlying price
            K (float): Strike (Exercise price)

        Returns:
            float: Call payoff
        """        
        return max(0, x - K)
    
    @staticmethod
    def PUT_PAYOFF(x: float, K: float) -> float:
        r"""Payoff function for a put option

        $$\Pi^{\text{PUT}} := (K - X)_+$$


        Args:
            x (float): underlying price
            K (float): Strike (Exercise price)

        Returns:
            float: Put payoff
        """  
        return max(0, K - x)