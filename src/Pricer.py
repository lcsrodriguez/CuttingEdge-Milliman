from .Constants import *
from .Utils import *
import numpy
import pandas 

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
    

    def simulate_samples_parallel(self, N_MC: int, N_PROC: int) -> pandas.DataFrame:
        r"""Function simulating prices trajectories

        Args:
            N_MC (int): Number of Monte-Carlo trajectories
            N_PROC (int): Number of processes to be spawned

        Returns:
            pandas.DataFrame: Trajectories results
        """

        # Computing the workload ratio per process
        WORKLOAD_PER_PROCESS: int = int(N_MC//N_PROC)
        print(f"# proc.: {N_PROC} \t # sim.: {N_MC} \t Workload pp: {WORKLOAD_PER_PROCESS}")

        # Array containing the results from each job's execution
        results = []
        
        # Declaring 1 queue for each process
        queues = [multiprocessing.Queue() for _ in range(N_PROC)]
        
        # Declaring arguments
        args = [(WORKLOAD_PER_PROCESS, True, queues[i]) for i in range(N_PROC)]
        
        # Declaring 1 job for each process
        jobs = [multiprocessing.Process(target=self.simulate_samples, args=(a)) for a in args]

        for i, j in enumerate(jobs): 
            print(f"Starting {i}")
            j.start()

        for i, q in enumerate(queues): 
            print(f"Getting {i}")
            results.append(q.get())

        for i, j in enumerate(jobs): 
            print(f"Waiting {i}")
            j.join()

        # Aggregating the results
        S = results
        return S

    def simulate_samples(self, N_MC: int = Constants.MC_DEFAULT_ITERS, parallel: bool = False, q: Any = None) -> pandas.DataFrame: # trajectories to be stored (for caching)
        r"""Function which simulates prices trajectories

        Args:
            N_MC (int, optional): Number of Monte-Carlo trajectories to be simulated. Defaults to Constants.MC_DEFAULT_ITERS.

        Returns:
            pd.DataFrame: Trajectories
        """
        
        # Updating N_MC if different
        self.N_MC = N_MC
        #print(N_MC)
        # Simulating the trajectories necessary to Monte-Carlo
        trajectories = []
        if parallel:
            #print(f"PARA: {N_MC}")
            R = range(N_MC)
            for i in R:
                trajectories.append(self.model.simulate_euler(getRates=True))
        else:
            R = trange(N_MC, colour="red", desc="Sim. progress")
            for i in R:
                R.set_description(f"Iteration #{i}/{N_MC}")
                trajectories.append(self.model.simulate_euler(getRates=True))

        # Casting it into pandas DataFrames for a better handling (using slicing)
        trajectories = [Utils.cast_df(k) for k in trajectories]

        # Storing the results
        self.trajectories = trajectories
        self.isSimulated = True

        # Checking whether parallelism is activated
        if parallel:
            # If parallel simulator activated, we put the simulated trajectories into the given Queue
            q.put(self.trajectories)
        else:
            # Otherwise, use of serial simulator by returning the trajectories
            return self.trajectories

    def compute_option_price(self, K: float, 
                             contract: Constants.Contract = Constants.Contract.CALL,
                             ci_levels: Union[List[Constants.Level], Constants.Level] = Constants.Level.LEVEL_95,
                             N_MC: int = Constants.MC_DEFAULT_ITERS) -> float:
        r"""_summary_

        Args:
            K (float): _description_
            contract (Constants.Contract, optional): _description_. Defaults to Constants.Contract.CALL.
            ci_levels (Union[List[Constants.Level], Constants.Level], optional): _description_. Defaults to Constants.Level.LEVEL_95.
            N_MC (int, optional): _description_. Defaults to Constants.MC_DEFAULT_ITERS.

        Returns:
            float: _description_
        """
        # TO BE OVERLOADED
        pass

    def compute_option_price_call(self, K: float, *args, **kwargs) -> float:
        r"""Function computing and returning the call option price thanks to a Monte-Carlo simulation

        Args:
            K (float): Strike price (Exercise price)

        Returns:
            float: Call option price
        """        
        return self.compute_option_price(K=K, contract=Constants.Contract.CALL, *args, **kwargs)

    def compute_option_price_put(self, K: float, *args, **kwargs) -> float:
        r"""Function computing and returning the put option price thanks to a Monte-Carlo simulation

        Args:
            K (float): Strike price (Exercise price)

        Returns:
            float: Put option price
        """       
        return self.compute_option_price(K=K, contract=Constants.Contract.PUT, *args, **kwargs)
    
    def get_MC_convergence_evolution(self, K: float, N_MC_values: Union[numpy.ndarray, List[float]], contract: Constants.Contract = Constants.Contract.CALL, *args, **kwargs) -> pandas.DataFrame:
        r"""Function executing the pricer for each value given in `N_MC_values`

        Args:
            K (float): Strike price (Exercise price)
            N_MC_values (Union[numpy.ndarray, List[float]]): Array containing the $N_{MC}$ values (number of simulations) to be tested
            contract (Constants.Contract, optional): Contract option type (PUT or CALL). Defaults to Constants.Contract.CALL.

        Returns:
            pd.DataFrame: Pandas DataFrame containing the results for each value of $N_{MC}$ 
        """

        # Declaring the results hashmap
        data = {N_MC: {"price": None, "ci": None, "exec_time": None} for N_MC in N_MC_values}
        
        for N_MC in N_MC_values:
            print(f"Processing:\t {N_MC}")
            
            # Setting the isSimulated boolean to False
            self.isSimulated = False
            
            # Computing the call price using Monte-Carlo simulation
            start_time = time.time()
            pricer_res = self.compute_option_price(K=K, 
                                                contract=contract, 
                                                N_MC=N_MC,
                                                *args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            # Retrieving the output from computations
            price, ci = Utils.get_dict_values(pricer_res)
            data[N_MC]["price"] = price
            data[N_MC]["ci"] = ci
            data[N_MC]["exec_time"] = duration

        # Returning the 
        return data