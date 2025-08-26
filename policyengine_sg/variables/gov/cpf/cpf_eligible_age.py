"""
CPF eligibility based on age for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_eligible_age(Variable):
    value_type = bool
    entity = Person
    label = "CPF eligible by age"
    definition_period = YEAR
    default_value = False
    reference = "https://www.cpf.gov.sg/member/faq/growing-your-savings/saving-for-my-retirement/what-is-the-minimum-age-to-contribute-to-cpf"
    documentation = """
    Determines if a person is eligible for CPF contributions based on age.
    
    CPF contributions are required for:
    - Singapore Citizens and Permanent Residents
    - From age 16 until the last day of the month in which they turn 70
    
    Based on CPF Act Section 7.
    """

    def formula(person, period, parameters):
        age = person("age", period)

        # CPF eligible from age 16 to 70 (inclusive)
        # Age changes affect contributions from first day of month after birthday
        return (age >= 16) & (age <= 70)
