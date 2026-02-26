from policyengine_sg.model_api import *


class interest_income(Variable):
    value_type = float
    entity = Person
    label = "Interest income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
