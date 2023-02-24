# Cutting-Edge Project - Milliman

<img src="https://img.shields.io/static/v1?label=Range&message=Academic project&color=007bff"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Languages&message=Python&color=ff0000"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Restriction&message=YES&color=26c601"/>

## Overview

*Project conducted in collaboration with [Milliman](https://www.milliman.com/en/)*.


## Architecture

```mermaid
  graph TD;
      Model --> RatesModel
      Model --> EquityModel
      RatesModel --> VasicekModel
      RatesModel --> CIRModel
      RatesModel --> HullWhiteModel
      EquityModel --> BlackScholesModel
```

## Getting started

```bash
python3 --version
pip3 -V
pip3 install -r requirements.txt
```

## References

## License

[See `LICENSE` file](LICENSE)
- **Amal BACHA - Dalia BARBI - Khalil BATTIKH - Lucas RODRIGUEZ - Naïm SOUNI**
- *Academic works (January 2023 - Present)*
