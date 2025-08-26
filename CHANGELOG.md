# Changelog

## [0.1.0] - 2024-08-26

### Added
- Initial implementation of Singapore tax-benefit microsimulation model
- CPF (Central Provident Fund) system with age-based contribution rates
- Support for ordinary wages and additional wages with dynamic ceilings
- Fully vectorized calculations for microsimulation performance
- Singapore-specific entity definitions (Person, TaxUnit, CPFUnit, BenefitUnit, Household)
- Directory structure for Singapore government agencies (IRAS, CPF, MSF, MOM)
- SGD currency support in model API
- Basic repository structure with Makefile, pyproject.toml, and README
- Test framework setup with pytest configuration
- Parameter structure for income tax, CPF, GST, ComCare, and WorkFare programs
- CI/CD foundation with comprehensive test coverage framework