from policyengine_sg.model_api import *


class other_income(Variable):
    value_type = float
    entity = Person
    label = "Other taxable income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
