from policyengine_sg.model_api import *


class dividend_income(Variable):
    value_type = float
    entity = Person
    label = "Dividend income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
