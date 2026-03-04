# PolicyEngine Singapore

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PolicyEngine Singapore is a free, open-source microsimulation model of Singapore's tax and benefit system. It enables users to calculate taxes and benefits for individual households and analyze the distributional impacts of policy reforms.

## What's Included

### Taxes
- **Personal income tax** — 13 progressive brackets (0-24%), 13 relief types, PIT and PTR rebates
- **CPF contributions** — Employee and employer rates across 5 age bands (2024-2025)
- **Property tax** — Owner-occupied and non-owner-occupied rates
- **Stamp duties** — BSD (6 brackets), ABSD (7 buyer profiles), SSD (3 holding periods)
- **GST** — 9% on taxable consumption
- **Skills Development Levy** — Employer payroll levy

### Benefits and Transfers
- **GSTV** — Cash, U-Save, MediSave, and S&CC rebates
- **CDC Vouchers** — Household vouchers for citizens
- **Assurance Package** — Cash transfers by income tier
- **Workfare Income Supplement (WIS)** — Piecewise linear tapering across 4 age bands
- **Silver Support** — Quarterly payouts by HDB flat type and income tier
- **ComCare** — Long-Term Assistance (LTA) and SMTA eligibility
- **Baby Bonus** — Cash gift by birth order
- **CDA First Step Grant** — By birth order and date
- **Childcare and infant care subsidies** — Basic + additional by GHI bracket
- **KiFAS** — Kindergarten fee assistance by GHI bracket
- **MOE FAS** — Financial assistance eligibility
- **CHAS** — Blue/Orange/Green tier classification by PCI
- **Enhanced CPF Housing Grant** — Up to $120k by GHI bracket
- **FDW levy concession** — Concessionary rates for families with children, elderly, or disabled
- **Student Care Fee Assistance (SCFA)** — By GHI bracket
- **Edusave contributions** — $230 (primary), $290 (secondary)

### Tax Reliefs
Earned income, spouse, child (QCR), working mother's child (WMCR), parent, handicapped parent, grandparent caregiver, sibling disability, CPF cash top-up, course fees, NSman (5 categories), and life insurance.

## Installation

### Requirements
- Python 3.10 or higher (3.13 recommended)

### Install from source

```bash
git clone https://github.com/PolicyEngine/policyengine-sg.git
cd policyengine-sg

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Quick Start

```python
from policyengine_sg import SingaporeTaxBenefitSystem
from policyengine_core.simulations import Simulation

system = SingaporeTaxBenefitSystem()

situation = {
    "people": {
        "person1": {
            "age": {"2025": 35},
            "is_citizen": {"2025": True},
            "employment_income": {"2025": 60_000},
        }
    },
    "benefit_units": {
        "bu": {
            "adults": ["person1"],
        }
    },
    "households": {
        "household": {
            "members": ["person1"],
        }
    },
}

simulation = Simulation(
    tax_benefit_system=system,
    situation=situation,
)

income_tax = simulation.calculate("income_tax", "2025")
cpf = simulation.calculate("cpf_total_contribution", "2025")

print(f"Income tax: S${income_tax[0]:,.2f}")
print(f"CPF total contribution: S${cpf[0]:,.2f}")
```

## Development

```bash
# Install development dependencies
uv pip install -e .[dev]

# Run tests (122 tests)
make test

# Format code
make format

# Check vectorization
make check-vectorization
```

## Project Stats

- ~113 variables
- ~155 parameter files with official .gov.sg sources
- 122 tests (all passing)

## Data and Validation

Parameters are sourced from and validated against:
- [IRAS](https://www.iras.gov.sg/) tax calculators and rate tables
- [CPF Board](https://www.cpf.gov.sg/) contribution tables and WIS calculator
- [MSF](https://www.msf.gov.sg/) ComCare and social assistance guidelines
- [MOF](https://www.mof.gov.sg/) Budget announcements and GSTV schedules
- [HDB](https://www.hdb.gov.sg/) housing grant information
- [ECDA](https://www.ecda.gov.sg/) childcare subsidy schedules

## Known Limitations

Some programs cannot be fully modeled due to PolicyEngine's single-period architecture:

| Program | Limitation |
|---------|-----------|
| CPF LIFE payouts | Needs CPF balance history |
| MediFund | Discretionary case-by-case assessment |
| ComCare SMTA amounts | Caseworker assessment (eligibility modeled) |
| PTR birth-order tracking | Multi-year carry-forward (balance input used) |
| SkillsFuture Credit | Balance tracking across periods |
| MediShield Life subsidies | Complex age+income premium matrix |
| CareShield Life subsidies | Complex premium/subsidy schedule |

See [GAPS.md](GAPS.md) for the full tracker.

## License

PolicyEngine Singapore is licensed under the [GNU Affero General Public License v3.0](LICENSE).

## Citation

```bibtex
@software{policyengine_singapore,
  title = {PolicyEngine Singapore},
  author = {PolicyEngine},
  year = {2025},
  url = {https://github.com/PolicyEngine/policyengine-sg}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/PolicyEngine/policyengine-sg/issues)
- **Email**: hello@policyengine.org
- **Website**: [policyengine.org](https://policyengine.org)
