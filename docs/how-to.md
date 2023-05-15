# How To ...

This page gathers several takeaways Python snippets and features from this project.

## Simulate an interest rate trajectory

Example for *Vasicek* model

```python hl_lines="2"
# Default Vasicek model
model = Vasicek(0.01875, 0.20, 0.01, 0.012) # r0, kappa, theta, sigma

# Displaying information on Vasicek model
model

# Casting the results into a pandas DataFrame
df = Utils.cast_df(model.simulate_euler(T=3, N = 1000))

# Simulation of a trajectory
_ = df.plot(figsize=(12, 6), color="blue", x="t", y ="r", label="$(r_t)_t$")
_ = plt.grid()
_ = plt.xlabel("Time ($t$)")
_ = plt.ylabel("Interest rates")
_ = plt.title(f"Simulation of 1 path of Vasicek model\n{model.get_parameter_string()}")
_ = plt.legend()
```

<div class="img-demo">
    <img src="../img/screens/vasicek.png">
</div>


### Simulate $k \in \mathbb{N}^*$ trajectories

In this example, we set $k := 8$

```python hl_lines="2"
# Simulation of several trajectories
NB_TRAJECTORIES = 8
_ = Utils.cast_df(model.simulate_paths(NB_TRAJECTORIES, T = 2)).T.plot(x = 0, y = list(range(1, NB_TRAJECTORIES + 1)), figsize=(12, 6))
_ = plt.grid()
_ = plt.xlabel("Time ($t$)")
_ = plt.ylabel("Interest rates")
_ = plt.title(f"Simulation of {NB_TRAJECTORIES} paths of Vasicek model\n{model.get_parameter_string()}")
_ = plt.legend()
```

<div class="img-demo">
    <img src="../img/screens/vasicek_multi.png">
</div>

## Simulate $l$ correlated Brownian motions paths

Let $l \leq 2$, be the number of Brownian motions to be generated with a given correlation matrix $\Sigma \in \mathcal{S}_n^+$


!!! note
    In the case of $l = 2$, one allows the user to only pass a correlation coefficient $\rho \in \left]-1, +1\right[$.

    $$
    \Sigma := \begin{bmatrix}
        1 & \rho\\
        \rho & 1
        \end{bmatrix}$$
    
    *The correlation matrix will then be build inside the function*


## Simulate an equity-index trajectory *with stochastic IR*

```python
S0 = 1
sigma = 0.7
rho = 0.5
r = CIR(0.4, 0.20, 0.01, 0.12) # Vasicek(0.01875, 0.20, 0.01, 0.014)
model = BlackScholes(S0, r, sigma, rho)
```

```python
d = model.simulate_euler(T=4.2, getRates=True)
df = pd.DataFrame(d)
df.head()
```

```python
# Plotting the asset price and the interest rates evolution over time 
_, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 8))
_ = df.plot(x = "t", y = "S", color="blue", label="Price $(S_t)_t$", ax=axes[0])
_ = axes[0].axhline(y = model.S0, color="green", ls="--", lw=1, alpha=0.7, label="Init. cond. $(S_0)$")
_ = df.plot(x = "t", y = "r", color="red", label="Interest rates $(r_t)_t$", ax=axes[1])
_ = axes[1].axhline(y = r.r0, color="green", ls="--", lw=1, alpha=0.7, label="Init. cond. $(r_0)$")
axes[0].legend()
axes[1].legend()
_ = plt.suptitle(f"Asset price $(S_t)$ and underlying rates $(r_t)$ with\n{r.MODEL_NAME}{r.get_parameter_string()} & {model.get_parameter_string()}")
```

<div class="img-demo">
    <img src="../img/screens/bs.png">
</div>

## Pricing an option 

!!! warning
    Currently, the library only contains fully-implemented/tested **European** and **Asian** option pricers.


First, we have to define our models respectively for interest rates & equity modelling.


```python
# Model parameters
S0 = 4
sigma = 0.7
rho = 0.5
r = CIR(0.4, 0.20, 0.01, 0.12) # Vasicek(0.01875, 0.20, 0.01, 0.014)
model = BlackScholes(S0, r, sigma, rho)
```

### EURO

```python
# Define the European pricer
ep = EuropeanPricer(udl_model=model, preCompute=True, N_MC=10)
```

```python
# Boolean representing whether the simulations have already been simulated
ep.isSimulated
```

```python
K = 3.3
# Call price
pricer_res = ep.compute_option_price(K=K, 
                                     contract=Constants.Contract.CALL, 
                                     ci_levels=[
                                         Constants.Level.LEVEL_80, 
                                         Constants.Level.LEVEL_85, 
                                         Constants.Level.LEVEL_90,
                                         Constants.Level.LEVEL_95,
                                         Constants.Level.LEVEL_99_9
                                     ])
pricer_res
```


```python
# Plot confidence intervals
Utils.plot_confidence_intervals(pricer_res)
```

Computing CALL & PUT prices

```python
# Call price
ep.compute_option_price_call(K)

# Put price
ep.compute_option_price_put(K)
```

### ASIA


```python
# Define the Asian pricer
ap = AsianPricer(udl_model=model, preCompute=True, N_MC=10)
```

```python
K = 1
# Call price
ap.compute_option_price(K=K, contract=Constants.Contract.CALL)
```

```python
# Call price
ap.compute_option_price_call(K)

# Put price
ap.compute_option_price_put(K)
```

## Plot 

Example below with the European option pricer

<div class="img-demo">
    <img src="../img/screens/CI_levels.png">
</div>
