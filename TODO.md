# TODO

- OOP to handle model parameters
- Typing module
- Add descriptions for each model


## Calcul brownien

- Pour calcul des browniens, on met rho dans l'equity model (rho à mettre dans le c-tor de BS)
- puis qd simulate_path de BlackScholes, simulation de dB et dW au sein de cette fonction, (pas dans le c-tor)
- on donne dB dans simulate_path de RateModel et dW pour le calcul du schéma au sien de simulate_path de BS
- 