# CPF Documentation Sources

This directory contains comprehensive documentation about Singapore's Central Provident Fund (CPF) system, compiled for use in policy modeling and analysis.

## Documentation Structure

### Core System Documentation
- **[CPF System Overview](cpf_system_overview.md)** - Comprehensive overview of the entire CPF system, its architecture, and key features
- **[Legislative References](legislative_references.md)** - Legal framework including the CPF Act and supporting regulations

### Implementation Details
- **[Contribution Rates](contribution_rates.md)** - Detailed contribution rates by age group, effective dates, and calculation examples
- **[Account Allocation](account_allocation.md)** - Rules for allocating contributions to OA, SA/RA, and MediSave accounts
- **[Salary Ceiling](salary_ceiling.md)** - Ordinary wage ceiling, additional wage ceiling, and annual contribution limits
- **[Retirement Schemes](retirement_schemes.md)** - BRS, FRS, ERS amounts and CPF LIFE annuity system
- **[Healthcare & Housing Schemes](healthcare_housing_schemes.md)** - MediSave, MediShield Life, CareShield Life, and housing withdrawal rules

## Key Parameters for Policy Modeling

### 2025 Contribution Rates
| Age Group | Employee | Employer | Total |
|-----------|----------|----------|-------|
| ≤ 55 | 20% | 17% | 37% |
| 55-60 | 17% | 15.5% | 32.5% |
| 60-65 | 11.5% | 12% | 23.5% |
| 65-70 | 7.5% | 9% | 16.5% |
| > 70 | 5% | 7.5% | 12.5% |

### 2025 Key Thresholds
- **Ordinary Wage Ceiling**: S$7,400 per month
- **Annual Salary Ceiling**: S$102,000 per year  
- **Minimum Wage for CPF**: S$500 per month
- **Full Contribution Threshold**: S$750 per month

### 2025 Retirement Sums
- **Basic Retirement Sum (BRS)**: S$106,500
- **Full Retirement Sum (FRS)**: S$213,000  
- **Enhanced Retirement Sum (ERS)**: S$426,000

### Interest Rates (2025)
- **Ordinary Account**: 2.5% per annum (floor rate)
- **Special/Retirement/MediSave**: 4% per annum (floor rate extended until 31 Dec 2025)

## Major Changes in 2025

1. **Special Account Closure**: SA for all 55+ members closes from Jan 2025, balances transfer to RA
2. **Enhanced Retirement Sum**: Increased from 3× to 4× BRS (S$426,000)
3. **Salary Ceiling**: Ordinary wage ceiling increased to S$7,400 (from S$6,800)
4. **Interest Rate Floor**: 4% floor extended for SA/RA/MA until end of 2025

## Data Quality and Sources

### Official Sources Used
- **CPF Board (cpf.gov.sg)**: Primary source for all contribution rates, procedures, and member information
- **Ministry of Manpower**: Policy development and regulatory framework
- **Ministry of Health**: Healthcare-related CPF policies (MediSave, MediShield Life)
- **Singapore Statutes Online**: Legislative references and legal framework

### Data Currency
- All information current as of January 2025
- Historical data included where relevant for trend analysis
- Future planned changes documented with effective dates

### Verification Notes
- Some detailed allocation percentages require verification from official CPF Board technical documentation
- Court cases and detailed legal precedents need additional legal research
- Specific calculation formulas for some benefits may require direct CPF Board confirmation

## Usage for Policy Modeling

### Implementation Priority
1. **Core contribution system**: Start with contribution_rates.md and salary_ceiling.md
2. **Account structure**: Implement basic OA, SA/RA, MA framework from account_allocation.md  
3. **Advanced features**: Add retirement schemes, healthcare, and housing components

### Key Modeling Considerations
- Age-based contribution rate transitions occur on first day of month after birthday
- Salary ceilings apply monthly for ordinary wages, annually for total wages
- Special Account closure affects members turning 55 from 2025 onwards
- Interest rates have floor guarantees that may override market rates

### Data Dependencies
- Birth dates for age-based rate calculations
- Employment status and income levels
- Property ownership for housing withdrawals and retirement sum calculations
- Health status for healthcare scheme participation

## Update Schedule

This documentation should be reviewed and updated:
- **Annually**: For budget-related changes (salary ceilings, retirement sums)
- **As needed**: For policy changes announced by CPF Board
- **Major reviews**: Every 3-5 years or when significant reforms occur

## Contact and Feedback

For questions about this documentation or to suggest improvements:
- Check official CPF Board website for most current information
- Cross-reference with Singapore Statutes Online for legal text
- Consider professional consultation for complex policy modeling scenarios

---
*Compiled by Document Collector Agent - January 2025*
*Based on official sources from CPF Board, MOM, MOH, and Singapore government*