from policyengine_sg.model_api import *


class self_employment_income(Variable):
    value_type = float
    entity = Person
    label = "Self-employment income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
