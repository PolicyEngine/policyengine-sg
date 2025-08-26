"""
CPF Ordinary Wage (OW) calculation with monthly ceiling for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_ordinary_wage(Variable):
    value_type = float
    entity = Person
    label = "CPF Ordinary Wage"
    unit = SGD
    definition_period = MONTH
    default_value = 0
    reference = "https://www.cpf.gov.sg/service/article/what-is-the-ordinary-wage-ow-ceiling"
    documentation = """
    Monthly ordinary wage subject to CPF contributions, capped at the ordinary wage ceiling.
    
    Ordinary Wage (OW) includes:
    - Basic monthly salary
    - Fixed allowances
    - Overtime pay (if paid monthly)
    
    The OW is subject to a monthly ceiling:
    - 2025: S$7,400 per month
    - 2026: S$8,000 per month
    
    Based on CPF Act Section 7.
    """

    def formula(person, period, parameters):
        # Get monthly employment income (assuming this represents ordinary wage)
        monthly_income = person("employment_income", period.this_year) / 12
        
        # Get the ordinary wage ceiling for this period
        ow_ceiling = parameters(period).gov.cpf.ceilings.ordinary_wage_ceiling
        
        # Check if person is CPF eligible by age
        cpf_eligible = person("cpf_eligible_age", period.this_year)
        
        # Apply ceiling to ordinary wage, only if CPF eligible
        ordinary_wage = where(
            cpf_eligible,
            min_(monthly_income, ow_ceiling),
            0
        )
        
        return ordinary_wage


def test_cpf_ordinary_wage():
    """Test CPF ordinary wage calculation with ceiling."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Income below ceiling
    sim = Microsimulation()
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [60000])  # S$5,000/month
    result = sim.calculate("cpf_ordinary_wage", "2025-01")
    assert abs(result[0] - 5000) < 0.01
    
    # Test case 2: Income above ceiling (should be capped at S$7,400)
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [120000])  # S$10,000/month
    result = sim.calculate("cpf_ordinary_wage", "2025-01")
    assert abs(result[0] - 7400) < 0.01
    
    # Test case 3: Not CPF eligible by age (under 16)
    sim.set_input("age", 2025, [15])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_ordinary_wage", "2025-01")
    assert result[0] == 0
    
    # Test case 4: Not CPF eligible by age (over 70)
    sim.set_input("age", 2025, [71])
    sim.set_input("employment_income", 2025, [60000])
    result = sim.calculate("cpf_ordinary_wage", "2025-01")
    assert result[0] == 0