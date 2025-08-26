"""
CPF Employee Contribution calculation with age-based rates for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_employee_contribution(Variable):
    value_type = float
    entity = Person
    label = "CPF Employee Contribution"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = "https://www.cpf.gov.sg/employer/employer-obligations/cpf-contributions/cpf-contribution-rates"
    documentation = """
    Annual CPF contribution made by the employee, calculated using age-based rates.
    
    Employee contribution rates (2025):
    - Age ≤ 55: 20%
    - Age 55-60: 17%
    - Age 60-65: 11.5%
    - Age 65-70: 7.5%
    - Age > 70: 5%
    
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
        
        # Get employee contribution rates from parameters
        employee_rates = parameters(period).gov.cpf.contribution_rates.employee_rates
        
        # Use vectorized select for age-based rate calculation
        # CRITICAL: Using select() with default parameter for vectorization
        employee_rate = select(
            [
                age <= 55,
                (age > 55) & (age <= 60),
                (age > 60) & (age <= 65),
                (age > 65) & (age <= 70)
            ],
            [
                employee_rates.age_55_and_below,
                employee_rates.age_55_to_60,
                employee_rates.age_60_to_65,
                employee_rates.age_65_to_70
            ],
            default=employee_rates.above_age_70  # Age > 70
        )
        
        # Calculate contribution: only if CPF eligible
        employee_contribution = where(
            cpf_eligible,
            total_cpf_wages * employee_rate,
            0
        )
        
        return employee_contribution


def test_cpf_employee_contribution():
    """Test CPF employee contribution calculation with age-based rates."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Age 30 (20% rate)
    sim = Microsimulation()
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [60000])  # S$5k/month, all ordinary wage
    result = sim.calculate("cpf_employee_contribution", 2025)
    expected = 60000 * 0.20  # S$12,000
    assert abs(result[0] - expected) < 1
    
    # Test case 2: Age 58 (17% rate)
    sim.set_input("age", 2025, [58])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employee_contribution", 2025)
    expected = 60000 * 0.17  # S$10,200
    assert abs(result[0] - expected) < 1
    
    # Test case 3: Age 62 (11.5% rate)
    sim.set_input("age", 2025, [62])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employee_contribution", 2025)
    expected = 60000 * 0.115  # S$6,900
    assert abs(result[0] - expected) < 1
    
    # Test case 4: Age 67 (7.5% rate)
    sim.set_input("age", 2025, [67])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employee_contribution", 2025)
    expected = 60000 * 0.075  # S$4,500
    assert abs(result[0] - expected) < 1
    
    # Test case 5: Age 71 (not CPF eligible)
    sim.set_input("age", 2025, [71])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_employee_contribution", 2025)
    assert result[0] == 0
    
    # Test case 6: High income with ceiling (Age 30)
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [120000])  # Above ceiling
    result = sim.calculate("cpf_employee_contribution", 2025)
    # Should be limited by annual ceiling of S$102,000
    max_contribution = 102000 * 0.20  # S$20,400
    assert result[0] <= max_contribution + 1  # Allow small rounding