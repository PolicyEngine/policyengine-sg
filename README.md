# PolicyEngine Singapore

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PolicyEngine Singapore is a free, open-source microsimulation model of Singapore's tax and benefit system. It enables users to calculate taxes and benefits for individual households and analyze the distributional impacts of policy reforms.

## Features

### Comprehensive Tax Modeling
- Personal income tax with progressive brackets
- Central Provident Fund (CPF) contributions
- Goods and Services Tax (GST)
- Foreign Worker Levy (coming soon)
- Property tax (coming soon)
- Motor vehicle taxes (coming soon)

### Social Benefits and Programs
- ComCare social assistance programs
- WorkFare Income Supplement (WIS)
- CPF schemes (Healthcare, Housing, etc.)
- Senior citizen benefits (coming soon)
- Education subsidies (coming soon)

### Key Capabilities
- **Up-to-date parameters**: Latest tax rates and benefit amounts
- **Government sources**: All parameters referenced to official Singapore sources
- **Test-driven development**: Comprehensive test coverage
- **Reform analysis**: Model policy changes and impacts
- **Open source**: Transparent and auditable

## Installation

### Requirements
- Python 3.10 or higher (3.13 recommended)
- pip or uv package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/PolicyEngine/policyengine-sg.git
cd policyengine-sg

# Install with uv (recommended)
uv pip install --system -e .

# Or with pip
pip install -e .
```

### Install from PyPI (coming soon)

```bash
pip install policyengine-sg
```

## Quick Start

```python
from policyengine_sg import SingaporeTaxBenefitSystem
from policyengine_core.simulations import Simulation

# Create the tax-benefit system
system = SingaporeTaxBenefitSystem()

# Define a household
situation = {
    "people": {
        "person1": {
            "age": {"2024": 35},
            "employment_income": {"2024": 60000}
        }
    },
    "households": {
        "household": {
            "members": ["person1"]
        }
    }
}

# Run simulation
simulation = Simulation(
    tax_benefit_system=system,
    situation=situation
)

# Calculate values
income_tax = simulation.calculate("income_tax", "2024")
cpf_contributions = simulation.calculate("cpf_contributions", "2024")

print(f"Income tax: S${income_tax[0]:,.2f}")
print(f"CPF contributions: S${cpf_contributions[0]:,.2f}")
```

## Documentation

Full documentation is available at: [https://policyengine.github.io/policyengine-sg](https://policyengine.github.io/policyengine-sg)

- [Tax Programs](docs/tax-programs.md) - Detailed tax calculations
- [Benefit Programs](docs/benefit-programs.md) - Social assistance programs
- [Developer Guide](docs/developer-guide.md) - Contributing guide
- [API Reference](docs/api-reference.md) - Technical documentation

## Development

### Setting up development environment

```bash
# Install development dependencies
uv pip install --system -e .[dev]

# Run tests
uv run pytest

# Format code
make format

# Build documentation
myst build docs
```

### Running tests

```bash
# Run all tests with coverage
uv run pytest --cov=policyengine_sg

# Run specific test file
uv run pytest policyengine_sg/tests/policy/baseline/test_income_tax.yaml

# Run only unit tests
uv run pytest policyengine_sg/tests -k "not yaml"
```

## Contributing

We welcome contributions! Please see our [Developer Guide](docs/developer-guide.md) for:
- Setting up your development environment
- Adding new parameters and variables
- Writing tests
- Submitting pull requests

### Key principles
1. **Test-driven development**: Write tests first
2. **Government sources**: Reference all parameters to official sources
3. **Code quality**: Format with Black (79 chars)
4. **Documentation**: Update docs with changes

## Data and Validation

PolicyEngine Singapore is validated against:
- IRAS tax calculators
- CPF contribution calculators
- MSF benefit calculators
- Published government rate tables
- Official Singapore statistics

## License

PolicyEngine Singapore is licensed under the [GNU Affero General Public License v3.0](LICENSE).

## Citation

If you use PolicyEngine Singapore in your research, please cite:

```bibtex
@software{policyengine_singapore,
  title = {PolicyEngine Singapore},
  author = {PolicyEngine},
  year = {2024},
  url = {https://github.com/PolicyEngine/policyengine-sg}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/PolicyEngine/policyengine-sg/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PolicyEngine/policyengine-sg/discussions)
- **Email**: hello@policyengine.org
- **Website**: [policyengine.org](https://policyengine.org)

## Acknowledgments

PolicyEngine Singapore builds on:
- [OpenFisca](https://openfisca.org/) framework via PolicyEngine Core
- Singapore government data and documentation
- Open source tax-benefit modeling community

## Roadmap

### Near-term (Q1 2025)
- Complete personal income tax implementation
- Add CPF contribution calculations
- Implement GST framework
- Add ComCare social assistance

### Medium-term (Q2-Q3 2025)
- WorkFare Income Supplement
- CPF housing and healthcare schemes
- Foreign Worker Levy
- Property tax calculations

### Long-term
- Full integration with PolicyEngine web app
- Motor vehicle taxes and COE system
- Education subsidies and schemes
- Behavioral responses and dynamic scoring

---

**Note**: This model is under active development. Parameters are updated regularly to reflect policy changes. Always verify calculations against official IRAS, CPF, and MSF sources for critical applications.