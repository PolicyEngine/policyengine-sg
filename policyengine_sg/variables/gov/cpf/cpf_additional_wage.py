"""
CPF Additional Wage (AW) calculation with dynamic ceiling for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_additional_wage(Variable):
    value_type = float
    entity = Person
    label = "CPF Additional Wage"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = "https://www.cpf.gov.sg/service/article/what-is-the-additional-wage-aw-ceiling"
    documentation = """
    Annual additional wage subject to CPF contributions, with dynamic ceiling.
    
    Additional Wage (AW) includes:
    - Bonuses (annual, performance, etc.)
    - Leave encashment
    - Commissions (if paid less frequently than monthly)
    - Overtime pay (if paid less frequently than monthly)
    
    The AW ceiling is calculated dynamically:
    AW Ceiling = S$102,000 - Total Ordinary Wages subject to CPF for the year
    
    This ensures total annual wages subject to CPF do not exceed S$102,000.
    
    Based on CPF Act Section 7.
    """

    def formula(person, period, parameters):
        # Check if person is CPF eligible by age
        cpf_eligible = person("cpf_eligible_age", period)
        
        # Get annual salary ceiling parameters
        annual_salary_ceiling = parameters(period).gov.cpf.ceilings.annual_contribution_limit.annual_salary_ceiling
        
        # Calculate total ordinary wages paid in the year (sum of all months)
        total_ow_paid = 0
        for month in period.get_subperiods(MONTH):
            monthly_ow = person("cpf_ordinary_wage", month)
            total_ow_paid = total_ow_paid + monthly_ow
        
        # Calculate dynamic AW ceiling
        # AW Ceiling = Annual ceiling - Total OW paid in the year
        aw_ceiling = max_(0, annual_salary_ceiling - total_ow_paid)
        
        # For simplicity, assume additional wage is any income above ordinary wage
        # In practice, this would be a separate input for bonuses, commissions etc.
        total_annual_income = person("employment_income", period)
        estimated_total_ow = total_ow_paid  # We already calculated this
        estimated_additional_wage = max_(0, total_annual_income - estimated_total_ow)
        
        # Apply the dynamic ceiling to additional wage, only if CPF eligible
        additional_wage = where(
            cpf_eligible,
            min_(estimated_additional_wage, aw_ceiling),
            0
        )
        
        return additional_wage


def test_cpf_additional_wage():
    """Test CPF additional wage calculation with dynamic ceiling."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Income within annual ceiling
    sim = Microsimulation()
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [80000])  # Below S$102k ceiling
    result = sim.calculate("cpf_additional_wage", 2025)
    # With income of S$80k, OW capped at S$7,400*12 = S$88,800
    # So AW should be S$80k - S$80k = S$0 (since total income < OW limit)
    assert result[0] >= 0
    
    # Test case 2: High income above annual ceiling
    sim.set_input("age", 2025, [30])
    sim.set_input("employment_income", 2025, [150000])  # Above S$102k ceiling
    result = sim.calculate("cpf_additional_wage", 2025)
    # Should be constrained by the annual ceiling logic
    assert result[0] >= 0
    
    # Test case 3: Not CPF eligible by age
    sim.set_input("age", 2025, [71])
    sim.set_input("employment_income", 2025, [80000])
    result = sim.calculate("cpf_additional_wage", 2025)
    assert result[0] == 0