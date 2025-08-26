"""
CPF Total Contribution calculation for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_total_contribution(Variable):
    value_type = float
    entity = Person
    label = "CPF Total Contribution"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = "https://www.cpf.gov.sg/employer/employer-obligations/cpf-contributions/cpf-contribution-rates"
    documentation = """
    Total annual CPF contribution (employee + employer contributions).
    
    Total contribution rates (2025):
    - Age ≤ 55: 37% (20% employee + 17% employer)
    - Age 55-60: 32.5% (17% employee + 15.5% employer)
    - Age 60-65: 23.5% (11.5% employee + 12% employer)
    - Age 65-70: 16.5% (7.5% employee + 9% employer)
    - Age > 70: 12.5% (5% employee + 7.5% employer)
    
    Contributions are calculated on:
    - Ordinary Wages (subject to monthly ceiling)
    - Additional Wages (subject to dynamic annual ceiling)
    - Maximum annual contribution on S$102,000 ceiling
    
    Based on CPF Act, First Schedule.
    """

    def formula(person, period, parameters):
        # Calculate total as sum of employee and employer contributions
        employee_contribution = person("cpf_employee_contribution", period)
        employer_contribution = person("cpf_employer_contribution", period)
        
        total_contribution = employee_contribution + employer_contribution
        
        return total_contribution


def test_cpf_total_contribution():
    """Test CPF total contribution calculation."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Age 30 (37% total rate)
    sim = Microsimulation()
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [60000])  # S$5k/month, all ordinary wage
    result = sim.calculate("cpf_total_contribution", 2025)
    expected = 60000 * 0.37  # S$22,200 (20% + 17%)
    assert abs(result[0] - expected) < 1
    
    # Test case 2: Age 58 (32.5% total rate)
    sim.set_input("age", 2025, [58])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_total_contribution", 2025)
    expected = 60000 * 0.325  # S$19,500 (17% + 15.5%)
    assert abs(result[0] - expected) < 1
    
    # Test case 3: Age 62 (23.5% total rate)
    sim.set_input("age", 2025, [62])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_total_contribution", 2025)
    expected = 60000 * 0.235  # S$14,100 (11.5% + 12%)
    assert abs(result[0] - expected) < 1
    
    # Test case 4: Age 67 (16.5% total rate)
    sim.set_input("age", 2025, [67])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_total_contribution", 2025)
    expected = 60000 * 0.165  # S$9,900 (7.5% + 9%)
    assert abs(result[0] - expected) < 1
    
    # Test case 5: Age 71 (not CPF eligible)
    sim.set_input("age", 2025, [71])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_total_contribution", 2025)
    assert result[0] == 0
    
    # Test case 6: High income with ceiling (Age 30)
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [120000])  # Above ceiling
    result = sim.calculate("cpf_total_contribution", 2025)
    # Should be limited by annual ceiling of S$102,000
    max_contribution = 102000 * 0.37  # S$37,740
    assert result[0] <= max_contribution + 1  # Allow small rounding
    
    # Test case 7: Verify components add up correctly
    sim.set_input("age", 2025, [45])
    sim.set_input("employment_income", 2025, [80000])
    total_result = sim.calculate("cpf_total_contribution", 2025)
    employee_result = sim.calculate("cpf_employee_contribution", 2025)
    employer_result = sim.calculate("cpf_employer_contribution", 2025)
    assert abs(total_result[0] - (employee_result[0] + employer_result[0])) < 0.01