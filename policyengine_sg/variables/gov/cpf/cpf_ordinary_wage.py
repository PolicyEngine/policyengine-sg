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
            cpf_eligible, min_(monthly_income, ow_ceiling), 0
        )

        return ordinary_wage

