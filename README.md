# Cutting-Edge Project - Milliman

<img src="https://img.shields.io/static/v1?label=Range&message=Academic project&color=007bff"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Languages&message=Python&color=ff0000"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Restriction&message=YES&color=26c601"/>

## Overview

*Project conducted in collaboration with [Milliman](https://www.milliman.com/en/)*.


## Architecture

The dependence tree below shows the links between each declared class in the source code.

```mermaid
  graph TD;
      Model --> RatesModel
      Model --> EquityModel
      RatesModel --> VasicekModel
      RatesModel --> CIRModel
      RatesModel --> HullWhiteModel
      EquityModel --> BlackScholesModel
```

**Remark**: `Model`, `RatesModel` and `EquityModel` are *abstract* classes and do not contain any implemented methods.

## Getting started

```bash
python3 --version
pip3 -V
pip3 install -r requirements.txt
```

## References

1. Ioane MUNI-TOKE, *Modèles stochastiques de taux d’intérêts*, 2011
2. Lionel GABET, Frédéric ABERGEL, Ioane MUNI-TOKE, *Introduction aux mathématiques financières*, 2010


## License

[See `LICENSE` file](LICENSE)
- **Amal BACHA - Dalia BARBI - Khalil BATTIKH - Lucas RODRIGUEZ - Naïm SOUNI**
- *Academic works (January 2023 - Present)*
