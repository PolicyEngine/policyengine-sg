"""
Age variable for Singapore tax-benefit system.
"""

from policyengine_sg.model_api import *


class age(Variable):
    value_type = int
    entity = Person
    label = "Age"
    definition_period = YEAR
    default_value = 0
    reference = "https://www.iras.gov.sg/taxes/individual-income-tax"
    documentation = """
    Age of the person in years.
    
    Used for various tax and benefit calculations including:
    - Income tax personal reliefs
    - CPF contribution rates
    - Social assistance eligibility
    """