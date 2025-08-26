"""
Employment income variable for Singapore tax-benefit system.
"""

from policyengine_sg.model_api import *


class employment_income(Variable):
    value_type = float
    entity = Person
    label = "Employment income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = "https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/taxable-income"
    documentation = """
    Annual employment income in Singapore dollars.
    
    This includes:
    - Salary and wages
    - Bonuses and allowances
    - Directors' fees
    - Benefits-in-kind (if taxable)
    
    Used for calculating:
    - Personal income tax
    - CPF contributions
    - Various benefit means tests
    """