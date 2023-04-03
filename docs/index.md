# Cutting-Edge project

<img src="https://img.shields.io/static/v1?label=Range&message=Academic project&color=007bff"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Languages&message=Python&color=ff0000"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Restriction&message=YES&color=26c601"/>

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lcsrodriguez/CuttingEdge-Milliman/main)&nbsp;[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lcsrodriguez/CuttingEdge-Milliman)

*Academic research project conducted between January and April 2023*

## Motivation

Insurers use economic scenarios of the main financial indicators of the state of an economy (i.e. simulated trajectories of interest rates, equity indices, etc.) to calculate a measure of risk (in other words, a quantile on the loss distribution).

Its purpose is to report on the level of risk embedded in the products in the insurer's portfolio.


Trajectories of updated equity indices are simulated using models calibrated on market prices. The joint law of the interest rate / equity index couple therefore has an impact on the quantile finally calculated. It is proposed in this subject to implement simulation schemes of some rate and equity models and to study the joint law of the rate / equity couple by simulation. Sensitivities will be carried out. A study of the impact of the parameters (models, discretization, etc.) on the quantile levels will be carried out.


A generic plan of our research project:

1. **Interest-rates** modelling $(r_t)_{t\in\mathbb{R}^+}$
    - Vasicek, CIR, Hull & White, Black-Karasinski, Ho-Lee[^1]
2. **Equity-index** modelling $(S_t)_{t\in\mathbb{R}^+}$
    - Black-Scholes with stochastic interest rates
3. **In-depth analysis** of simulation results
    - Pricing of vanilla European derivatives
    - Analysis of the distribution of $S_T$ for $T > 0$

<i>To start with this project, please follows the procedure detailed <a href="getting-started/">here</a></i>.

## About

This academic project has been conducted in association with [Milliman](https://milliman.com/) and [University of Paris-Saclay](https://www.universite-paris-saclay.fr/).

Our research group is composed of **Amal BACHA**, **Dalia BARBI**, **Khalil BATTIKH**, **Lucas RODRIGUEZ** and **Naïm SOUNI**, engineering student in the [M2 Quantitative Finance](https://www.universite-paris-saclay.fr/formation/master/mathematiques-et-applications/m2-finance-quantitative) of [University of Paris-Saclay](https://www.universite-paris-saclay.fr/).

 <div class="row">
  <div class="column">
    <img src="img/Milliman.png" alt="Milliman" style="width:100%">
  </div>
  <div class="column">
    <img src="img/UPS.png" alt="Université Paris-Saclay" style="width:80%">
  </div>
</div> 


## Bug tracker & Contribution

If you have discovered any technical issue within the source code, or you want to propose new features, feel free to open a [new issue](https://github.com/lcsrodriguez/CuttingEdge-Milliman/issues/new) or initiate a [PR](https://github.com/lcsrodriguez/CuttingEdge-Milliman/pulls). We thank you for your interest in this project.


## License

See the [LICENSE](https://github.com/lcsrodriguez/CuttingEdge-Milliman/blob/main/LICENSE) file for more information.

[^1]: Some other models can also be implemented as an extension of this current work