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
        employer_rates = parameters(period).gov.cpf.contribution_rates.employer_rates
        
        # Use vectorized select for age-based rate calculation
        # CRITICAL: Using select() with default parameter for vectorization
        employer_rate = select(
            [
                age <= 55,
                (age > 55) & (age <= 60),
                (age > 60) & (age <= 65),
                (age > 65) & (age <= 70)
            ],
            [
                employer_rates.age_55_and_below,
                employer_rates.age_55_to_60,
                employer_rates.age_60_to_65,
                employer_rates.age_65_to_70
            ],
            default=employer_rates.above_age_70  # Age > 70
        )
        
        # Calculate contribution: only if CPF eligible
        employer_contribution = where(
            cpf_eligible,
            total_cpf_wages * employer_rate,
            0
        )
        
        return employer_contribution


def test_cpf_employer_contribution():
    """Test CPF employer contribution calculation with age-based rates."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Age 30 (17% rate)
    sim = Microsimulation()
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [60000])  # S$5k/month, all ordinary wage
    result = sim.calculate("cpf_employer_contribution", 2025)
    expected = 60000 * 0.17  # S$10,200
    assert abs(result[0] - expected) < 1
    
    # Test case 2: Age 58 (15.5% rate)
    sim.set_input("age", 2025, [58])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employer_contribution", 2025)
    expected = 60000 * 0.155  # S$9,300
    assert abs(result[0] - expected) < 1
    
    # Test case 3: Age 62 (12% rate)
    sim.set_input("age", 2025, [62])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employer_contribution", 2025)
    expected = 60000 * 0.12  # S$7,200
    assert abs(result[0] - expected) < 1
    
    # Test case 4: Age 67 (9% rate)
    sim.set_input("age", 2025, [67])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employer_contribution", 2025)
    expected = 60000 * 0.09  # S$5,400
    assert abs(result[0] - expected) < 1
    
    # Test case 5: Age 71 (not CPF eligible)
    sim.set_input("age", 2025, [71])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employer_contribution", 2025)
    assert result[0] == 0
    
    # Test case 6: High income with ceiling (Age 30)
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [120000])  # Above ceiling
    result = sim.calculate("cpf_employer_contribution", 2025)
    # Should be limited by annual ceiling of S$102,000
    max_contribution = 102000 * 0.17  # S$17,340
    assert result[0] <= max_contribution + 1  # Allow small rounding