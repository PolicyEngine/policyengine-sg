from policyengine_sg.model_api import *


class spouse_income(Variable):
    value_type = float
    entity = Person
    label = "Spouse's annual income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
