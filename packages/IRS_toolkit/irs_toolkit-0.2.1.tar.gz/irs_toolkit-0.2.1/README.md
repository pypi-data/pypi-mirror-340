# IRS Toolkit

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style - Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)

## Table of Contents

1. [Installation](#installation)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Example of usage](#example-of-usage)
5. [Documentation](#documentation)
6. [Future Work](#future-work)

## Installation

### Requirements 
- Python 3.9 or higher (up to Python 3.12)

### Quick install 
It is published on PyPI. To install, run:

```bash
pip install IRS_toolkit
```

## Features

The Financial Toolkit Library provides a comprehensive suite of tools for financial calculations and analysis. Here's a detailed breakdown of the main features:

### Interest Rate Swap (IRS) Valuation
- **Swap Pricing** ([`core/swap.py`](IRS_toolkit/core/swap.py)): Calculate present value and fair value of interest rate swaps
- **Cash Flow Analysis** ([`core/cash_flow.py`](IRS_toolkit/core/cash_flow.py)): Generate and analyze swap cash flows
- **Swap Legs** ([`core/leg/`](IRS_toolkit/core/leg/)): Handle different types of swap legs and their characteristics

### Curve Analysis
- **Yield Curve Construction** ([`core/curve/yield_curve.py`](IRS_toolkit/core/curve/yield_curve.py)): Build and manipulate yield curves from market data with overnight rate integration
- **Compounded Rates** ([`core/curve/compounded.py`](IRS_toolkit/core/curve/compounded.py)): Handle compounded rate calculations
- **Bootstrapping**: Implement bootstrapping algorithms for zero-coupon rates
- **Forward Rates**: Calculate forward rates 


### Additional Features
- **Date Handling**: Comprehensive date manipulation and business day conventions
- **Documentation**: Detailed documentation and usage examples
- **Testing**: Comprehensive unit test suite for all major functionalities


## Project Structure

```
financial-toolkit-library/
├── IRS_toolkit/          # Main package source code
│   ├── core/            # Core functionality
│   │   ├── curve/      # Yield curve implementations
│   │   ├── leg/        # Swap leg implementations
│   │   ├── swap.py     # Swap pricing
│   │   └── cash_flow.py # Cash flow analysis
│   ├── utils/          # Utility functions
│   └── options/        # Options pricing
├── docs/               # Documentation files
├── examples/           # Example notebooks and scripts
├── tests/             # Unit test suite
├── pyproject.toml     # Project dependencies and metadata
└── mkdocs.yml        # Documentation configuration
```

## Example of usage 

### Build your yield curve

```python

# Import packages
from IRS_toolkit.core.curve import yield_curve
from datetime import datetime 

# Input data
list_tenor = ['1D', '2D', '1W', '2W', '3W', '1M', '2M', '3M', '6M', '7M', '8M', '9M', '1Y', '15M', '18M', '21M', '2Y','3Y']
rates = [0.02, 0.021, 0.022, 0.023, 0.025, 0.027, 0.03, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039, 0.04, 0.041, 0.045]
curve_date = datetime(2025,3,10)

# Set the curve
curve_tool = yield_curve.YieldCurve(
        list_tenor=list_tenor,
        list_rate=rates,
        date_curve=curve_date,
        date_convention="ACT/360",
    )

#Bootstrap yield curve
curve_tool.bootstrap("quarterly")

# Visualize dataframe
curve_tool.df
```

## Documentation

The documentation is built using MkDocs. To view it, run:

```bash
mkdocs serve
```

## Future Work
The next planned improvements that can be added to this library are:
* Improvement of yield curve construction by adding other conventions and multi-curve framework
* Pricing of swaptions 
* Expanding documentation