# spacebud

`spacebud` is a Python package for creating performance budgets following the ECSS‐E‐ST‐60‐10C standard, commonly used in space engineering projects.

## Features

- Simplifies performance budget creation aligned with ECSS‐E‐ST‐60‐10C.
- Supports standard performance error indices APE, MPE, RPE, PDE, PRE, and knowledge error indices AKE, MKE, RKE.
- Temporal, ensemble, or mixed interpretation of requirements.

## Installation

Install `spacebud` using pip:

```bash
pip install spacebud
```

## Usage

Here is a toy example of how to use `spacebud`:

Consider: 
* Array of temperature sensors reading on a time scale of 0.1
* Each sensor has white readout noise (Gaussian) where the readout noise level is around 2.0, but it depends on the sensor with a uniform ensemble distribution. 
* Each sensor has an unknown bias value which is fixed over time and the value is uniformly distributed according to supplier specification

```python
from spacebud import Budget, Gaussian

# Create a new performance budget
budget = Budget(name="Radiometric Uncertainty")

# Add contributor to the budget
budget.add(name="Sensor Noise", timescale=0.1, temporal_distribution=Gaussian(sigma=Uniform(1.8, 2.2)))
budget.add(name="Sensor Bias", timescale='inf', temporal_distribution=Fixed(value=Uniform(-0.1, 0.1)))

# Generate a report
report = budget.report()
print(report)
```

## Documentation

For documentation, visit [spacebud documentation](https://github.com/himbeles/spacebud).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

