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
