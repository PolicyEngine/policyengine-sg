"""
CPF Employer Contribution calculation with age-based rates for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_employer_contribution(Variable):
    value_type = float
    entity = Person
    label = "CPF Employer Contribution"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = "https://www.cpf.gov.sg/employer/employer-obligations/cpf-contributions/cpf-contribution-rates"
    documentation = """
    Annual CPF contribution made by the employer, calculated using age-based rates.
    
    Employer contribution rates (2025):
    - Age ≤ 55: 17%
    - Age 55-60: 15.5%
    - Age 60-65: 12%
    - Age 65-70: 9%
    - Age > 70: 7.5%
    
    Contributions are calculated on:
    - Ordinary Wages (subject to monthly ceiling)
    - Additional Wages (subject to dynamic annual ceiling)
    
    Based on CPF Act, First Schedule.
    """

    def formula(person, period, parameters):
        age = person("age", period)

        # Get CPF eligible status
        cpf_eligible = person("cpf_eligible_age", period)

        # Calculate total CPF wages (OW + AW)
        # Sum monthly ordinary wages for the year
        total_ow = 0
        for month in period.get_subperiods(MONTH):
            monthly_ow = person("cpf_ordinary_wage", month)
            total_ow = total_ow + monthly_ow

        # Get additional wages for the year
        additional_wage = person("cpf_additional_wage", period)

        # Total wages subject to CPF
        total_cpf_wages = total_ow + additional_wage

        # Get employer contribution rates from parameters
        employer_rates = parameters(
            period
        ).gov.cpf.contribution_rates.employer_rates

        # Use vectorized select for age-based rate calculation
        # CRITICAL: Using select() with default parameter for vectorization
        employer_rate = select(
            [
                age <= 55,
                (age > 55) & (age <= 60),
                (age > 60) & (age <= 65),
                (age > 65) & (age <= 70),
            ],
            [
                employer_rates.age_55_and_below,
                employer_rates.age_55_to_60,
                employer_rates.age_60_to_65,
                employer_rates.age_65_to_70,
            ],
            default=employer_rates.above_age_70,  # Age > 70
        )

        # Calculate contribution: only if CPF eligible
        employer_contribution = where(
            cpf_eligible, total_cpf_wages * employer_rate, 0
        )

        return employer_contribution

